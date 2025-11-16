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
- Changelog management (developer access only)

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
1. Download the `TempRemover.exe` file from the `dist` folder.
2. Double-click `TempRemover.exe` to run the application directly on Windows.
3. Share the exe with friends without needing Python or packages installed.

## Usage

- **Program Tab**: Main functionality - scan and delete temp files.
- **Settings Tab**: Change appearance mode (Light, Dark, System), view current version, check for updates, and download new versions.
- **Changelog Tab**: View changelog; edit only with password (for developers).

## Note

This application only deletes files that are not currently open by any process. It does not delete directories or subfolders.