import sys
import os
import sys
import time
import subprocess
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import QObject, pyqtSignal, QThread




from auto_push import push_to_git, COMMIT_MESSAGE, run_command



class GitPushHandler(QObject):
    file_modified = pyqtSignal(str)
    file_created = pyqtSignal(str)
    def __init__(self, tray_app):
        super().__init__()
        self.tray_app = tray_app
        self.repo_configs = [] # List of dictionaries: {'repo_path': '', 'auth_token': '', 'repo_url': ''}
        self.push_timer = QtCore.QTimer()
        self.push_timer.setSingleShot(True)
        self.push_timer.timeout.connect(self.start_git_push)
        self.active_threads = [] # To keep references to threads

    def check_for_changes(self):
        for config in self.repo_configs:
            repo_path = config['repo_path']
            if not repo_path or not os.path.isdir(repo_path):
                self.tray_app.status_label.setText(f"Invalid path for {repo_path}. Please enter a valid repository path.")
                continue

            print(f"[GitPushHandler] Checking for changes in {repo_path}...")
            status = run_command("git status --porcelain", cwd=repo_path)
            if status and not status.startswith("[ERROR]"):
                print(f"[GitPushHandler] Changes detected in {repo_path}. Scheduling push.")
                self.tray_app.status_label.setText(f"Changes detected in {repo_path}. Scheduling push...")
                self.push_timer.start(5000) # Wait 5 seconds before pushing
            elif status.startswith("[ERROR]"):
                self.tray_app.status_label.setText(f"Error checking changes in {repo_path}: {status}")



    def start_git_push(self):
        for config in self.repo_configs:
            repo_path = config['repo_path']
            auth_token = config['auth_token']
            repo_url = config['repo_url']

            if not repo_path or not os.path.isdir(repo_path):
                self.tray_app.status_label.setText(f"Skipping push for invalid path: {repo_path}")
                continue

            print(f"[GitPushHandler] Directly calling push_to_git for {repo_path}.")
            try:
                output = push_to_git(repo_path, auth_token, repo_url, progress_callback=self.tray_app.update_progress_callback)
                self.tray_app.update_progress(f"Push for {repo_path}: {output}")
            except Exception as e:
                self.tray_app.show_error(f"Error during git push for {repo_path}: {e}")









class GitTrayApp(QtWidgets.QSystemTrayIcon):
    def __init__(self):
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

        # Input fields
        # Container for multiple repository inputs
        self.repo_configs_widget = QtWidgets.QWidget()
        self.repo_configs_layout = QtWidgets.QVBoxLayout(self.repo_configs_widget)
        self.repo_configs_layout.addStretch(1) # Allows items to push to top

        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.repo_configs_widget)
        layout.addWidget(self.scroll_area)

        # Buttons for adding/removing repositories
        button_layout = QtWidgets.QHBoxLayout()
        self.add_repo_button = QtWidgets.QPushButton("Add Repository")
        self.add_repo_button.clicked.connect(self.add_repo_input_fields)
        self.remove_repo_button = QtWidgets.QPushButton("Remove Selected")
        self.remove_repo_button.clicked.connect(self.remove_selected_repo_input_fields)
        button_layout.addWidget(self.add_repo_button)
        button_layout.addWidget(self.remove_repo_button)
        layout.addLayout(button_layout)

        self.repo_input_fields = [] # List to store tuples of (auth_token_input, location_input, repo_url_input)
        self.add_repo_input_fields() # Add initial set of input fields

        layout.addWidget(QtWidgets.QLabel("Push Progress:"))
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)

        self.push_button = QtWidgets.QPushButton("Manual Git Push")
        layout.addWidget(self.push_button)

        self.progress_window.setLayout(layout)
        self.progress_window.resize(400, 350) # Increased height to accommodate the button
        self.progress_window.show()
        self.show()

    def update_progress(self, message):
        self.status_label.setText(message)

    def update_progress_callback(self, value, message):
        self.progress_bar.setValue(value)
        self.status_label.setText(message)

    def show_error(self, message):
        QtWidgets.QMessageBox.critical(self.progress_window, "Git Error", message)
        self.status_label.setText("Error occurred!")
        self.progress_bar.setValue(0)

    def add_repo_input_fields(self):
        group_box = QtWidgets.QGroupBox(f"Repository {len(self.repo_input_fields) + 1}")
        group_layout = QtWidgets.QVBoxLayout()

        auth_token_input = QtWidgets.QLineEdit()
        auth_token_input.setPlaceholderText("Enter GitHub Auth Token")
        location_input = QtWidgets.QLineEdit()
        location_input.setPlaceholderText("Enter Repository Location (e.g., C:\\Users\\YourUser\\Repo)")
        repo_url_input = QtWidgets.QLineEdit()
        repo_url_input.setPlaceholderText("Enter Repository URL (e.g., https://github.com/user/repo.git)")

        checkbox = QtWidgets.QCheckBox("Select for Removal")

        group_layout.addWidget(QtWidgets.QLabel("Auth Token:"))
        group_layout.addWidget(auth_token_input)
        group_layout.addWidget(QtWidgets.QLabel("Repository Location:"))
        group_layout.addWidget(location_input)
        group_layout.addWidget(QtWidgets.QLabel("Repository URL:"))
        group_layout.addWidget(repo_url_input)
        group_layout.addWidget(checkbox)

        group_box.setLayout(group_layout)
        self.repo_configs_layout.insertWidget(self.repo_configs_layout.count() - 1, group_box) # Insert before the stretch
        self.repo_input_fields.append((auth_token_input, location_input, repo_url_input, group_box, checkbox))

    def remove_selected_repo_input_fields(self):
        to_remove = []
        for i, (auth_token_input, location_input, repo_url_input, group_box, checkbox) in enumerate(self.repo_input_fields):
            if checkbox.isChecked():
                to_remove.append(i)

        # Remove in reverse order to avoid index issues
        for i in reversed(to_remove):
            auth_token_input, location_input, repo_url_input, group_box, checkbox = self.repo_input_fields.pop(i)
            group_box.deleteLater()

    def handle_file_event(self, path):
        print(f"[GitTrayApp] File event received for: {path}")
        # Here you would trigger the git push logic, perhaps by calling start_git_push on event_handler

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Retrieve values from input fields
    # Initialize tray_app first to access input fields
    tray_app = GitTrayApp()

    event_handler = GitPushHandler(tray_app)

    # Populate repo_configs in event_handler from GUI inputs
    for auth_token_input, location_input, repo_url_input, _, _ in tray_app.repo_input_fields:
        event_handler.repo_configs.append({
            'auth_token': auth_token_input.text(),
            'repo_path': location_input.text(),
            'repo_url': repo_url_input.text()
        })

    tray_app.push_button.clicked.connect(event_handler.start_git_push)

    # The check_timer now directly calls the event_handler's check_for_changes
    check_timer = QtCore.QTimer()
    check_timer.timeout.connect(event_handler.check_for_changes)
    check_timer.start(10000) # Check every 10 seconds
    print("[main] QTimer started for polling.")

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