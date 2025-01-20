import os
import time
import shutil
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class FileSyncHandler(FileSystemEventHandler):
    """
    A custom file system event handler for syncing a file from the source 
    to the target location upon detecting changes.
    """
    def __init__(self, source_file, target_file):
        self.source_file = source_file
        self.target_file = target_file
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

    def sync_file(self):
        """
        Synchronize the file to the target location.
        Deletes the target file if the source file no longer exists.
        """
        try:
            if os.path.exists(self.source_file):
                shutil.copy2(self.source_file, self.target_file)
                return(f"File synced: {self.source_file} -> {self.target_file}")
            else:
                if os.path.exists(self.target_file):
                    confirm = input(
                        f"Source file deleted. Do you want to delete the target file {self.target_file}? (yes/no): "
                    ).strip().lower()
                    if confirm == "yes":
                        os.remove(self.target_file)
                        return(f"Target file deleted: {self.target_file}")
                    else:
                        return("Target file not deleted.")
        except Exception as e:
            return(f"Error syncing file: {e}")

    def on_modified(self, event):
        """Handle file modification events."""
        if event.src_path == self.source_file:
            return(f"File modified: {self.source_file}")
            self.sync_file()

    def on_created(self, event):
        """Handle file creation events."""
        if event.src_path == self.source_file:
            return(f"File created: {self.source_file}")
            self.sync_file()

    def on_deleted(self, event):
        """Handle file deletion events."""
        if event.src_path == self.source_file:
            return(f"File deleted: {self.source_file}")
            self.sync_file()


def sync_file(source_file: str, target_file: str):
    """
    Watches a file for changes (creation, modification, deletion) 
    and synchronizes it to a target location.

    Args:
        source_file (str): Path to the source file.
        target_file (str): Path to the target location.
    """
    if not os.path.exists(os.path.dirname(source_file)):
        raise FileNotFoundError(f"Source directory not found: {os.path.dirname(source_file)}")

    event_handler = FileSyncHandler(source_file, target_file)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(source_file), recursive=False)
    observer.start()

    return(f"Watching for changes in: {source_file}")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        return("Synchronization stopped.")
    observer.join()

