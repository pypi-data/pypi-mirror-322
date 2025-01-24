import unittest
from .tree_parser import parse_tree_to_nodes
from .models import TreeNode, TreeFormat

class TestTreeParser(unittest.TestCase):
    def assert_trees_equal(self, actual_nodes, expected_lines, fmt=TreeFormat.DEFAULT):
        actual_tree = TreeNode.list_to_tree_string(actual_nodes, fmt=fmt)
        expected_tree = "\n".join(expected_lines)

        if actual_tree != expected_tree:
            print("\nActual tree:")
            print(actual_tree)
            print("\nExpected tree:")
            print(expected_tree)
            self.assertEqual(actual_tree, expected_tree)


    def test_basic_structure(self):
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
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, input_lines, fmt=TreeFormat.PARSED)

    def test_special_characters(self):
        input_lines = [
            "project/",
            "├── dir_with_safe_chars_!@#$%^&()_+=-/",
            "│   ├── file_with_safe_chars_!@#$%^&()_+=-.txt",
            "│   ├── file_with_unicode_★日本語.md",
            "│   └── file_with_spaces and_parens (test).log"
        ]
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, input_lines, fmt=TreeFormat.PARSED2)

    def test_with_comments(self):
        input_lines = [
            "project/  # Root directory",
            "├── src/  # Source code",
            "│   ├── main.py  # Main application file",
            "│   └── util/  # Utility module",
            "│       └── helper.py  # Helper functions",
            "├── tests/  # Test suite",
            "│   └── test_main.py  # Test for main.py",
            "└── README.md  # Project documentation"
        ]
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, input_lines, fmt=TreeFormat.PARSED)

    def test_empty_directories(self):
        input_lines = [
            "empty_dir/",
            "parent_dir/",
            "└── child_dir/"
        ]
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, input_lines, fmt=TreeFormat.PARSED)

    def test_files_with_spaces(self):
        input_lines = [
            "documents/",
            "├── my report.pdf",
            "└── notes 2023.txt"
        ]
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, input_lines, fmt=TreeFormat.PARSED)

    def test_mixed_depth_entries(self):
        input_lines = [
            "root_file.txt",
            "dir1/",
            "└── subdir1/",
            "    └── subfile.txt",
            "dir2/",
            "file2.txt"
        ]
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, input_lines, fmt=TreeFormat.DEFAULT)

    def test_inconsistent_indentation(self):
        input_lines = [
            "project/",
            "├── src/",
            "│   ├── main.py",
            "│  └── util/",  # Invalid indentation
            "│       └── helper.py",
            "└── README.md"
        ]
        with self.assertRaises(ValueError) as context:
            parse_tree_to_nodes(input_lines)
        self.assertEqual(str(context.exception),
                        "Invalid indentation length in line: │  └── util/")

    def test_deeply_nested(self):
        input_lines = [
            "a/",
            "└── b/",
            "    └── c/",
            "        └── d/",
            "            └── file.txt"
        ]
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, input_lines, fmt=TreeFormat.PARSED)

    def test_multiple_files_same_dir(self):
        input_lines = [
            "dir/",
            "├── file1.txt",
            "├── file2.txt",
            "└── file3.txt"
        ]
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, input_lines, fmt=TreeFormat.PARSED)

    def test_empty_input(self):
        input_lines = []
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, input_lines, fmt=TreeFormat.PARSED)

    def test_empty_input_with_comments(self):
        input_lines = [
            "# This is a comment",
            "",
            "# Another comment",
            "    # Indented comment",
            ""
        ]
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, [], fmt=TreeFormat.PARSED)  # Should parse to empty tree

    def test_comments_within_paths(self):
        input_lines = [
            "project/",
            "├── core/ # Core logic",
            "│   # A comment in middle",
            "│   ├── models/ # Data models",
            "│   │   ├── __init__.py # Init file",
            "│   │   └── user.py",
            "└── README.md # Documentation file"
        ]
        expected_lines = [
            "project/",
            "├── core/  # Core logic",
            "│   ├── models/  # Data models",
            "│   │   ├── __init__.py  # Init file",
            "│   │   └── user.py",
            "└── README.md  # Documentation file"
        ]
        actual_tree = parse_tree_to_nodes(input_lines)
        self.assert_trees_equal(actual_tree, expected_lines, fmt=TreeFormat.PARSED2)
