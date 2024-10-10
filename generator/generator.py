import os


def generate_readme_structure(project_root):
    """
    Генерирует README.md с архитектурой проекта на основе файловой структуры.
    """

    architecture_content = "```angular2html\n"
    architecture_content += generate_structure(project_root)
    architecture_content += "\n```"

    readme_path = os.path.join(project_root, "README.md")

    if os.path.exists(readme_path):
        with open(readme_path, "a", encoding="utf-8") as readme_file:
            readme_file.write("\n\n# Архитектура\n\n")
            readme_file.write(architecture_content)
        print(f"Архитектура проекта успешно добавлена в существующий README.md в {readme_path}")
    else:
        with open(readme_path, "w", encoding="utf-8") as readme_file:
            readme_file.write("# Архитектура\n\n")
            readme_file.write(architecture_content)
        print(f"README.md с архитектурой проекта успешно создан в {readme_path}")


def generate_structure(path, prefix=""):
    """
    Рекурсивно проходит по структуре файлов и папок, генерируя список с отступами.
    """

    structure = ""
    items = sorted(os.listdir(path))
    for index, item in enumerate(items):
        item_path = os.path.join(path, item)

        if item in {
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
        }:
            continue

        connector = "└── " if index == len(items) - 1 else "├── "

        if os.path.isdir(item_path):
            structure += f"{prefix}{connector}{item}/\n"
            structure += generate_structure(item_path, prefix + ("    " if index == len(items) - 1 else "│   "))
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
