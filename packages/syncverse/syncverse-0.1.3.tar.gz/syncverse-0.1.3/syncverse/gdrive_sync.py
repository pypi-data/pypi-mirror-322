import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError

# Updated to broader access scope
SCOPES = ["https://www.googleapis.com/auth/drive"]  # Full Google Drive access

class GoogleDriveSyncHandler(FileSystemEventHandler):
    def __init__(self, local_file, drive_service, file_id=None):
        self.local_file = local_file
        self.drive_service = drive_service
        self.file_id = file_id

    def sync_to_drive(self):
        """Synchronize the file to Google Drive."""
        try:
            if os.path.exists(self.local_file):
                file_metadata = {'name': os.path.basename(self.local_file)}
                media = MediaFileUpload(self.local_file, resumable=True)

                if self.file_id:
                    # Update the existing file
                    updated_file = self.drive_service.files().update(
                        fileId=self.file_id,
                        media_body=media
                    ).execute()
                    print(f"File updated on Google Drive: {updated_file.get('name')}")
                else:
                    # Upload a new file
                    uploaded_file = self.drive_service.files().create(
                        body=file_metadata,
                        media_body=media,
                        fields='id'
                    ).execute()
                    self.file_id = uploaded_file.get('id')
                    print(f"File uploaded to Google Drive: {uploaded_file.get('name')} (ID: {self.file_id})")
            else:
                if self.file_id:
                    # Delete the file from Google Drive if it's removed locally
                    self.drive_service.files().delete(fileId=self.file_id).execute()
                    print(f"File deleted from Google Drive: {self.file_id}")
                    self.file_id = None
        except Exception as e:
            print(f"Error syncing to Google Drive: {e}")

    def on_modified(self, event):
        if event.src_path == self.local_file:
            print(f"File modified: {self.local_file}")
            self.sync_to_drive()

    def on_created(self, event):
        if event.src_path == self.local_file:
            print(f"File created: {self.local_file}")
            self.sync_to_drive()

    def on_deleted(self, event):
        if event.src_path == self.local_file:
            print(f"File deleted: {self.local_file}")
            self.sync_to_drive()

def authenticate_drive():
    """Authenticate and build the Google Drive API service."""
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def sync_to_drive(local_file):
    """
    Synchronizes a local file with Google Drive.
    - Authenticates and establishes the connection to Google Drive.
    - Monitors the file for changes.
    
    Args:
        local_file: Path to the local file to sync.
    """
    if not os.path.exists(local_file):
        print(f"Error: File not found at {local_file}")
        return

    drive_service = authenticate_drive()

    # Determine if the file already exists on Google Drive
    file_id = None
    file_name = os.path.basename(local_file)
    query = f"name='{file_name}' and trashed=false"
    print(f"Checking for file with query: {query}")

    try:
        # Search for the file on Google Drive
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        items = results.get('files', [])
        if items:
            # File exists, get the first matching file's ID
            file_id = items[0]['id']
            print(f"File found on Google Drive with ID: {file_id}")
        else:
            print("No matching file found on Google Drive. A new file will be uploaded.")
    except HttpError as error:
        print(f"An error occurred while searching for the file: {error}")
        return

    # Set up a file sync handler
    event_handler = GoogleDriveSyncHandler(local_file, drive_service, file_id)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(local_file), recursive=False)
    observer.start()

    print(f"Watching for changes in: {local_file}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("Synchronization stopped.")
    observer.join()



__all__ = ["GoogleDriveSyncHandler", "authenticate_drive", "sync_to_drive"]
