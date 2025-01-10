import os
from src.tree_viewers.base_viewer import BaseViewer
from src.utils.tree_formatter import format_tree

class LocalViewer(BaseViewer):
    def view(self, path, config):
        tree = self._build_tree(path, config)
        contents = self._get_contents(path, config) if config.show_file_contents else {}
        return format_tree(tree, path, config), contents

    def _build_tree(self, path, config):
        tree = {}
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                tree[item] = self._build_tree(item_path, config)
            elif os.path.isfile(item_path):
                tree[item] = None
        return tree

    def _get_contents(self, path, config):
        contents = {}
        for root, _, files in os.walk(path):
            if any(config.is_excluded(p) for p in root.split(os.sep)):
                continue
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        contents[file_path] = f.read()
                except:
                    contents[file_path] = "[Unable to read file content]"
        return contents
