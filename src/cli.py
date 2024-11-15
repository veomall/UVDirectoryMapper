import os
import zipfile
import tarfile
import rarfile
from src.tree_viewers.local_viewer import LocalViewer
from src.tree_viewers.archive_viewer import ArchiveViewer
from src.tree_viewers.github_viewer import GitHubViewer
from src.config import Config


def get_viewer_type():
    print("Select viewer type:")
    print("1. Local directory")
    print("2. Archive (ZIP, TAR, RAR)")
    print("3. GitHub repository")
    while True:
        choice = input("Enter your choice (1, 2 or 3): ")
        if choice in ('1', '2', '3'):
            return int(choice)
        print("Invalid choice. Please enter 1, 2 or 3.")

def get_path():
    return input("Enter the path to the directory, archive or GitHub repository URL: ")

def is_archive(path):
    return (zipfile.is_zipfile(path) or 
            tarfile.is_tarfile(path) or 
            rarfile.is_rarfile(path))

def is_github_url(url):
    return url.startswith("https://github.com/") and url.count('/') >= 4

def manage_exclusions(config):
    while True:
        print("\nExclusion Management:")
        print("1. Add exclusion")
        print("2. Remove exclusion")
        print("3. View current exclusions")
        print("4. Done")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            folder = input("Enter folder name to exclude: ").strip()
            config.add_excluded_folder(folder)
            print(f"Added '{folder}' to exclusions.")
        elif choice == '2':
            folder = input("Enter folder name to remove from exclusions: ").strip()
            config.remove_excluded_folder(folder)
            print(f"Removed '{folder}' from exclusions.")
        elif choice == '3':
            print("Current exclusions:")
            for folder in config.excluded_folders:
                print(f"- {folder}")
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

def run_interactive_cli():
    config = Config()
    viewer_type = get_viewer_type()
    path = get_path()

    print("Would you like to manage folder exclusions?")
    if input("Enter 'y' for yes, any other key for no: ").lower() == 'y':
        manage_exclusions(config)

    if viewer_type == 1 and os.path.isdir(path):
        viewer = LocalViewer()
    elif viewer_type == 2 and is_archive(path):
        viewer = ArchiveViewer()
    elif viewer_type == 3 and is_github_url(path):
        viewer = GitHubViewer()
    else:
        print(f"Error: The selected viewer type does not match the provided path.")
        return

    try:
        tree = viewer.view(path, config)
        print(tree)
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    run_interactive_cli()
