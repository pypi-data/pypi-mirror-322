#!/usr/bin/env python3
import sys
import subprocess
import argparse
from typing import List, Optional
from .serializers import BashArraySerializer, YamlSerializer, CommandSerializer
from .tree_parser import parse_tree_to_nodes, validate_tree_structure
from .command_generator import generate_commands

def generate_commands_from_tree(tree_lines: List[str]) -> List[str]:
    """
    Convert tree structure lines into shell commands.

    Args:
        tree_lines: List of strings in tree format

    Returns:
        List of shell commands (mkdir, touch) to recreate the structure
    """
    # Filter out comments and empty lines
    tree_lines = [line.strip() for line in tree_lines if line.strip() and not line.strip().startswith('#')]

    # Parse the tree structure first
    nodes = parse_tree_to_nodes(tree_lines)

    # Validate tree structure
    if not validate_tree_structure(nodes):
        raise ValueError("Invalid tree structure")

    commands = generate_commands(nodes)
    return commands

def tree_to_commands(tree_input: Optional[str] = None, serializer: CommandSerializer = BashArraySerializer(), dry_run=True) -> None:
    """
    Read tree structure from a file or stdin and output serialized commands.

    Args:
        tree_input: Path to file containing tree structure or None to read from stdin.
        serializer: Serializer instance to format output.
        dry_run: If True, only print commands. If False, execute them.
    """
    if tree_input:
        # Read from file
        with open(tree_input, 'r') as f:
            lines = f.readlines()
    else:
        # Read from stdin
        lines = sys.stdin.readlines()

    commands = generate_commands_from_tree(lines)

    if dry_run:
        print(serializer.serialize(commands))
    else:
        run_commands(commands)

def run_commands(commands: List[str], cwd: str | None = None) -> None:
    """
    Execute a list of shell commands in the specified working directory.

    Args:
        commands: List of shell commands to execute.
        cwd: Working directory where commands will be executed (default: current directory).
              This must be a string (not a Path object).
    """
    for cmd in commands:
        subprocess.run(cmd, shell=True, cwd=str(cwd) if cwd else None, check=True)

def main():
    parser = argparse.ArgumentParser(description="Transform directory tree structures into shell commands.")
    parser.add_argument('tree_file', nargs='?', help="Path to file containing tree structure. Reads from stdin if not provided.")
    parser.add_argument('--no-dry', action='store_false', dest='dry_run', help="Execute commands directly instead of printing them.")
    parser.add_argument('--serializer', choices=['bash', 'yaml'], default='bash', help="Output format for commands.")

    args = parser.parse_args()

    # Choose serializer based on the argument
    if args.serializer == 'yaml':
        serializer = YamlSerializer()
    else:
        serializer = BashArraySerializer()

    tree_to_commands(args.tree_file, serializer=serializer, dry_run=args.dry_run)

if __name__ == '__main__':
    main()
