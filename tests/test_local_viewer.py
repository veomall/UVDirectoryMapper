import unittest
import os
import tempfile
import shutil
from src.tree_viewers.local_viewer import LocalViewer


class TestLocalViewer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.viewer = LocalViewer()

        # Create a test directory structure
        os.mkdir(os.path.join(self.temp_dir, "dir1"))
        os.mkdir(os.path.join(self.temp_dir, "dir2"))
        open(os.path.join(self.temp_dir, "file1.txt"), "w").close()
        open(os.path.join(self.temp_dir, "dir1", "file2.txt"), "w").close()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_build_tree(self):
        expected_tree = {
            "dir1": {"file2.txt": None},
            "dir2": {},
            "file1.txt": None
        }
        result = self.viewer._build_tree(self.temp_dir)
        self.assertEqual(result, expected_tree)

    def test_view(self):
        temp_dir_name = os.path.basename(self.temp_dir)
        expected_output = (
            f"{temp_dir_name}\n"
            "├── dir1\n"
            "│   └── file2.txt\n"
            "├── dir2\n"
            "└── file1.txt\n"
        )
        result = self.viewer.view(self.temp_dir)
        self.assertEqual(result, expected_output)


if __name__ == "__main__":
    unittest.main()
