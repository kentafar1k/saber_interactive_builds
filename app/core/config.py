from app.services.build_service import BuildService
import os

# Пути к YAML-файлам
TASKS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'builds', 'tasks.yaml')
BUILDS_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', 'builds', 'builds.yaml')

build_service = BuildService(tasks_path=TASKS_PATH, builds_path=BUILDS_PATH) 