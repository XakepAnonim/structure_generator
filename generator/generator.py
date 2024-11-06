import os
import toml

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
    config_files=("structure_config.toml", "structure.toml", "pyproject.toml")
):
    """
    Пытается загрузить конфигурацию из нескольких возможных TOML файлов.
    """

    config = {
        'exclude': set(),
        'read_docstrings': True  # default
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
                else:
                    config['exclude'] = set(config_data.get('exclude', []))
                    config['read_docstrings'] = config_data.get('read_docstrings', True)
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
            lines = file.readlines()
            # Пробуем найти докстринг в первых нескольких строках файла
            if lines and lines[0].strip().startswith('"""'):
                docstring_lines = []
                for line in lines[1:]:
                    if line.strip().startswith('"""'):
                        break
                    docstring_lines.append(line.strip())
                docstring = " ".join(docstring_lines).strip()
    except Exception as e:
        print(f"Ошибка при чтении файла {file_path}: {e}")
    return docstring


def generate_readme_structure(project_root):
    """
    Генерирует README.md с архитектурой проекта на основе файловой структуры.
    """

    config = load_config(project_root)
    excluded_items = DEFAULT_EXCLUDED_ITEMS.union(config['exclude'])
    read_docstrings = config['read_docstrings']

    architecture_content = "```angular2html\n"
    architecture_content += generate_structure(
        project_root,
        excluded_items,
        read_docstrings,
    )
    architecture_content += "\n```"

    readme_path = os.path.join(project_root, "README.md")

    if os.path.exists(readme_path):
        with open(readme_path, "a", encoding="utf-8") as readme_file:
            readme_file.write("\n\n# Архитектура\n\n")
            readme_file.write(architecture_content)
        print(f"Архитектура проекта успешно добавлена в существующий README.md в "
              f"{readme_path}")
    else:
        with open(readme_path, "w", encoding="utf-8") as readme_file:
            readme_file.write("# Архитектура\n\n")
            readme_file.write(architecture_content)
        print(f"README.md с архитектурой проекта успешно создан в {readme_path}")


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
        generate_readme_structure(project_root)


if __name__ == "__main__":
    main()
