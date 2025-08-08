import os
import subprocess
from datetime import datetime

# -------- CONFIGURATION --------
REPO_PATH = r"c:\Users\abhis\java"  # Replace with your actual local path
BRANCH = "master"                                 # Use the correct branch (main or master)
COMMIT_MESSAGE = f"Auto update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
# --------------------------------

def run_command(command, cwd=None):
    try:
        result = subprocess.run(
            command, cwd=cwd, shell=True, check=True,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {e.stderr.strip()}")
        return None

def list_repo_files():
    print("📂 Listing files in the repository:")
    print("--- Tracked Files ---")
    tracked_files = run_command("git ls-files", cwd=REPO_PATH)
    if tracked_files:
        print(tracked_files)
    else:
        print("No tracked files found.")

    print("\n--- Untracked Files ---")
    # Using PowerShell to list untracked files, excluding directories and .git folder
    untracked_files_command = "powershell -Command \"Get-ChildItem -Path . -Recurse -File | Where-Object { ($_.FullName -notlike '*.git*') -and ($_.FullName -notlike '*/java/*') } | ForEach-Object { $_.FullName }\""
    untracked_files = run_command(untracked_files_command, cwd=REPO_PATH)
    if untracked_files:
        # Filter out files that are already tracked (git ls-files output)
        tracked_list = tracked_files.splitlines() if tracked_files else []
        untracked_list = [f for f in untracked_files.splitlines() if f not in tracked_list]
        if untracked_list:
            print("\n".join(untracked_list))
        else:
            print("No untracked files found.")
    else:
        print("No untracked files found.")
    print("-----------------------")

def push_to_git():
    if not os.path.exists(REPO_PATH):
        print("❌ Repository path not found!")
        return

    list_repo_files() # Call the new function here

    print("🔍 Checking for file changes...")
    status = run_command("git status --porcelain", cwd=REPO_PATH)
    if not status:
        print("✅ No changes detected. Nothing to push.")
        return

    print("📦 Moving Java files to 'java' subdirectory...")
    # Execute the PowerShell script to move .java and .class files
    run_command(f"powershell -File move_java_files.ps1 -RepoPath '{REPO_PATH}'", cwd=REPO_PATH)

    print("📌 Adding files...")
    run_command("git add .", cwd=REPO_PATH)

    print("📝 Committing changes...")
    run_command(f'git commit -m "{COMMIT_MESSAGE}"', cwd=REPO_PATH)

    print("🚀 Pushing to GitHub...")
    run_command(f"git push origin {BRANCH}", cwd=REPO_PATH)

    print("🎯 Push complete.")

if __name__ == "__main__":
    push_to_git()