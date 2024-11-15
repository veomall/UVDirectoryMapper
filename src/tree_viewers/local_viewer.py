import os
from src.tree_viewers.base_viewer import BaseViewer
from src.utils.tree_formatter import format_tree


class LocalViewer(BaseViewer):
    def view(self, path, config):
        tree = self._build_tree(path, config)
        return format_tree(tree, path, config)

    def _build_tree(self, path, config):
        tree = {}
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                tree[item] = self._build_tree(item_path, config)
            elif os.path.isfile(item_path):
                tree[item] = None
        return tree
