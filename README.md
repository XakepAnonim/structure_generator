# Project Structure Generator

Этот пакет позволяет автоматически создавать описание архитектуры проекта и сохранять его в `README.md`.

## Установка

Установите пакет через pip:
```bash
pip install structure-generator-by-xakepanonim
```

## Как пользоваться

Перед тем как использовать пакет, убедитесь что находитесь в корневой папке проекта и запустите команду:

```bash
generate-structure .
```


## Настройки

Пакет поддерживает несколько вариантов файлов конфигурации для указания исключений:

1. `structure.toml` — дефолтный файл
2. `pyproject.toml` — в этом файле используйте секцию `[tool.structure_generator]`

Параметры:

- `exclude` — список файлов, которые необходимо исключить из генерации
- `read_docstrings` — если `true`, то будет считано описание документации для каждого файла

Пример настройки в `structure.toml`:
```toml
exclude = [
    'venv',
    '__pycache__',
    '.git',
]

read_docstrings = true
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
```
