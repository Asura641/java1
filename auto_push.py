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

    # Get tracked files (relative paths)
    print("--- Tracked Files ---")
    tracked_files_raw = run_command("git ls-files", cwd=REPO_PATH)
    tracked_files = tracked_files_raw.splitlines() if tracked_files_raw else []
    for f in tracked_files:
        print(f)

    print("\n--- Untracked Files ---")
    # Get all files recursively using PowerShell (absolute paths)
    untracked_files_raw = run_command(
        'powershell -Command "Get-ChildItem -Path . -Recurse -File | ForEach-Object { $_.FullName }"',
        cwd=REPO_PATH
    )
    if not untracked_files_raw:
        print("⚠️ Could not get file list from PowerShell.")
        return

    all_files = untracked_files_raw.splitlines()
    untracked_list = []
    repo_path_normalized = REPO_PATH.replace('/', '\\').rstrip("\\") + "\\"

    # Convert tracked files to lowercase + normalized for better comparison
    tracked_set = set(f.lower().replace('/', '\\') for f in tracked_files)

    for full_path in all_files:
        full_path = full_path.strip()
        if not full_path.startswith(repo_path_normalized):
            continue  # Skip anything weird

        rel_path = full_path[len(repo_path_normalized):]  # relative path
        rel_path_normalized = rel_path.replace('/', '\\')

        if (
            '.git' in rel_path_normalized.lower() or
            rel_path_normalized.lower().startswith('java\\') or
            rel_path_normalized.lower() in tracked_set
        ):
            continue  # Skip git, already tracked, or inside 'java/'

        untracked_list.append(rel_path_normalized)

    if untracked_list:
        print("Untracked files:")
        for f in untracked_list:
            print(f)
    else:
        print("✅ No untracked files found.")
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