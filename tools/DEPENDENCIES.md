# Зависимости проекта winLoadXRAY

Этот каталог содержит различные файлы зависимостей для установки и настройки окружения проекта winLoadXRAY.

## Файлы зависимостей

### Основные файлы

- **`requirements.txt`** - Основной файл зависимостей с минимальными требованиями к версиям
- **`requirements-exact.txt`** - Точные версии пакетов для стабильной установки

### Современные форматы

- **`pyproject.toml`** - Современный стандарт Python проектов (рекомендуется)
- **`setup.py`** - Традиционный setuptools файл

### Менеджеры окружений

- **`Pipfile`** - Для pipenv
- **`environment.yml`** - Для conda/Anaconda

## Установка зависимостей

### Стандартная установка (pip)

```bash
# С минимальными требованиями
pip install -r requirements.txt

# С точными версиями
pip install -r requirements-exact.txt
```

### Современная установка (pip + pyproject.toml)

```bash
pip install -e .
```

### Установка для разработки

```bash
pip install -e ".[dev]"
```

### Использование pipenv

```bash
pipenv install
pipenv install --dev
```

### Использование conda

```bash
conda env create -f environment.yml
conda activate winLoadXRAY
```

## Основные зависимости

- **pillow>=10.0.0** - Обработка изображений для GUI
- **requests>=2.31.0** - HTTP запросы для загрузки подписок
- **pyinstaller>=5.13.0** - Сборка в исполняемый файл (только для dev)

## Системные требования

- Python 3.8+
- Windows 10/11
- Права администратора (для TUN-режима)

## Внешние компоненты

Для полной функциональности также требуется:

1. **XRAY Core** - скачать с https://github.com/XTLS/Xray-core/releases
2. **tun2proxy** - скачать с https://github.com/tun2proxy/tun2proxy/releases

См. основной README.md для подробных инструкций по установке.