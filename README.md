# Temp File Remover

A Python application with a modern Windows 11-style UI to safely delete unused temporary files from the system's temp folder.

## Features

- Scans the temp folder for files not currently in use by any process
- Displays an estimate of the size (in MB and GB) of files that can be deleted
- Confirms before deletion
- Deletes only files that are not locked by running processes
- Tabbed interface: Program, Settings, Changelog
- Theme switching (Light/Dark/System)
- Version display and automatic update checking/downloading from GitHub
- Changelog fetched from the latest GitHub release

## Requirements

- Python 3.7+
- customtkinter
- psutil

## Installation and Running

### For Python Users:
1. Clone or download the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run the application: `python TempRemover.py`

### Standalone Executable (No Python Required):
1. Download the `TempRemover.exe` file from the latest [release](https://github.com/Rick007110/TempRemover/releases/latest).
2. Double-click `TempRemover.exe` to run the application directly on Windows.
3. Make sure to click `More Info` and then `Run anyway`. Windows defender (and possibly other AV's) show this program as a virus (which is a false positive) which is because of the way the python code gets bundled with PyInstaller.
4. Share the exe with friends without needing Python or packages installed.

## Usage

- **Program Tab**: Main functionality - scan and delete temp files.
- **Settings Tab**: Change appearance mode (Light, Dark, System), view current version, check for updates, and download new versions.
- **Changelog Tab**: View the changelog from the latest GitHub release.

## Note

This application only deletes files that are not currently open by any process. It does not delete directories or subfolders.

## To do

- [ ] Make the changelog view work better
- [ ] Make the background dark grey
- [ ] Blacklist files that are needed by TempRemover from being deleted in temp folder
