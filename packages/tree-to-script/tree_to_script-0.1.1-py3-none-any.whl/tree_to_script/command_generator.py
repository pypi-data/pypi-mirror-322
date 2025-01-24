import os
import shlex
from typing import List
from .models import TreeNode

def generate_commands(nodes: List[TreeNode]) -> List[str]:
    """
    Convert tree structure lines into shell commands.

    Args:
        nodes: List of node

    Returns:
        List of shell commands (mkdir, touch) to recreate the structure
    """
    commands = []
    created_dirs = set()

    def traverse(node: TreeNode, current_path: List[str]):
        """
        Recursively traverse the tree and generate commands.

        Args:
            node: Current TreeNode being processed.
            current_path: List of directory names representing the current path.
        """
        # Build the full path for the current node
        full_path = os.path.join(*(current_path + [node.name]))

        if node.is_dir:
            # Directory: create it if not already created
            if full_path not in created_dirs:
                commands.append(f'mkdir -p {shlex.quote(full_path)}')
                created_dirs.add(full_path)

            # Recursively process children
            for child in node.children:
                traverse(child, current_path + [node.name])
        else:
            # File: ensure parent directory exists, then create the file
            parent_dir = os.path.dirname(full_path)
            if parent_dir and parent_dir not in created_dirs:
                commands.append(f'mkdir -p {shlex.quote(parent_dir)}')
                created_dirs.add(parent_dir)

            commands.append(f'touch {shlex.quote(full_path)}')

    # Start traversal from the root nodes
    for node in nodes:
        traverse(node, [])

    return commands
