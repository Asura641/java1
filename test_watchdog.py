import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

WATCH_FOLDER = r'c:\Users\abhis\java'

class MyEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if not event.is_directory:
            print(f"[Watchdog] Detected modified: {event.src_path}")

    def on_created(self, event):
        if not event.is_directory:
            print(f"[Watchdog] Detected created: {event.src_path}")

    def on_deleted(self, event):
        if not event.is_directory:
            print(f"[Watchdog] Detected deleted: {event.src_path}")

    def on_moved(self, event):
        if not event.is_directory:
            print(f"[Watchdog] Detected moved: {event.src_path} to {event.dest_path}")

def main():
    event_handler = MyEventHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
    observer.start()
    print(f"[Watchdog] Monitoring folder: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()