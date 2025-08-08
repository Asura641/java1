param(
    [string]$RepoPath
)

$javaDir = Join-Path $RepoPath 'java'

# Create the 'java' subdirectory if it doesn't exist
New-Item -ItemType Directory -Force -Path $javaDir

Get-ChildItem -Path $RepoPath -File | Where-Object { ($_.Extension -eq '.java' -or $_.Extension -eq '.class') -and $_.Name -ne 'auto_push.py' -and $_.Name -ne 'move_java_files.ps1' } | ForEach-Object {
    Move-Item -Path $_.FullName -Destination $javaDir -Force
}