import sys
import tempfile
from pathlib import Path
from unittest import mock

import pytest
from context_generator.cli import calibrate, load_config, save_config, main


@pytest.mark.skipif(sys.platform != "win32", reason="Windows-only test")
@mock.patch("context_generator.cli.os.startfile")
@mock.patch("context_generator.cli.subprocess.run")
def test_calibrate_windows(mock_subprocess_run, mock_startfile):
    """
    Test the calibrate function on Windows systems.

    This test ensures that the calibrate function calls 'os.startfile' with the
    correct configuration file path and does not call 'subprocess.run'.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".generate_context_config.json"
        with mock.patch("context_generator.cli.CONFIG_PATH", config_path):
            with open(config_path, "w") as f:
                f.write("{}")

            calibrate()
            mock_startfile.assert_called_once_with(str(config_path))
            mock_subprocess_run.assert_not_called()


@mock.patch("context_generator.cli.subprocess.run")
@mock.patch("context_generator.cli.os.uname")
def test_calibrate_posix_mac(mock_uname, mock_subprocess_run):
    """
    Test the calibrate function on macOS systems.

    This test verifies that the calibrate function correctly calls 'open'
    with the configuration file path on macOS systems.
    """
    mock_uname.return_value = mock.Mock(sysname="Darwin")
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".generate_context_config.json"
        with mock.patch("context_generator.cli.CONFIG_PATH", config_path):
            with open(config_path, "w") as f:
                f.write("{}")

            calibrate()
            mock_subprocess_run.assert_called_once_with(
                ["open", str(config_path)], check=True
            )


@mock.patch("context_generator.cli.subprocess.run")
@mock.patch("context_generator.cli.os.uname")
def test_calibrate_posix_linux(mock_uname, mock_subprocess_run):
    """
    Test the calibrate function on Linux systems.

    This test ensures that the calibrate function calls 'xdg-open' with the
    correct configuration file path on Linux systems.
    """
    mock_uname.return_value = mock.Mock(sysname="Linux")
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".generate_context_config.json"
        with mock.patch("context_generator.cli.CONFIG_PATH", config_path):
            with open(config_path, "w") as f:
                f.write("{}")

            calibrate()
            mock_subprocess_run.assert_called_once_with(
                ["xdg-open", str(config_path)], check=True
            )


def test_load_config_creates_default_if_not_exists():
    """
    Test that load_config creates a default configuration file if it
    does not exist.

    This test verifies that load_config returns the DEFAULT_CONFIG
    when the configuration file is absent and that the file is
    created on disk.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".generate_context_config.json"
        with mock.patch("context_generator.cli.CONFIG_PATH", config_path):
            config = load_config()
            assert config == {
                "exclude_files": [".env", "package-lock.json", "LICENSE"],
                "exclude_paths": [".git", "__pycache__", "build"],
                "output_file": "file_context.txt",
                "exclude_hidden": True,
            }
            assert config_path.exists()


def test_save_config():
    """
    Test that save_config correctly saves the provided configuration to a file.

    This test ensures that the configuration saved by save_config matches the
    input dictionary and can be loaded accurately.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".generate_context_config.json"
        new_config = {
            "exclude_files": ["test.env"],
            "exclude_paths": ["tests"],
            "output_file": "test_context.txt",
            "exclude_hidden": False,
        }
        with mock.patch("context_generator.cli.CONFIG_PATH", config_path):
            save_config(new_config)
            loaded_config = load_config()
            assert loaded_config == new_config


def test_main_generate_context(capsys):
    """
    Test the main function's generate command.

    This test verifies that the generate command correctly processes
    CLI arguments,merges them with the configuration, and calls
    generate_context with the resolved settings.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".generate_context_config.json"
        with mock.patch("context_generator.cli.CONFIG_PATH", config_path):
            config = {
                "exclude_files": [".env"],
                "exclude_paths": [".git"],
                "output_file": "file_context.txt",
                "exclude_hidden": True,
            }
            save_config(config)

            with mock.patch(
                "context_generator.cli.generate_context",
                return_value="file_context.txt",
            ) as mock_generate:
                test_args = [
                    "generate-context",
                    "generate",
                    "some_directory",
                    "--output",
                    "output.txt",
                    "--exclude-files",
                    "test.py",
                ]
                with mock.patch("sys.argv", test_args):
                    main()

                mock_generate.assert_called_once_with(
                    directory="some_directory",
                    output_file="output.txt",
                    exclude_files=["test.py"],
                    exclude_paths=[".git"],
                    exclude_hidden=True,
                )

                captured = capsys.readouterr()
                assert "Resolved Exclusions:" in captured.out
                assert "Exclude Files: ['test.py']" in captured.out
                assert "Exclude Paths: ['.git']" in captured.out
                assert "Exclude Hidden: True" in captured.out
                assert "Output File: output.txt" in captured.out
                assert (
                    "Calling generate_context with exclude_hidden=True"
                    in captured.out
                )


def test_main_calibrate(capsys):
    """
    Test the main function's calibrate command.

    This test ensures that the calibrate command invokes the calibrate
    function correctly.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        config_path = Path(tmpdir) / ".generate_context_config.json"
        with mock.patch("context_generator.cli.CONFIG_PATH", config_path):
            test_args = ["generate-context", "calibrate"]
            with mock.patch("sys.argv", test_args):
                with mock.patch(
                    "context_generator.cli.calibrate"
                ) as mock_calibrate:
                    main()
                    mock_calibrate.assert_called_once()
