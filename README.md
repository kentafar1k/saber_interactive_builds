# Saber Interactive Build System

## Описание
Микросервис для управления задачами и билдами игровой билд-системы. Реализован на FastAPI.

## Установка

1. Клонируйте репозиторий и перейдите в папку проекта.
2. Установите зависимости:

```bash
pip install -r requirements.txt
```

## Запуск

```bash
uvicorn app.main:app --reload
```

## Тестирование

```bash
pytest
```

## Пример запроса

POST `/api/v1/get_tasks`

```json
{
  "build": "make_tests"
}
```

Пример ответа:
```json
[
  "compile_exe",
  "pack_build"
]
```

## Структура проекта

- `app/` — исходный код микросервиса
- `builds/` — YAML-файлы с задачами и билдами
- `tests/` — тесты 