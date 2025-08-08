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

def push_to_git():
    if not os.path.exists(REPO_PATH):
        print("❌ Repository path not found!")
        return

    print("🔍 Checking for file changes...")
    status = run_command("git status --porcelain", cwd=REPO_PATH)
    if not status:
        print("✅ No changes detected. Nothing to push.")
        return

    print("📦 Moving Java files to 'java' subdirectory...")
    # Move .java and .class files into the 'java' subdirectory
    move_command = (
        "Get-ChildItem -Path . -Include *.java, *.class -File | " +
        "Where-Object { $_.Name -ne 'auto_push.py' } | " +
        "ForEach-Object { Move-Item -Path $_.FullName -Destination (Join-Path '{REPO_PATH}' 'java') -Force }"
    )
    # Create the 'java' subdirectory if it doesn't exist
    run_command(f"powershell -Command \"New-Item -ItemType Directory -Force -Path (Join-Path '{REPO_PATH}' 'java')\"", cwd=REPO_PATH)
    run_command(f"powershell -Command \"& {{ {move_command} }}\"", cwd=REPO_PATH)

    print("📌 Adding files...")
    run_command("git add .", cwd=REPO_PATH)

    print("📝 Committing changes...")
    run_command(f'git commit -m "{COMMIT_MESSAGE}"', cwd=REPO_PATH)

    print("🚀 Pushing to GitHub...")
    run_command(f"git push origin {BRANCH}", cwd=REPO_PATH)

    print("🎯 Push complete.")

if __name__ == "__main__":
    push_to_git()