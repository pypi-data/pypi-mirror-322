import re
from typing import List, Tuple, Optional
from .models import TreeNode

def parse_tree_line(line: str) -> Optional[Tuple[int, str, bool, Optional[str]]]:
    """
    Parse a single line from a tree structure format.

    Args:
        line: A string representing a line from tree output

    Returns:
        Tuple of (depth: int, name: str, is_dir: bool, comment: Optional[str])

    Raises:
        ValueError: If the line has invalid format or indentation
    """
    # Strip connectors (├──, └──, │) and leading/trailing whitespace
    stripped_line = re.sub(r'^[│ ]*(├──|└──)?\s*', '', line).strip()

    # Skip standalone comment lines (after stripping connectors and indentation)
    if stripped_line.startswith('#'):
        return None

    # Match indentation, connector, name, and optional comment (requires a space before #)
    match = re.match(r'^([│ ]*)(├──|└──)?\s*(.*?)(?:\s+#(.*))?$', line)
    if not match:
        name = line.strip()
        return 0, name, name.endswith('/'), None

    indentation, connector, name, comment = match.groups()
    # print((indentation, connector, name, comment))

    # Validate indentation format
    if indentation and not all(c in '│ ' for c in indentation):
        raise ValueError(f"Invalid indentation characters in line: {line}")

    # Calculate depth based on indentation length
    indentation_length = len(indentation)
    if indentation_length % 4 != 0:
        raise ValueError(f"Invalid indentation length in line: {line}")

    depth = indentation_length // 4

    # If there's a connector, this line is a child of the previous depth
    if connector:
        depth += 1

    name = name.strip()
    is_dir = name.endswith('/')

    # Clean up comment (remove leading '# ' if present)
    if comment:
        comment = comment.strip().lstrip('#').strip()

    return depth, name.rstrip('/') if is_dir else name, is_dir, comment


def parse_tree_to_nodes(tree_lines: List[str]) -> List[TreeNode]:
    """
    Convert tree structure lines into a list of TreeNode objects.

    Args:
        tree_lines: List of strings in tree format

    Returns:
        List of TreeNode objects representing the tree structure
    """
    nodes: List[TreeNode] = []
    stack: List[TreeNode] = []

    for line in tree_lines:
        line = line.rstrip('\n')
        if not line or line.strip().startswith('#'):
            # Skip empty lines and comments
            continue

        parsed = parse_tree_line(line)
        if parsed is None:
            # Skip standalone comments
            continue

        depth, name, is_dir, comment = parsed

        # Skip nodes with empty names (invalid entries)
        if not name:
            continue

        node = TreeNode(name=name, is_dir=is_dir, depth=depth, comment=comment)

        # Clear stack until we find the parent
        while stack and stack[-1].depth >= depth:
            stack.pop()

        if stack:
            # Add as child to parent
            stack[-1].children.append(node)
        else:
            # Root level node
            nodes.append(node)

        if is_dir:
            stack.append(node)

    return nodes


def validate_tree_structure(nodes: List[TreeNode]) -> bool:
    """
    Validate the tree structure for consistency.

    Rules:
    1. Child nodes must have depth = parent depth + 1
    2. Sibling nodes must have the same depth
    3. All nodes under a parent must be properly nested
    """
    def validate_node_and_children(node: TreeNode, expected_depth: int) -> bool:
        if node.depth != expected_depth:
            return False

        if node.children:
            child_depth = expected_depth + 1
            # All children should have depth = parent_depth + 1
            return all(validate_node_and_children(child, child_depth)
                        for child in node.children)
        return True

    # For root level nodes
    prev_depth = None
    for node in nodes:
        # Check if root level nodes have consistent depth
        if prev_depth is not None and node.depth != prev_depth:
            return False
        prev_depth = node.depth

        # Validate each node and its children
        if not validate_node_and_children(node, node.depth):
            return False

    return True


def parse_and_validate_tree(tree_lines: List[str]) -> List[TreeNode]:
    """Parse tree lines and validate the resulting structure."""
    nodes = parse_tree_to_nodes(tree_lines)
    if not validate_tree_structure(nodes):
        raise ValueError("Invalid tree structure")
    return nodes
