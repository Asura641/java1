import sys
import os
import time
from PyQt5 import QtWidgets, QtGui, QtCore
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo, GitCommandError
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# === CONFIGURATION ===
WATCH_FOLDER = "c:\\Users\\abhis\\java\\java"
COMMIT_MESSAGE = "Auto-commit: Updated files"

class GitWorker(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, repo_path, commit_message):
        super().__init__()
        self.repo_path = repo_path
        self.commit_message = commit_message

    def run(self):
        try:
            from git import Repo
            repo = Repo(self.repo_path)
            repo.git.add(A=True)
            if repo.is_dirty():
                repo.index.commit(self.commit_message)
                self.progress.emit(20)
                repo.remotes.origin.push()
                self.progress.emit(100)
            else:
                self.progress.emit(100) # No changes to push, still complete
        except Exception as e:
            self.error.emit(f"Error: {e}")
        finally:
            self.finished.emit()

class GitPushHandler(QObject):
    file_modified = pyqtSignal(str)
    file_created = pyqtSignal(str)
    def __init__(self, repo_path, tray_app):
        super().__init__()
        self.repo_path = repo_path
        self.tray_app = tray_app
        self.push_timer = QtCore.QTimer()
        self.push_timer.setSingleShot(True)
        self.push_timer.timeout.connect(self.start_git_push)
        self.active_threads = [] # To keep references to threads

    def schedule_push(self, path):
        print(f"[GitPushHandler] Scheduling push for: {path}")
        self.tray_app.status_label.setText(f"Waiting to push... {path}")
        self.push_timer.start(5000)  # Wait 5 sec before pushing



    def start_git_push(self):

        thread = QThread()
        worker = GitWorker(self.repo_path, COMMIT_MESSAGE)
        worker.moveToThread(thread)

        worker.progress.connect(self.tray_app.update_progress)
        worker.error.connect(self.tray_app.show_error)
        worker.finished.connect(thread.quit)
        worker.finished.connect(worker.deleteLater)
        thread.finished.connect(thread.deleteLater)

        # Clean up finished threads
        thread.finished.connect(lambda: self.active_threads.remove(thread))

        thread.started.connect(worker.run)
        thread.start()
        self.active_threads.append(thread) # Store reference to the thread



class WatchdogEventHandler(FileSystemEventHandler):
    def __init__(self, git_push_handler):
        super().__init__()
        self.git_push_handler = git_push_handler

    def on_modified(self, event):
        if not event.is_directory:
            print(f"[WatchdogEventHandler] File modified: {event.src_path}")
            QtCore.QMetaObject.invokeMethod(self.git_push_handler, 'schedule_push', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, event.src_path))

    def on_created(self, event):
        if not event.is_directory:
            print(f"[WatchdogEventHandler] File created: {event.src_path}")
            QtCore.QMetaObject.invokeMethod(self.git_push_handler, 'schedule_push', QtCore.Qt.QueuedConnection, QtCore.Q_ARG(str, event.src_path))





class GitTrayApp(QtWidgets.QSystemTrayIcon):
    def __init__(self, repo_path):
        self.repo_path = repo_path
        icon = QtGui.QIcon("icon.png")
        super().__init__(icon)

        menu = QtWidgets.QMenu()
        quit_action = menu.addAction("Quit")
        quit_action.triggered.connect(QtWidgets.qApp.quit)
        self.setContextMenu(menu)

        self.progress_window = QtWidgets.QWidget()
        self.progress_window.setWindowTitle("Auto Git Push")
        layout = QtWidgets.QVBoxLayout()
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setValue(0)
        self.status_label = QtWidgets.QLabel("Idle")
        layout.addWidget(QtWidgets.QLabel("Push Progress:"))
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        self.progress_window.setLayout(layout)
        self.progress_window.resize(300, 100)
        self.progress_window.show()
        self.show()

    def update_progress(self, value):
        self.progress_bar.setValue(value)
        if value == 100:
            self.status_label.setText("Push complete!")
        elif value == 0:
            self.status_label.setText("Starting push...")
        else:
            self.status_label.setText(f"Pushing... {value}%")

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(self.progress_window, "Git Error", message)
        self.status_label.setText("Error occurred!")
        self.progress_bar.setValue(0)

    def handle_file_event(self, path):
        print(f"[GitTrayApp] File event received for: {path}")
        # Here you would trigger the git push logic, perhaps by calling start_git_push on event_handler

def main():
    app = QtWidgets.QApplication(sys.argv)

    tray_app = GitTrayApp(WATCH_FOLDER)
    event_handler = GitPushHandler(WATCH_FOLDER, tray_app)
    # tray_app.event_handler = event_handler  # allow handle_file_event to call start_git_push()

    # Connect signals from GitPushHandler to GitTrayApp's handle_file_event
    # Note: GitPushHandler now directly calls schedule_push via QMetaObject.invokeMethod
    # So these connections are not strictly needed for watchdog events, but keep for clarity if needed elsewhere.
    # event_handler.file_modified.connect(tray_app.handle_file_event)
    # event_handler.file_created.connect(tray_app.handle_file_event)

    observer = Observer()
    # Pass the event_handler (which is GitPushHandler) directly to WatchdogEventHandler
    # WatchdogEventHandler will then use QMetaObject.invokeMethod to call schedule_push on GitPushHandler
    watchdog_event_handler = WatchdogEventHandler(event_handler)
    observer.schedule(watchdog_event_handler, WATCH_FOLDER, recursive=True)
    observer.start()

    try:
        sys.exit(app.exec_())
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()