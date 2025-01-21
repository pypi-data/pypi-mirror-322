# Context Generator

![PyPI](https://img.shields.io/pypi/v/context-generator)
![Python Versions](https://img.shields.io/pypi/pyversions/context-generator)
![License](https://img.shields.io/pypi/l/context-generator)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Generating Context](#generating-context)
  - [Calibrating Configuration](#calibrating-configuration)
- [Configuration](#configuration)
- [Examples](#examples)
- [Integration with VSCode](#integration-with-vscode)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

**Context Generator** is a Python CLI tool designed to generate a comprehensive file tree and collect file contents from your project. This tool is used to give a comprehensive context of your project to an LLM for improved responses.

for an example of the output please look in the img dir

## Features

- **File Tree Generation:** Visual representation of your project's directory structure.
- **Content Collection:** Aggregates contents of selected files for easy reference.
- **Exclusion Options:** Customize which files or directories to exclude from the context.
- **Hidden Files Handling:** Option to include or exclude hidden files and directories.
- **Configuration Management:** Easily configure default settings through a JSON file.
- **VSCode Integration:** Seamlessly integrate with Visual Studio Code via a dedicated extension (planned).
- **Cross-Platform Support:** Works on Windows, macOS, and Linux.

## Installation

### Prerequisites

- **Python 3.7+**: Ensure you have Python installed. You can download it from [python.org](https://www.python.org/downloads/).

### Install via PyPI

```bash
pip install context-generator
```

## Usage

### Generating Context

To generate a file tree and collect contents:

```bash
generate-context generate <directory> --output <output_file>
```

**Options:**
- `directory`: The root directory to scan. Defaults to the current working directory.
- `--output`: Specify the output file for the generated context.
- `--exclude-files`: List filenames to exclude from the context.
- `--exclude-paths`: List directory paths to exclude from the context.
- `--include-hidden`: Include hidden files and directories in the output.

### Example

Generate a context file for your project:

```bash
generate-context generate . --output context.txt --exclude-files .env --exclude-paths .git
```

### Calibrating Configuration

To edit the default configuration file:

```bash
generate-context calibrate
```

This opens the configuration file located at `~/.generate_context_config.json` in your default editor. Adjust the settings as needed.

## Configuration

The configuration file is stored at `~/.generate_context_config.json`. Below is an example configuration:

```json
{
  "exclude_files": [".env", "package-lock.json", "LICENSE"],
  "exclude_paths": [".git", "__pycache__"],
  "output_file": "file_context.txt",
  "exclude_hidden": true
}
```

**Fields:**
- `exclude_files`: Files to exclude from the context generation.
- `exclude_paths`: Directories to exclude.
- `output_file`: Default output file name.
- `exclude_hidden`: Whether to exclude hidden files and directories.

## Examples

1. **Basic File Tree Generation:**

   ```bash
   generate-context generate .
   ```

2. **Excluding Specific Files and Directories:**

   ```bash
   generate-context generate ./src --exclude-files .env --exclude-paths .git
   ```

3. **Including Hidden Files:**

   ```bash
   generate-context generate ./ --include-hidden
   ```

## Integration with VSCode

- Planned integration with Visual Studio Code to provide an extension for generating context directly from the editor.

## Contributing

We welcome contributions! Feel free to submit issues and pull requests on [GitHub](https://github.com/aldo-g/context-generator).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, reach out to **Alastair Grant** at [aldo.e.george@gmail.com](mailto:aldo.e.george@gmail.com).

