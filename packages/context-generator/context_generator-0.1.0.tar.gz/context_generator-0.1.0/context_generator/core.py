import os
from pathlib import Path
from typing import List


def build_file_tree(
    directory: str,
    exclude_files: List[str] = [],
    exclude_paths: List[str] = [],
    exclude_hidden: bool = True,
) -> List[str]:
    """
    Build a visual representation of the file tree within the
    specified directory, excluding specified files, paths,
    and optionally hidden files.

    Args:
        directory (str): The root directory to scan.
        exclude_files (List[str], optional): Filenames to exclude
        from the tree.
            Defaults to [].
        exclude_paths (List[str], optional): Directory paths to exclude
        from the tree.
            Defaults to [].
        exclude_hidden (bool, optional): Flag to exclude hidden files
        and directories.
            Defaults to True.

    Returns:
        List[str]: A list of strings representing the file tree structure.
    """
    if exclude_files is None:
        exclude_files = []
    if exclude_paths is None:
        exclude_paths = []

    def traverse(dir_path: str, prefix: str = "") -> List[str]:
        lines: List[str] = []
        try:
            items: List[str] = sorted(os.listdir(dir_path))
        except PermissionError:
            lines.append(f"{prefix}├── [Permission Denied]")
            return lines
        for index, item in enumerate(items):
            item_path: str = os.path.join(dir_path, item)

            if exclude_hidden and item.startswith("."):
                continue

            if item in exclude_files or any(
                exclude in item_path for exclude in exclude_paths
            ):
                continue

            connector: str = "├── " if index < len(items) - 1 else "└── "
            new_prefix: str = "│   " if index < len(items) - 1 else "    "

            if os.path.isdir(item_path):
                lines.append(f"{prefix}{connector}{item}/")
                lines.extend(
                    traverse(
                        item_path,
                        prefix + new_prefix,
                    )
                )
            else:
                lines.append(f"{prefix}{connector}{item}")
        return lines

    return traverse(directory)


def collect_file_contents(
    directory: str,
    exclude_files: List[str] = [],
    exclude_paths: List[str] = [],
    exclude_hidden: bool = True,
) -> List[str]:
    """
    Collect the contents of files within the specified directory,
    excluding specified files, paths, and optionally hidden files.

    Args:
        directory (str): The root directory to scan.
        exclude_files (List[str], optional): Filenames to exclude from
        content collection.
            Defaults to [].
        exclude_paths (List[str], optional): Directory paths to exclude from
        content collection.
            Defaults to [].
        exclude_hidden (bool, optional): Flag to exclude hidden files
        and directories.
            Defaults to True.

    Returns:
        List[str]: A list of strings containing file contents with
        context markers.
    """
    if exclude_files is None:
        exclude_files = []
    if exclude_paths is None:
        exclude_paths = []

    content_lines: List[str] = []
    for root, _, files in os.walk(directory):
        if any(exclude in root for exclude in exclude_paths):
            continue
        if exclude_hidden and any(
            part.startswith(".") for part in Path(root).parts
        ):
            continue

        for file in sorted(files):
            file_path: str = os.path.join(root, file)

            if exclude_hidden and file.startswith("."):
                continue

            if file in exclude_files:
                continue

            relative_path: str = os.path.relpath(file_path, directory)
            relative_path = relative_path.replace(os.sep, "/")

            if file == "__init__.py":
                content_lines.append(f"\n--- Start of {relative_path} ---\n")
                continue

            try:
                file_content: str = Path(file_path).read_text(errors="ignore")
                content_lines.append(f"\n--- Start of {relative_path} ---\n")
                content_lines.append(file_content + "\n")
            except Exception as e:
                content_lines.append(f"\n--- Start of {relative_path} ---\n")
                content_lines.append(f"Error reading file: {e}\n")

    return content_lines


def generate_context(
    directory: str,
    output_file: str,
    exclude_files: List[str] = [],
    exclude_paths: List[str] = [],
    exclude_hidden: bool = True,
) -> str:
    """
    Generate the context by building the file tree and collecting
    file contents,
    then write the combined information to the specified output file.

    Args:
        directory (str): The root directory to scan.
        output_file (str): The output file where context will be saved.
        exclude_files (List[str], optional): Filenames to exclude from
        the context.
            Defaults to [].
        exclude_paths (List[str], optional): Directory paths to exclude
        from the context.
            Defaults to [].
        exclude_hidden (bool, optional): Flag to exclude hidden files
        and directories.
            Defaults to True.

    Returns:
        str: Path to the generated output file.
    """
    if exclude_files is None:
        exclude_files = []
    if exclude_paths is None:
        exclude_paths = []

    # Always exclude the output file dynamically
    if output_file not in exclude_files:
        exclude_files.append(output_file)

    file_tree: List[str] = build_file_tree(
        directory,
        exclude_files,
        exclude_paths,
        exclude_hidden,
    )
    file_contents: List[str] = collect_file_contents(
        directory,
        exclude_files,
        exclude_paths,
        exclude_hidden,
    )

    try:
        with open(
            output_file,
            "w",
            encoding="utf-8",
        ) as f:
            f.write("File Tree:\n")
            f.write("\n".join(file_tree))
            f.write("\n\nFiles:\n")
            f.writelines(file_contents)
    except Exception as e:
        print(f"Failed to write to output file '{output_file}': {e}")
        raise e

    return output_file
