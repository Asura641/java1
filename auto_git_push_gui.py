import sys
import os
import time
from PyQt5 import QtWidgets, QtGui, QtCore
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from git import Repo, GitCommandError
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# === CONFIGURATION ===
WATCH_FOLDER = r"c:\Users\abhis\java"
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

class GitPushHandler(FileSystemEventHandler):
    def __init__(self, repo_path, progress_callback, error_callback):
        super().__init__()
        self.repo_path = repo_path
        self.progress_callback = progress_callback
        self.error_callback = error_callback

    def on_modified(self, event):
        if event.is_directory:
            return
        self.start_git_push()

    def on_created(self, event):
        if event.is_directory:
            return
        self.start_git_push()

    def start_git_push(self):
        self.thread = QThread()
        self.worker = GitWorker(self.repo_path, COMMIT_MESSAGE)
        self.worker.moveToThread(self.thread)

        self.worker.progress.connect(self.progress_callback)
        self.worker.error.connect(self.error_callback)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.started.connect(self.worker.run)
        self.thread.start()

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

def main():
    app = QtWidgets.QApplication(sys.argv)
    # repo = Repo(WATCH_FOLDER) # No longer needed directly in main thread
    tray_app = GitTrayApp(WATCH_FOLDER)
    event_handler = GitPushHandler(WATCH_FOLDER, tray_app.update_progress, tray_app.show_error)
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=True)
    observer.start()

    try:
        sys.exit(app.exec_())
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()