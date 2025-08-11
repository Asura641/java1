import os
import subprocess
from datetime import datetime


BRANCH = "main"
COMMIT_MESSAGE = f"Auto update {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
# --------------------------------

def run_command(command, cwd=None):
    try:
        # Ensure cwd is a valid directory if provided
        if cwd and not os.path.isdir(cwd):
            return f"[ERROR] Directory not found: {cwd}"

        result = subprocess.run(command, shell=True, check=True, cwd=cwd,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        error_message = f"[ERROR] Command '{command}' failed with exit code {e.returncode}.\nStdout: {e.stdout.strip()}\nStderr: {e.stderr.strip()}"
        print(error_message)
        return error_message
    except FileNotFoundError:
        error_message = f"[ERROR] Command not found: {command.split()[0]}"
        print(error_message)
        return error_message
    except Exception as e:
        error_message = f"[ERROR] An unexpected error occurred: {e}"
        print(error_message)
        return error_message

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

def push_to_git(repo_path, auth_token, repo_url, progress_callback=None):
    output_lines = []
    # print("DEBUG: Entering push_to_git") # Debug print
    if not os.path.exists(repo_path):
        output_lines.append("❌ Repository path not found!")
        # print("DEBUG: Repo path not found, returning.") # Debug print
        return "\n".join(output_lines)

    output_lines.append(list_untracked_files())

    if progress_callback:
        progress_callback(10, "🔍 Checking for file changes...")
    output_lines.append("🔍 Checking for file changes...")
    status = run_command("git status --porcelain", cwd=repo_path)
    if not status or status.startswith("[ERROR]") or "nothing to commit" in status:
        output_lines.append("✅ No changes detected. Nothing to push.")
        result = "\n".join(output_lines)
        # print("DEBUG: No changes detected, returning.") # Debug print
        return result

    if progress_callback:
        progress_callback(40, "📌 Adding files...")
    output_lines.append("📌 Adding files...")
    add_output = run_command("git add .", cwd=repo_path)
    if add_output and add_output.startswith("[ERROR]"):
        output_lines.append(add_output)
        # print("DEBUG: Error adding files, returning.") # Added this for completeness
        return "\n".join(output_lines)

    if progress_callback:
        progress_callback(70, "📝 Committing changes...")
    output_lines.append("📝 Committing changes...")
    commit_output = run_command(f'git commit -m "{COMMIT_MESSAGE}"', cwd=repo_path)
    if commit_output and commit_output.startswith("[ERROR]"):
        output_lines.append(commit_output)
        # print("DEBUG: Error committing changes, returning.") # Added this for completeness
        return "\n".join(output_lines)

    if progress_callback:
        progress_callback(90, "🚀 Pushing to GitHub...")
    output_lines.append("🚀 Pushing to GitHub...")
    # Configure Git to use the provided authentication token for the repository URL
    # This is a temporary configuration for the current operation
    run_command(f"git config --local credential.helper \"!f() {{ echo \"username=oauth2\\npassword={auth_token}\"; }}; f\"", cwd=repo_path)
    run_command(f"git remote set-url origin {repo_url}", cwd=repo_path)

    push_output = run_command(f"git push origin {BRANCH}", cwd=repo_path)

    # Clear the temporary credential helper
    run_command("git config --local --unset credential.helper", cwd=repo_path)
    if push_output and push_output.startswith("[ERROR]"):
        output_lines.append(push_output)
        # print("DEBUG: Error pushing to GitHub, returning.") # Added this for completeness
        return "\n".join(output_lines)

    output_lines.append("🎯 Push complete.")
    if progress_callback:
        progress_callback(100, "🎯 Push complete.")
    final_output = "\n".join(output_lines)
    # print(f"DEBUG: push_to_git returning: {final_output}") # Debug print
    return final_output

# The main execution block is removed as this file is now a module for the GUI.