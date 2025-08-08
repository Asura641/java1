import os
import os
import subprocess
from datetime import datetime

# -------- CONFIGURATION --------
REPO_PATH = r"c:\Users\abhis\java"  # Set your local repo path
BRANCH = "master"
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

def get_git_tracked_files():
    output = run_command("git ls-files", cwd=REPO_PATH)
    if output:
        return set(os.path.normpath(f.strip()) for f in output.splitlines())
    return set()

def get_all_local_files():
    local_files = set()
    for root, dirs, files in os.walk(REPO_PATH):
        # Skip .git folder
        if '.git' in dirs:
            dirs.remove('.git')
        for file in files:
            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, REPO_PATH)
            local_files.add(os.path.normpath(rel_path))
    return local_files

def list_untracked_files():
    print("📂 Checking for files present in local folder but not tracked by Git...")
    tracked_files = get_git_tracked_files()
    local_files = get_all_local_files()

    print(f"Debug: Tracked files: {tracked_files}")
    print(f"Debug: Local files: {local_files}")

    untracked_files = local_files - tracked_files

    if untracked_files:
        print("❗ Untracked Files Detected:")
        for f in sorted(untracked_files):
            print(f"- {f}")
    else:
        print("✅ All local files are tracked by Git.")

def push_to_git():
    if not os.path.exists(REPO_PATH):
        print("❌ Repository path not found!")
        return

    list_untracked_files()  # Show files that are local but not in git

    print("🔍 Checking for file changes...")
    status = run_command("git status --porcelain", cwd=REPO_PATH)
    if not status:
        print("✅ No changes detected. Nothing to push.")
        return

    print("📌 Adding files...")
    run_command("git add .", cwd=REPO_PATH)

    print("📝 Committing changes...")
    run_command(f'git commit -m "{COMMIT_MESSAGE}"', cwd=REPO_PATH)

    print("🚀 Pushing to GitHub...")
    run_command(f"git push origin {BRANCH}", cwd=REPO_PATH)

    print("🎯 Push complete.")

if __name__ == "__main__":
    push_to_git()