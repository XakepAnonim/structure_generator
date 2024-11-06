import os
import toml
import re
from typing import Set, Tuple, Dict, Optional, TypeVar

T = TypeVar('T', bound=str)
U = TypeVar('U', bound=Dict[str, object])

DEFAULT_EXCLUDED_ITEMS: Set[str] = {
    'venv',
    '__pycache__',
    '.git',
    '.env',
    '.venv',
    '.idea',
    '.vscode',
    '.DS_Store',
    '.gitignore',
    'migrations',
    'db.sqlite3',
    '.log',
    '.jar',
    'node_modules',
    'dist',
}  # Default excluded items


def load_config(
    project_root: str,
    config_files: Tuple[str, ...] = ("structure.toml", "pyproject.toml")
) -> U:
    """
    Attempts to load configuration from multiple possible TOML files.

    This function looks for configuration files in the specified
    `config_files` list. If the file exists, it loads its contents
    and merges the relevant configuration options into a dictionary.

    Args:
        project_root (str): The root directory of the project where config files are located.
        config_files (tuple of str): List of possible configuration file names (default: "structure.toml", "pyproject.toml").

    Returns:
        dict: A dictionary containing the merged configuration options.
            The dictionary has the following keys:
            - 'exclude' (Set[str]): A set of directory names to exclude from processing.
            - 'read_docstrings' (bool): Whether to read Python docstrings (default: True).
            - 'output_file' (str): The file to which the project structure should be written (default: "README.md").
    """

    config: U = {
        'exclude': set(),
        'read_docstrings': True,  # default
        'output_file': "README.md"  # default
    }

    for config_file_name in config_files:
        config_path = os.path.join(project_root, config_file_name)
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as file:
                config_data = toml.load(file)

                # If it's pyproject.toml, look in the [tool.structure_generator] section
                if config_file_name.endswith("pyproject.toml"):
                    tool_config = config_data.get(
                        'tool', {}
                    ).get('structure_generator', {})
                    if tool_config:
                        config['exclude'] = set(tool_config.get('exclude', []))
                        config['read_docstrings'] = tool_config.get(
                            'read_docstrings', True
                        )
                        config['output_file'] = tool_config.get(
                            'output_file', "README.md"
                        )
                else:
                    config['exclude'] = set(config_data.get('exclude', []))
                    config['read_docstrings'] = config_data.get('read_docstrings', True)
                    config['output_file'] = config_data.get('output_file', "README.md")
            break
    return config


def extract_docstring(file_path: str) -> Optional[str]:
    """
    Extracts the docstring from a Python file, if present.

    This function reads the content of the specified Python file and uses a regular
    expression to extract the first docstring found in the file. It returns the
    docstring as a string or `None` if no docstring is present.

    Args:
        file_path (str): The path to the Python file from which the docstring should be extracted.

    Returns:
        Optional[str]: The extracted docstring, or `None` if no docstring is found.
    """

    docstring: Optional[str] = None
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            docstring_match = re.match(
                r'^[ \t]*("""(.*?)"""|\'\'\'(.*?)\'\'\')', content, re.DOTALL
            )
            if docstring_match:
                docstring = docstring_match.group(2) or docstring_match.group(3)
                docstring = docstring.strip()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return docstring


def generate_structure_file(project_root: str) -> None:
    """
    Generates a file containing the project structure based on the directory layout.

    This function generates the architecture content by recursively traversing the
    project directory structure, considering excluded items and docstrings (if enabled).
    It then writes this content to a file, specified by the configuration or default file.

    Args:
        project_root (str): The root directory of the project to analyze.
    """

    config = load_config(project_root)
    excluded_items: Set[str] = DEFAULT_EXCLUDED_ITEMS.union(config['exclude'])
    read_docstrings: bool = config['read_docstrings']
    output_file: str = config['output_file']

    architecture_content: str = "```angular2html\n"
    architecture_content += generate_structure(
        project_root,
        excluded_items,
        read_docstrings,
    )
    architecture_content += "\n```"

    output_path: str = os.path.join(project_root, output_file)

    if os.path.exists(output_path):
        with open(output_path, "a", encoding="utf-8") as file:
            file.write("\n\n# Architecture\n\n")
            file.write(architecture_content)
        print(f"Project architecture successfully added to existing file "
              f"{output_path}")
    else:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write("# Architecture\n\n")
            file.write(architecture_content)
        print(f"File {output_path} with project architecture successfully created")


def generate_structure(
    path: str,
    excluded_items: Set[str],
    read_docstrings: bool = True,
    prefix: str = ""
) -> str:
    """
    Recursively traverses the file system structure and generates a list with indentation.

    This function recursively scans the given directory and its subdirectories,
    excluding the directories specified in `excluded_items`. For Python files, it
    attempts to extract the docstring and appends it to the structure representation.

    Args:
        path (str): The root directory to scan.
        excluded_items (Set[str]): A set of directory names to exclude from the scan.
        read_docstrings (bool): Whether to read Python docstrings (default: True).
        prefix (str): The current indentation prefix for the structure (default: "").

    Returns:
        str: A string representing the indented file and folder structure.
    """

    structure: str = ""
    items = sorted(os.listdir(path))
    for index, item in enumerate(items):
        item_path = os.path.join(path, item)

        if item in excluded_items:
            continue

        connector: str = "└── " if index == len(items) - 1 else "├── "

        if os.path.isdir(item_path):
            structure += f"{prefix}{connector}{item}/\n"
            structure += generate_structure(
                item_path,
                excluded_items,
                read_docstrings,
                prefix + ("    " if index == len(items) - 1 else "│   "),
            )
        else:
            if item.endswith('.py') and read_docstrings:
                docstring = extract_docstring(item_path)
                if docstring:
                    structure += f"{prefix}{connector}{item} - {docstring}\n"
                else:
                    structure += f"{prefix}{connector}{item}\n"
            else:
                structure += f"{prefix}{connector}{item}\n"
    return structure


def main() -> None:
    """
    Main entry point for the script.

    This function parses command-line arguments and triggers the process of
    generating the project structure file. It expects one argument: the root
    directory of the project.
    """

    import sys
    if len(sys.argv) != 2:
        print("Usage: generate-structure <project_root>")
    else:
        project_root: str = sys.argv[1]
        generate_structure_file(project_root)


if __name__ == "__main__":
    main()
