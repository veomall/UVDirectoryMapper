import os
from tree_viewers.base_viewer import BaseViewer
from utils.tree_formatter import format_tree


class LocalViewer(BaseViewer):
    def view(self, path):
        tree = self._build_tree(path)
        return format_tree(tree)

    def _build_tree(self, path):
        tree = {}
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                tree[item] = self._build_tree(item_path)
            else:
                tree[item] = None
        return tree