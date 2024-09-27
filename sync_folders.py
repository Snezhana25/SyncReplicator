import os
import shutil
import logging
from time import sleep
import argparse

# Get the current project directory (this will be used as a base path)
project_directory = os.path.dirname(os.path.abspath(__file__))

# Set up command-line argument parsing
parser = argparse.ArgumentParser(description="Sync two folders: source and replica.")
parser.add_argument("--source", default=os.path.join(project_directory, "SourceFolder"),
                    help="Source folder path (default: SourceFolder in project directory)")
parser.add_argument("--destination", default=os.path.join(project_directory, "DestinationFolder"),
                    help="Destination folder path (default: DestinationFolder in project directory)")
parser.add_argument("--interval", type=int, default=2, help="Sync interval in seconds (default: 2)")
parser.add_argument("--logfile", default="sync_log.txt", help="Path to log file (default: sync_log.txt)")

args = parser.parse_args()

# Configure logging with the log file path from the command line
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(args.logfile, mode='w'),  # Log to specified file
        logging.StreamHandler()  # Log to console
    ]
)

# Function to copy files from the source folder to the destination folder
def copy_files(source, destination):
    # Create destination folder if it doesn't exist
    if not os.path.exists(destination):
        os.makedirs(destination)

    # Iterate through the source folder items
    for item in os.listdir(source):
        src_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)

        # If the item is a folder, copy it recursively
        if os.path.isdir(src_path):
            if not os.path.exists(dest_path):
                shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
                logging.info(f"Copying folder: {src_path} -> {dest_path}")
        else:
            # If the item is a file, copy it if it's new or has been modified
            if (not os.path.exists(dest_path)) or (os.path.getmtime(src_path) > os.path.getmtime(dest_path)):
                shutil.copy2(src_path, dest_path)
                logging.info(f"Copying file: {src_path} -> {dest_path}")

# Function to remove files from the destination if they have been deleted in the source
def remove_deleted_files(source, destination):
    # Iterate through the destination folder items
    for item in os.listdir(destination):
        dest_path = os.path.join(destination, item)
        src_path = os.path.join(source, item)

        # If the item no longer exists in the source, delete it from the destination
        if not os.path.exists(src_path):
            if os.path.isdir(dest_path):
                shutil.rmtree(dest_path)  # Delete the folder
                logging.info(f"Deleting folder: {dest_path}")
            else:
                os.remove(dest_path)  # Delete the file
                logging.info(f"Deleting file: {dest_path}")

# Function for continuous synchronization with intervals between checks
def continuous_sync(source, destination, interval):
    while True:
        logging.info("Starting file synchronization")
        copy_files(source, destination)
        remove_deleted_files(source, destination)
        logging.info("Synchronization complete")
        sleep(interval)  # Delay between synchronization checks

# Start synchronization with paths and interval from command line arguments
continuous_sync(args.source, args.destination, args.interval)
