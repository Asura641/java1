import os
import subprocess
from datetime import datetime

# -------- CONFIGURATION --------
REPO_PATH = r"c:\Users\abhis\java"  # Set your local repo path
BRANCH = "main"
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
        return f"[ERROR] {e.stderr.strip()}"

def get_git_tracked_files():
    output = run_command("git ls-files", cwd=REPO_PATH)
    if output and not output.startswith("[ERROR]"):
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
    output_lines = []
    output_lines.append("📂 Checking for files present in local folder but not tracked by Git...")
    tracked_files = get_git_tracked_files()
    local_files = get_all_local_files()

    untracked_files = local_files - tracked_files

    if untracked_files:
        output_lines.append("❗ Untracked Files Detected:")
        for f in sorted(untracked_files):
            output_lines.append(f"- {f}")
    else:
        output_lines.append("✅ All local files are tracked by Git.")
    return "\n".join(output_lines)

def push_to_git():
    output_lines = []
    # print("DEBUG: Entering push_to_git") # Debug print
    if not os.path.exists(REPO_PATH):
        output_lines.append("❌ Repository path not found!")
        # print("DEBUG: Repo path not found, returning.") # Debug print
        return "\n".join(output_lines)

    output_lines.append(list_untracked_files())

    output_lines.append("🔍 Checking for file changes...")
    status = run_command("git status --porcelain", cwd=REPO_PATH)
    if not status or status.startswith("[ERROR]") or "nothing to commit" in status:
        output_lines.append("✅ No changes detected. Nothing to push.")
        result = "\n".join(output_lines)
        # print("DEBUG: No changes detected, returning.") # Debug print
        return result

    output_lines.append("📌 Adding files...")
    add_output = run_command("git add .", cwd=REPO_PATH)
    if add_output and add_output.startswith("[ERROR]"):
        output_lines.append(add_output)
        # print("DEBUG: Error adding files, returning.") # Added this for completeness
        return "\n".join(output_lines)

    output_lines.append("📝 Committing changes...")
    commit_output = run_command(f'git commit -m "{COMMIT_MESSAGE}"', cwd=REPO_PATH)
    if commit_output and commit_output.startswith("[ERROR]"):
        output_lines.append(commit_output)
        # print("DEBUG: Error committing changes, returning.") # Added this for completeness
        return "\n".join(output_lines)

    output_lines.append("🚀 Pushing to GitHub...")
    push_output = run_command(f"git push origin {BRANCH}", cwd=REPO_PATH)
    if push_output and push_output.startswith("[ERROR]"):
        output_lines.append(push_output)
        # print("DEBUG: Error pushing to GitHub, returning.") # Added this for completeness
        return "\n".join(output_lines)

    output_lines.append("🎯 Push complete.")
    final_output = "\n".join(output_lines)
    # print(f"DEBUG: push_to_git returning: {final_output}") # Debug print
    return final_output

if __name__ == "__main__":
    print(push_to_git())