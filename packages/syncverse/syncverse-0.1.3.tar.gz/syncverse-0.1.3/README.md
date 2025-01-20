## Syncverse
Syncverse is a Python package that helps you synchronize files between your local storage and cloud storage (Google Drive). With Syncverse, you can easily monitor and keep your files in sync—whether it's uploading, updating, or deleting files on Google Drive, or syncing files between local directories.

## Features
Local File Sync - Synchronize files between two local directories.
Google Drive Sync - Sync files to Google Drive from local, including support for file updates and deletions.

## Installation
Install Syncverse directly from PyPI using:
```pip install syncverse```

## Requirements
Python 3.6 or higher
watchdog for file system monitoring
Google API client libraries for Google Drive integration
To install dependencies manually using requirements.txt: 
```pip install -r requirements.txt```

## Usage
### Importing the Package
```console
import syncverse
import gdrive_sync
from syncverse.gdrive_sync import GoogleDriveSyncHandler
from syncverse.local_sync import FileSyncHandler
```

## Synchronizing Files Locally
### Sync files between two local directories:
```console
from syncverse.local_sync import FileSyncHandler

# Define source and destination file paths
source_file = "path/to/your/sourcefile"
destination_file = "path/to/your/destinationfile"

# Initialize FileSyncHandler
local_sync = FileSyncHandler(source_file, destination_file)

# Start synchronization
local_sync.sync_file()
```
### Explanation:

```FileSyncHandler```: Monitors and synchronizes changes from a source file to a destination file.

## Synchronizing Files with Google Drive
### Sync a local file with Google Drive:
```console
from syncverse.gdrive_sync import GoogleDriveSyncHandler

# Authenticate Google Drive (Make sure your 'credentials.json' is in the working directory)
drive_service = authenticate_drive()

# Define local file path
local_file_path = "path/to/your/localfile"

# Initialize GoogleDriveSyncHandler
drive = GoogleDriveSyncHandler(local_file_path, drive_service, file_id=None)

# Start synchronization
drive.sync_to_drive()
```
### Explanation:

```authenticate_drive()```: Authenticates and connects to Google Drive.
```GoogleDriveSyncHandler```: Handles synchronization between the local file and Google Drive.
```file_id```: If set to None, a new file will be uploaded; if an ID is provided, the file will be updated instead.

## Google Drive Authentication
For Google Drive synchronization, you'll need to authenticate your Google account. The first time you run a Google Drive sync, the package will prompt you to authenticate using OAuth2.

After successful authentication, your credentials will be stored in a token.json file, so you don't need to authenticate again unless the token expires.

### Steps to authenticate:

Place your ```credentials.json```(from Google Cloud Console) in your working directory.
Run the script, and a browser window will open for authentication.
After granting permissions, a ```token.json``` file will be created.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements
This package uses the watchdog library for monitoring file system events.
The Google API Client Library for Python (google-api-python-client) is used to interact with Google Drive.

## Support
If you encounter any issues, feel free to open an issue.