import argparse
from tree_viewers.local_viewer import LocalViewer


def run_cli():
    parser = argparse.ArgumentParser(description="TreeView Console - Directory structure viewer")
    parser.add_argument("path", help="Path to the directory to view")
    args = parser.parse_args()

    viewer = LocalViewer()
    tree = viewer.view(args.path)
    print(tree)
