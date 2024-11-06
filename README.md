# Project Structure Generator

This package automatically generates a project architecture description and saves it in the `README.md` file.

## Installation

Install the package using pip:
```bash
pip install structure-generator-by-xakepanonim
```

## Usage

Before using the package, make sure you are in the root directory of the project and run the following command:

```bash
generate-structure .
```

## Configuration

The package supports multiple configuration file options for specifying exclusions:

1. `structure.toml` — the default configuration file
2. `pyproject.toml` — use the section `[tool.structure_generator]` in this file

Parameters:

- `exclude` — a list of files to exclude from the generation process
- `read_docstrings` — if `true`, the documentation strings (docstrings) will be read for each file
- `output_file` — the path to the file where the architecture description will be saved

Example configuration in `structure.toml`:
```toml
exclude = [
    'venv',
    '__pycache__',
    '.git',
]

read_docstrings = true
output_file = "README.md"
```

Example configuration in `pyproject.toml`:
```toml
[tool.structure_generator]
exclude = [
    'venv',
    '__pycache__',
    '.git',
]

read_docstrings = true
output_file = "README.md"
```

---

# Генератор Структуры Проекта

Этот пакет автоматически генерирует описание архитектуры проекта и сохраняет его в файл `README.md`.

## Установка

Установите пакет через pip:
```bash
pip install structure-generator-by-xakepanonim
```

## Использование

Перед тем как использовать пакет, убедитесь, что вы находитесь в корневой папке проекта, и выполните следующую команду:

```bash
generate-structure .
```

## Конфигурация

Пакет поддерживает несколько вариантов файлов конфигурации для указания исключений:

1. `structure.toml` — дефолтный файл конфигурации
2. `pyproject.toml` — используйте секцию `[tool.structure_generator]` в этом файле

Параметры:

- `exclude` — список файлов, которые необходимо исключить из генерации
- `read_docstrings` — если `true`, то будет считано описание документации для каждого файла
- `output_file` — путь к файлу, в который будет сохранено описание архитектуры

Пример настройки в `structure.toml`:
```toml
exclude = [
    'venv',
    '__pycache__',
    '.git',
]

read_docstrings = true
output_file = "README.md"
```

Пример настройки в `pyproject.toml`:
```toml
[tool.structure_generator]
exclude = [
    'venv',
    '__pycache__',
    '.git',
]

read_docstrings = true
output_file = "README.md"
```