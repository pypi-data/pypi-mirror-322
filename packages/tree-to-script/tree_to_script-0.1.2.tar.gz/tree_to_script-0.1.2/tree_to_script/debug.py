from .models import TreeNode
from typing import List

def print_tree(nodes: List[TreeNode], prefix: str = "", is_last: bool = True):
    """
    Debug helper to print the parsed tree structure in a tree-like format.

    Args:
        nodes: List of TreeNode objects to print.
        prefix: Prefix string for indentation and connectors.
        is_last: Whether the current node is the last child of its parent.

    Example output:
        └── TreeNode(name='project', is_dir=True, depth=0)  # Root directory
            ├── TreeNode(name='src', is_dir=True, depth=1)  # Source code
            │   ├── TreeNode(name='main.py', is_dir=False, depth=2)  # Entry point
            │   └── TreeNode(name='util', is_dir=True, depth=2)  # Utility functions
            │       └── TreeNode(name='helper.py', is_dir=False, depth=3)  # Helper functions
            ├── TreeNode(name='tests', is_dir=True, depth=1)  # Test suite
            │   └── TreeNode(name='test_main.py', is_dir=False, depth=2)  # Test for main.py
            └── TreeNode(name='README.md', is_dir=False, depth=1)  # Project documentation

    Notes:
        - Comments associated with TreeNode objects are displayed after the node representation.
        - The tree structure is printed with proper connectors (├──, └──) and indentation.
    """
    for i, node in enumerate(nodes):
        # Determine the connector and new prefix
        connector = "└── " if i == len(nodes) - 1 else "├── "
        node_repr = f"TreeNode(name={node.name!r}, is_dir={node.is_dir}, depth={node.depth})"
        if node.comment:
            node_repr += f"  # {node.comment}"
        print(f"{prefix}{connector}{node_repr}")

        # Update the prefix for children
        new_prefix = prefix + ("    " if i == len(nodes) - 1 else "│   ")

        # Recursively print children
        if node.children:
            print_tree(node.children, new_prefix, i == len(nodes) - 1)
