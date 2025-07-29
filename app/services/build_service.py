from typing import Dict, List, Set
import yaml
from app.models.schemas import Task, Build

class BuildService:
    def __init__(self, tasks_path: str, builds_path: str):
        self.tasks_path = tasks_path
        self.builds_path = builds_path
        self.tasks: Dict[str, Task] = {}
        self.builds: Dict[str, Build] = {}
        self.load_data()

    def load_data(self):
        with open(self.tasks_path, 'r', encoding='utf-8') as f:
            tasks_yaml = yaml.safe_load(f)
        with open(self.builds_path, 'r', encoding='utf-8') as f:
            builds_yaml = yaml.safe_load(f)
        self.tasks = {t['name']: Task(**t) for t in tasks_yaml['tasks']}
        self.builds = {b['name']: Build(**b) for b in builds_yaml['builds']}

    def get_sorted_tasks(self, build_name: str) -> List[str]:
        if build_name not in self.builds:
            raise ValueError(f"Build '{build_name}' not found")
        build = self.builds[build_name]
        visited: Set[str] = set()
        temp_mark: Set[str] = set()
        result: List[str] = []

        def visit(task_name: str):
            if task_name not in self.tasks:
                raise ValueError(f"Task '{task_name}' not found")
            if task_name in temp_mark:
                raise RuntimeError(f"Cyclic dependency detected at '{task_name}'")
            if task_name not in visited:
                temp_mark.add(task_name)
                for dep in self.tasks[task_name].dependencies:
                    visit(dep)
                temp_mark.remove(task_name)
                visited.add(task_name)
                result.append(task_name)

        for task_name in build.tasks:
            visit(task_name)
        return result 