import sys
import os
import sys
import time
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# === CONFIGURATION ===
WATCH_FOLDER = "c:\\Users\\abhis\\java"


from auto_push import push_to_git, REPO_PATH, COMMIT_MESSAGE, run_command



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

    def check_for_changes(self):
        print("[GitPushHandler] Checking for changes...")
        status = run_command("git status --porcelain", cwd=self.repo_path)
        if status:
            print("[GitPushHandler] Changes detected. Scheduling push.")
            self.tray_app.status_label.setText("Changes detected. Scheduling push...")
            self.push_timer.start(5000) # Wait 5 seconds before pushing



    def start_git_push(self):
        print("[GitPushHandler] Directly calling push_to_git.")
        try:
            output = push_to_git()
            print(f"[GitPushHandler] Output from push_to_git: {output}") # Debug print
            self.tray_app.update_progress(output)
        except Exception as e:
            self.tray_app.show_error(f"Error during git push: {e}")









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

    def update_progress(self, message):
        self.status_label.setText(message)

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(self.progress_window, "Git Error", message)
        self.status_label.setText("Error occurred!")
        self.progress_bar.setValue(0)

    def handle_file_event(self, path):
        print(f"[GitTrayApp] File event received for: {path}")
        # Here you would trigger the git push logic, perhaps by calling start_git_push on event_handler

def main():
    app = QtWidgets.QApplication(sys.argv)

    tray_app = GitTrayApp(REPO_PATH)
    event_handler = GitPushHandler(REPO_PATH, tray_app)
    # tray_app.event_handler = event_handler  # allow handle_file_event to call start_git_push()

    # Connect signals from GitPushHandler to GitTrayApp's handle_file_event
    # Note: GitPushHandler now directly calls schedule_push via QMetaObject.invokeMethod
    # So these connections are not strictly needed for watchdog events, but keep for clarity if needed elsewhere.
    # event_handler.file_modified.connect(tray_app.handle_file_event)
    # event_handler.file_created.connect(tray_app.handle_file_event)

    # Start a timer to periodically check for changes
    check_timer = QtCore.QTimer()
    check_timer.timeout.connect(event_handler.check_for_changes)
    check_timer.start(10000) # Check every 10 seconds
    print("[main] QTimer started for polling.")

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()