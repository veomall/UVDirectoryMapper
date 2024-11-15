import zipfile
import tarfile
import rarfile
from src.tree_viewers.base_viewer import BaseViewer
from src.utils.tree_formatter import format_tree


class ArchiveViewer(BaseViewer):
    def view(self, path):
        tree = self._build_tree(path)
        return format_tree(tree, path)

    def _build_tree(self, path):
        if zipfile.is_zipfile(path):
            return self._build_zip_tree(path)
        elif tarfile.is_tarfile(path):
            return self._build_tar_tree(path)
        elif rarfile.is_rarfile(path):
            return self._build_rar_tree(path)
        else:
            raise ValueError("Unsupported archive format")

    def _build_zip_tree(self, path):
        tree = {}
        with zipfile.ZipFile(path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                self._add_to_tree(tree, file.split('/'))
        return tree

    def _build_tar_tree(self, path):
        tree = {}
        with tarfile.open(path, 'r:*') as tar_ref:
            for member in tar_ref.getmembers():
                self._add_to_tree(tree, member.name.split('/'))
        return tree

    def _build_rar_tree(self, path):
        tree = {}
        with rarfile.RarFile(path) as rar_ref:
            for file in rar_ref.namelist():
                self._add_to_tree(tree, file.split('/'))
        return tree

    def _add_to_tree(self, tree, parts):
        for part in parts[:-1]:
            tree = tree.setdefault(part, {})
        if parts[-1]:  # Ignore empty names (directory entries)
            tree[parts[-1]] = None
