from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class TreeFormat(Enum):
    DEFAULT = "default"  # Standard tree output with ├── format
    PARSED = "parsed"    # Output showing exact parse structure with indentation
    PARSED2 = "parsed2"    # Output showing exact parse structure with indentation


@dataclass
class TreeNode:
    """
    Represents a node in the file tree structure.

    Attributes:
        name (str): The name of the file or directory.
        is_dir (bool): True if the node represents a directory, False for a file.
        depth (int): The depth of the node in the tree hierarchy (0 for root).
        children (List[TreeNode]): List of child nodes (defaults to an empty list).
        comment (Optional[str]): An optional comment associated with the node (defaults to None).
    """
    name: str
    is_dir: bool
    depth: int
    children: List['TreeNode'] = None
    comment: Optional[str] = None

    def __post_init__(self):
        if self.children is None:
            self.children = []

    # def to_tree_string(self, prefix: str = "", is_last: bool = True, fmt: TreeFormat = TreeFormat.DEFAULT) -> str:
    #     """
    #     Convert node and its children to tree format string.

    #     Args:
    #         prefix: Current line prefix for proper indentation
    #         is_last: Whether this node is the last child of its parent
    #         fmt: Output format (DEFAULT or PARSED)

    #     Returns:
    #         String representation in tree format
    #     """
    #     result = ""

    #     if fmt == TreeFormat.DEFAULT:
    #         # Standard tree format
    #         if self.depth == 0:
    #             result = f"{self.name}"
    #         else:
    #             connector = "└── " if is_last else "├── "
    #             result = f"{prefix}{connector}{self.name}"
    #     else:
    #         # Parsed format (showing exact parse structure)
    #         result = f"{prefix}{self.name}"

    #     if self.is_dir:
    #         result += "/"

    #     if self.comment:
    #         result += f"  # {self.comment}"
    #     result += "\n"

    #     if self.children:
    #         for i, child in enumerate(self.children):
    #             is_last_child = i == len(self.children) - 1

    #             if fmt == TreeFormat.DEFAULT:
    #                 if self.depth == 0:
    #                     child_prefix = "│   " if not is_last_child else "    "
    #                 else:
    #                     child_prefix = prefix + ("    " if is_last else "│   ")
    #             else:
    #                 child_prefix = prefix + "│   "

    #             result += child.to_tree_string(
    #                 child_prefix,
    #                 is_last=is_last_child,
    #                 fmt=fmt
    #             )

    #     return result

    def to_tree_string(self, prefix: str = "", is_last: bool = True, fmt: TreeFormat = TreeFormat.DEFAULT) -> str:
        result = ""

        # Handle root node
        if self.depth == 0:
            result = f"{self.name}"
            if self.is_dir:
                result += "/"
            if self.comment:
                result += f"  # {self.comment}"
            result += "\n"
        else:
            # Non-root nodes
            if fmt == TreeFormat.DEFAULT:
                # Tree connector format
                connector = "└── " if is_last else "├── "
                result = f"{prefix}{connector}{self.name}"
            elif fmt == TreeFormat.PARSED:
                # Parser format
                connector = "└── " if is_last else "├── "
                result = f"{prefix}{connector}{self.name}"
            else:
                # Parser format
                connector = "└── " if (is_last and not self.children) else "├── "
                result = f"{prefix}{connector}{self.name}"

            if self.is_dir:
                result += "/"
            if self.comment:
                result += f"  # {self.comment}"
            result += "\n"

        # Handle children
        if self.children:
            for i, child in enumerate(self.children):
                is_last_child = i == len(self.children) - 1

                # Calculate child prefix
                if fmt == TreeFormat.DEFAULT:
                    if self.depth == 0:
                        child_prefix = "    " if not is_last_child else "    "
                    if self.depth > 1:
                        child_prefix = prefix + ("    " if is_last else "3   ")
                    else:
                        child_prefix = prefix + ("    " if is_last else "")
                elif fmt == TreeFormat.PARSED:
                    # Parser format (indentation)
                    child_prefix = prefix + ("" if is_last and self.depth < 1 else ("    " if is_last else "│   "))
                else:
                    # Parser format (indentation)
                    child_prefix = prefix + ("" if is_last and self.depth < 1 else ("│   " if is_last else "│   "))

                result += child.to_tree_string(
                    child_prefix,
                    is_last=is_last_child,
                    fmt=fmt
                )

        return result

    @classmethod
    def list_to_tree_string(cls, nodes: List['TreeNode'], fmt: TreeFormat = TreeFormat.DEFAULT) -> str:
        """
        Convert list of nodes to tree format string.

        Args:
            nodes: List of TreeNode objects

        Returns:
            Complete tree structure as string
        """
        result = ""
        for i, node in enumerate(nodes):
            result += node.to_tree_string(is_last=(i == len(nodes) - 1), fmt=fmt)
        return result.rstrip()

        # result = ""
        # for i, node in enumerate(nodes):
        #     if node.depth == 0:
        #         # Root nodes get no prefix
        #         result += node.to_tree_string(is_last=(i == len(nodes) - 1))
        #     else:
        #         # Non-root nodes get tree connectors
        #         connector = "└── " if i == len(nodes) - 1 else "├── "
        #         result += connector + node.to_tree_string(is_last=(i == len(nodes) - 1))
        # return result.rstrip()
