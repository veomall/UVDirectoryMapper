import os
import zipfile
import tarfile
import rarfile
from src.tree_viewers.local_viewer import LocalViewer
from src.tree_viewers.archive_viewer import ArchiveViewer


def get_viewer_type():
    print("Select viewer type:")
    print("1. Local directory")
    print("2. Archive (ZIP, TAR, RAR)")
    while True:
        choice = input("Enter your choice (1 or 2): ")
        if choice in ['1', '2']:
            return int(choice)
        print("Invalid choice. Please enter 1 or 2.")

def get_path():
    return input("Enter the path to the directory or archive: ")

def is_archive(path):
    return (zipfile.is_zipfile(path) or 
            tarfile.is_tarfile(path) or 
            rarfile.is_rarfile(path))

def run_interactive_cli():
    viewer_type = get_viewer_type()
    path = get_path()

    if viewer_type == 1 and os.path.isdir(path):
        viewer = LocalViewer()
    elif viewer_type == 2 and is_archive(path):
        viewer = ArchiveViewer()
    else:
        print(f"Error: The selected viewer type does not match the provided path.")
        return

    tree = viewer.view(path)
    print(tree)

if __name__ == "__main__":
    run_interactive_cli()
