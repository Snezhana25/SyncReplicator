# SyncReplicator

SyncReplicator is a simple Python tool that keeps two folders in sync. It copies new or updated files from the source folder to the destination folder and deletes any files in the destination that are no longer in the source.

## Features

- **One-way sync** from source to destination.
- **Automatic folder detection** if source and destination folders are not provided.
- **Logs actions** (copying, deleting) to both the console and a log file.
- **Customizable sync interval**.

## Usage

You can run SyncReplicator from the command line. If no folder paths are provided, it will automatically use `SourceFolder` and `DestinationFolder` inside the project directory.

### Command-line Arguments

- `--source`: Path to the source folder (default: `SourceFolder`).
- `--destination`: Path to the destination folder (default: `DestinationFolder`).
- `--interval`: Time between syncs in seconds (default: 2 seconds).
- `--logfile`: Path to the log file (default: `sync_log.txt`).

### Example

```bash
python3 sync_folders.py
