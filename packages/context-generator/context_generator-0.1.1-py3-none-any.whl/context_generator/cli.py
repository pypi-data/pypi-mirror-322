import argparse
import os
import json
import subprocess
from pathlib import Path
from typing import Any, List

from context_generator.core import (
    generate_context,
)

CONFIG_PATH: Path = Path.home() / ".generate_context_config.json"

DEFAULT_CONFIG: dict[str, Any] = {
    "exclude_files": [
        ".env",
        "package-lock.json",
        "LICENSE",
    ],
    "exclude_paths": [
        ".git",
        "__pycache__",
        "build",
    ],  # Removed the empty string
    "output_file": "file_context.txt",
    "exclude_hidden": True,  # New flag
}


def load_config() -> dict[str, Any]:
    """
    Load the JSON configuration file, creating it with default settings
    if it doesn't exist.

    Returns:
        dict[str, Any]: The loaded configuration dictionary.
    """
    if not CONFIG_PATH.exists():
        with open(CONFIG_PATH, "w") as f:
            json.dump(
                DEFAULT_CONFIG,
                f,
                indent=4,
            )
    with open(CONFIG_PATH, "r") as f:
        config: dict[str, Any] = json.load(f)
    return config


def save_config(config: dict[str, Any]) -> None:
    """
    Save the provided configuration dictionary to the JSON configuration file.

    Args:
        config (dict[str, Any]): The configuration settings to save.
    """
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)


def calibrate() -> None:
    """
    Open the JSON configuration file in the default editor.
    If the configuration file does not exist, create it with default settings.
    """
    if not CONFIG_PATH.exists():
        print(
            f"The configuration file does not exist. "
            f"Creating default configuration at {CONFIG_PATH}"
        )
        save_config(DEFAULT_CONFIG)  # Save the default configuration

    print(f"Opening configuration file: {CONFIG_PATH}")
    try:
        if os.name == "nt":  # Windows
            os.startfile(str(CONFIG_PATH))
        elif os.name == "posix":  # macOS or Linux
            subprocess.run(
                [
                    ("open" if os.uname().sysname == "Darwin" else "xdg-open"),
                    str(CONFIG_PATH),
                ],
                check=True,
            )
    except Exception as e:
        print(f"Failed to open the configuration file: {e}")


def main() -> None:
    """
    The main entry point for the CLI tool. Parses command-line arguments
    and executes the appropriate command (generate or calibrate).
    """
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Generate file tree and contents for coding assistance."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Generate subcommand
    generate_parser: argparse.ArgumentParser = subparsers.add_parser(
        "generate",
        help="Generate the context",
    )
    generate_parser.add_argument(
        "directory",
        nargs="?",
        default=os.getcwd(),
        help="The root directory to scan (defaults to the current directory)",
    )
    generate_parser.add_argument(
        "-o",
        "--output",
        help="The output file for the context (overrides configuration)",
    )
    generate_parser.add_argument(
        "--exclude-files",
        nargs="*",
        help="List of filenames to exclude (overrides configuration)",
    )
    generate_parser.add_argument(
        "--exclude-paths",
        nargs="*",
        help="List of paths to exclude (overrides configuration)",
    )

    # Mutually exclusive group for hidden files
    hidden_group = generate_parser.add_mutually_exclusive_group()
    hidden_group.add_argument(
        "--include-hidden",
        action="store_false",
        dest="exclude_hidden",
        default=None,  # Explicitly set default to None
        help="Include hidden files and directories",
    )
    hidden_group.add_argument(
        "--exclude-hidden",
        action="store_true",
        dest="exclude_hidden",
        default=None,  # Explicitly set default to None
        help="Exclude hidden files and directories (default)",
    )

    # Calibrate subcommand
    subparsers.add_parser(
        "calibrate",
        help="Open the configuration file for editing",
    )

    args: argparse.Namespace = parser.parse_args()

    if args.command == "calibrate":
        calibrate()
    elif args.command == "generate":
        # Load configuration
        config: dict[str, Any] = load_config()

        # Merge CLI arguments with configuration
        exclude_files: List[str] = (
            args.exclude_files
            if args.exclude_files is not None
            else config.get("exclude_files", [])
        )
        exclude_paths: List[str] = (
            args.exclude_paths
            if args.exclude_paths is not None
            else config.get("exclude_paths", [])
        )
        output_file: str = (
            args.output
            if args.output
            else config.get(
                "output_file",
                "file_context.txt",
            )
        )

        # Determine exclude_hidden
        if args.exclude_hidden is not None:
            exclude_hidden: bool = args.exclude_hidden
        else:
            exclude_hidden = config.get("exclude_hidden", True)

        # Resolved Exclusions
        print("Resolved Exclusions:")
        print(f"  Exclude Files: {exclude_files}")
        print(f"  Exclude Paths: {exclude_paths}")
        print(f"  Exclude Hidden: {exclude_hidden}")
        print(f"  Output File: {output_file}")

        # Calling generate_context with exclude_hidden
        print(f"Calling generate_context with exclude_hidden={exclude_hidden}")

        # Run the generator with the resolved settings
        generate_context(
            directory=args.directory,
            output_file=output_file,
            exclude_files=exclude_files,
            exclude_paths=exclude_paths,
            exclude_hidden=exclude_hidden,
        )
