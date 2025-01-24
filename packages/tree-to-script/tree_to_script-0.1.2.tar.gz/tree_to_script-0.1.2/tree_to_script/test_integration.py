import unittest
import tempfile
from pathlib import Path
from .main import generate_commands_from_tree, run_commands

class TestIntegration(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.TemporaryDirectory()
        self.test_path = Path(self.test_dir.name)

    def tearDown(self):
        # Clean up the temporary directory
        self.test_dir.cleanup()

    def assert_structure_exists(self, expected_structure):
        """Helper function to verify that the directory structure matches expectations."""
        for path in expected_structure:
            full_path = self.test_path / path
            self.assertTrue(full_path.exists(), f"Expected path {path} does not exist")

    def test_basic_structure(self):
        """Test a basic directory structure with files and directories."""
        input_lines = [
            "project/",
            "├── src/",
            "│   ├── main.py",
            "│   └── util/",
            "│       └── helper.py",
            "├── tests/",
            "│   └── test_main.py",
            "└── README.md"
        ]

        # Generate commands
        commands = generate_commands_from_tree(input_lines)

        # Run commands in the temporary directory
        run_commands(commands, cwd=str(self.test_path))  # Convert Path to string

        # Verify the structure
        expected_structure = [
            "project",
            "project/src",
            "project/src/main.py",
            "project/src/util",
            "project/src/util/helper.py",
            "project/tests",
            "project/tests/test_main.py",
            "project/README.md"
        ]
        self.assert_structure_exists(expected_structure)

    def test_special_characters(self):
        """Test handling of filenames with special characters and spaces."""
        input_lines = [
            "documents/",
            "├── my report.pdf",
            "└── notes 2023.txt"
        ]

        # Generate commands
        commands = generate_commands_from_tree(input_lines)

        # Run commands in the temporary directory
        run_commands(commands, cwd=str(self.test_path))  # Convert Path to string

        # Verify the structure
        expected_structure = [
            "documents",
            "documents/my report.pdf",
            "documents/notes 2023.txt"
        ]
        self.assert_structure_exists(expected_structure)

    def test_deeply_nested_structure(self):
        """Test a deeply nested directory structure."""
        input_lines = [
            "a/",
            "└── b/",
            "    └── c/",
            "        └── d/",
            "            └── file.txt"
        ]

        # Generate commands
        commands = generate_commands_from_tree(input_lines)

        # Run commands in the temporary directory
        run_commands(commands, cwd=str(self.test_path))  # Convert Path to string

        # Verify the structure
        expected_structure = [
            "a",
            "a/b",
            "a/b/c",
            "a/b/c/d",
            "a/b/c/d/file.txt"
        ]
        self.assert_structure_exists(expected_structure)

    def test_empty_directories(self):
        """Test creation of empty directories."""
        input_lines = [
            "empty_dir/",
            "parent_dir/",
            "└── child_dir/"
        ]

        # Generate commands
        commands = generate_commands_from_tree(input_lines)

        # Run commands in the temporary directory
        run_commands(commands, cwd=str(self.test_path))  # Convert Path to string

        # Verify the structure
        expected_structure = [
            "empty_dir",
            "parent_dir",
            "parent_dir/child_dir"
        ]
        self.assert_structure_exists(expected_structure)

    def test_mixed_depth_entries(self):
        """Test mixed depth entries (files and directories at different levels)."""
        input_lines = [
            "root_file.txt",
            "dir1/",
            "└── subdir1/",
            "    └── subfile.txt",
            "dir2/",
            "file2.txt"
        ]

        # Generate commands
        commands = generate_commands_from_tree(input_lines)

        # Run commands in the temporary directory
        run_commands(commands, cwd=str(self.test_path))  # Convert Path to string

        # Verify the structure
        expected_structure = [
            "root_file.txt",
            "dir1",
            "dir1/subdir1",
            "dir1/subdir1/subfile.txt",
            "dir2",
            "file2.txt"
        ]
        self.assert_structure_exists(expected_structure)

    def test_comments_in_input(self):
        """Test that comments in the input are ignored."""
        input_lines = [
            "project/  # Root directory",
            "├── src/  # Source code",
            "│   ├── main.py  # Main application file",
            "│   └── util/  # Utility module",
            "│       └── helper.py  # Helper functions",
            "└── README.md  # Project documentation"
        ]

        # Generate commands
        commands = generate_commands_from_tree(input_lines)

        # Run commands in the temporary directory
        run_commands(commands, cwd=str(self.test_path))  # Convert Path to string

        # Verify the structure
        expected_structure = [
            "project",
            "project/src",
            "project/src/main.py",
            "project/src/util",
            "project/src/util/helper.py",
            "project/README.md"
        ]
        self.assert_structure_exists(expected_structure)

    def test_invalid_structure_raises_error(self):
        """Test that invalid tree structures raise an error."""
        input_lines = [
            "project/",
            "├── src/",
            "│  └── util/",  # Invalid indentation
            "│       └── helper.py",
            "└── README.md"
        ]

        # Ensure a ValueError is raised
        with self.assertRaises(ValueError):
            generate_commands_from_tree(input_lines)

    def test_empty_input(self):
        """Test that empty input generates no commands."""
        input_lines = []

        # Generate commands
        commands = generate_commands_from_tree(input_lines)

        # Verify no commands are generated
        self.assertEqual(commands, [])

if __name__ == '__main__':
    unittest.main()
