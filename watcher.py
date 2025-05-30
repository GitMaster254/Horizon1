# watcher.py
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, indexer):
        self.indexer = indexer

    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".txt"):  # Or any file type you support
            print(f"[Watcher] New file detected: {event.src_path}")
            try:
                with open(event.src_path, "r", encoding="utf-8") as f:
                    content = f.read()
                title = os.path.basename(event.src_path)
                self.indexer.add_document(
                    file_path=event.src_path,
                    content=content,
                    title=title,
                    author="Unknown",
                    metadata={}
                )
                print(f"[Watcher] Indexed: {event.src_path}")
            except Exception as e:
                print(f"[Watcher Error] Failed to index {event.src_path}: {e}")

    def on_modified(self, event):
        self.on_created(event)  # Same behavior for now

def start_watching(indexer, directory="read"):
    from pathlib import Path
    path = Path(directory)
    if not path.exists():
        print(f"[Watcher] Directory '{directory}' does not exist.")
        return

    observer = Observer()
    handler = FileChangeHandler(indexer)
    observer.schedule(handler, str(path), recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
