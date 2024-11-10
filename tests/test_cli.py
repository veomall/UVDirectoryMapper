import unittest
import sys
from io import StringIO
from unittest.mock import patch
from src.cli import run_cli

class TestCLI(unittest.TestCase):
    @patch('sys.stdout', new_callable=StringIO)
    def test_run_cli(self, mock_stdout):
        # Create a mock directory structure
        mock_tree = {
            "dir1": {"file2.txt": None},
            "dir2": {},
            "file1.txt": None
        }
        
        expected_output = (
            ".\n"
            "├── dir1\n"
            "│   └── file2.txt\n"
            "├── dir2\n"
            "└── file1.txt\n"
        )

        with patch('src.tree_viewers.local_viewer.LocalViewer.view', return_value=expected_output):
            with patch('sys.argv', ['mapper.py', '/mock/path']):
                run_cli()

        self.assertEqual(mock_stdout.getvalue().strip(), expected_output.strip())

if __name__ == "__main__":
    unittest.main()