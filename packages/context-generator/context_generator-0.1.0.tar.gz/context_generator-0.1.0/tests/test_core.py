import os
import tempfile

from context_generator.core import (
    build_file_tree,
    collect_file_contents,
    generate_context,
)


def test_build_file_tree():
    """
    Test the build_file_tree function.

    This test verifies that build_file_tree correctly constructs the file tree,
    excluding specified files, paths, and hidden files.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "dir1", "subdir1"))
        os.makedirs(os.path.join(tmpdir, ".hidden_dir"))
        with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
            f.write("Content of file1")
        with open(os.path.join(tmpdir, ".hidden_file.txt"), "w") as f:
            f.write("Hidden file content")
        with open(os.path.join(tmpdir, "dir1", "file2.txt"), "w") as f:
            f.write("Content of file2")
        with open(
            os.path.join(tmpdir, "dir1", "subdir1", "file3.txt"), "w"
        ) as f:
            f.write("Content of file3")

        file_tree = build_file_tree(
            directory=tmpdir,
            exclude_files=["file1.txt"],
            exclude_paths=["dir1/subdir1"],
            exclude_hidden=True,
        )

        assert "file1.txt" not in file_tree
        assert "subdir1" not in file_tree
        assert ".hidden_dir" not in file_tree
        assert ".hidden_file.txt" not in file_tree


def test_collect_file_contents():
    """
    Test the collect_file_contents function.

    This test ensures that collect_file_contents correctly gathers
    file contents, excluding specified files, paths, and hidden files.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "dir1"))
        with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
            f.write("Content of file1")
        with open(os.path.join(tmpdir, "__init__.py"), "w") as f:
            f.write("# Init file")

        contents = collect_file_contents(
            directory=tmpdir,
            exclude_files=["file1.txt"],
            exclude_paths=["dir1"],
            exclude_hidden=True,
        )

        assert "file1.txt" not in "".join(contents)
        assert "dir1" not in "".join(contents)
        assert "__init__.py" in "".join(contents)


def test_generate_context():
    """
    Test the generate_context function.

    This test verifies that generate_context correctly generates the file tree
    and collects file contents, writing them to the specified output
    file while respecting exclusions.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        os.makedirs(os.path.join(tmpdir, "dir1"))
        with open(os.path.join(tmpdir, "file1.txt"), "w") as f:
            f.write("Content of file1")
        with open(os.path.join(tmpdir, "dir1", "file2.txt"), "w") as f:
            f.write("Content of file2")

        output_file = os.path.join(tmpdir, "output.txt")

        generate_context(
            directory=tmpdir,
            output_file=output_file,
            exclude_files=["file1.txt"],
            exclude_paths=["dir1"],
            exclude_hidden=True,
        )

        with open(output_file, "r") as f:
            content = f.read()

        assert "file1.txt" not in content
        assert "dir1" not in content
        assert "file2.txt" not in content
        assert "output.txt" not in content
        assert "File Tree:" in content
        assert "Files:" in content
