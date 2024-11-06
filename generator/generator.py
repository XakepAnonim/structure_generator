import os
import toml
import re

DEFAULT_EXCLUDED_ITEMS = {
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
}  # default


def load_config(
    project_root,
    config_files=("structure.toml", "pyproject.toml")
):
    """
    Пытается загрузить конфигурацию из нескольких возможных TOML файлов.
    """

    config = {
        'exclude': set(),
        'read_docstrings': True,  # default
        'output_file': "README.md"  # default
    }

    for config_file in config_files:
        config_path = os.path.join(project_root, config_file)
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as config_file:
                config_data = toml.load(config_file)

                # Если это pyproject.toml, ищем в секции [tool.structure_generator]
                if config_file.name.endswith("pyproject.toml"):
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


def extract_docstring(file_path):
    """
    Извлекает докстринг из Python файла, если он есть.
    Возвращает строку с докстрингом или None, если докстринга нет.
    """
    docstring = None
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
        print(f"Ошибка при чтении файла {file_path}: {e}")
    return docstring


def generate_structure_file(project_root):
    """
    Генерирует файл с архитектурой проекта на основе файловой структуры.
    Файл может быть указан в конфигурации TOML.
    """

    config = load_config(project_root)
    excluded_items = DEFAULT_EXCLUDED_ITEMS.union(config['exclude'])
    read_docstrings = config['read_docstrings']
    output_file = config['output_file']

    architecture_content = "```angular2html\n"
    architecture_content += generate_structure(
        project_root,
        excluded_items,
        read_docstrings,
    )
    architecture_content += "\n```"

    output_path = os.path.join(project_root, output_file)

    if os.path.exists(output_path):
        with open(output_path, "a", encoding="utf-8") as output_file:
            output_file.write("\n\n# Архитектура\n\n")
            output_file.write(architecture_content)
        print(f"Архитектура проекта успешно добавлена в существующий файл "
              f"{output_path}")
    else:
        with open(output_path, "w", encoding="utf-8") as output_file:
            output_file.write("# Архитектура\n\n")
            output_file.write(architecture_content)
        print(f"Файл {output_path} с архитектурой проекта успешно создан")


def generate_structure(path, excluded_items, read_docstrings=True, prefix=""):
    """
    Рекурсивно проходит по структуре файлов и папок, генерируя список с отступами.
    """

    structure = ""
    items = sorted(os.listdir(path))
    for index, item in enumerate(items):
        item_path = os.path.join(path, item)

        if item in excluded_items:
            continue

        connector = "└── " if index == len(items) - 1 else "├── "

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


def main():
    import sys
    if len(sys.argv) != 2:
        print("Использование: generate-structure <путь_до_проекта>")
    else:
        project_root = sys.argv[1]
        generate_structure_file(project_root)


if __name__ == "__main__":
    main()
