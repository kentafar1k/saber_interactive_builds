import pytest
from app.services.build_service import BuildService
import tempfile
import yaml
import os

def make_yaml_files(tmp_path, tasks, builds):
    tasks_path = tmp_path / "tasks.yaml"
    builds_path = tmp_path / "builds.yaml"
    with open(tasks_path, 'w', encoding='utf-8') as f:
        yaml.dump({"tasks": tasks}, f)
    with open(builds_path, 'w', encoding='utf-8') as f:
        yaml.dump({"builds": builds}, f)
    return str(tasks_path), str(builds_path)

def test_topological_sort_simple(tmp_path):
    tasks = [
        {"name": "a", "dependencies": []},
        {"name": "b", "dependencies": ["a"]},
        {"name": "c", "dependencies": ["b"]},
    ]
    builds = [
        {"name": "build1", "tasks": ["c"]}
    ]
    tasks_path, builds_path = make_yaml_files(tmp_path, tasks, builds)
    service = BuildService(tasks_path, builds_path)
    assert service.get_sorted_tasks("build1") == ["a", "b", "c"]

def test_unknown_build(tmp_path):
    tasks = [{"name": "a", "dependencies": []}]
    builds = [{"name": "build1", "tasks": ["a"]}]
    tasks_path, builds_path = make_yaml_files(tmp_path, tasks, builds)
    service = BuildService(tasks_path, builds_path)
    with pytest.raises(ValueError):
        service.get_sorted_tasks("not_exist")

def test_unknown_task(tmp_path):
    tasks = [{"name": "a", "dependencies": []}]
    builds = [{"name": "build1", "tasks": ["b"]}]
    tasks_path, builds_path = make_yaml_files(tmp_path, tasks, builds)
    service = BuildService(tasks_path, builds_path)
    with pytest.raises(ValueError):
        service.get_sorted_tasks("build1")

def test_cycle_detection(tmp_path):
    tasks = [
        {"name": "a", "dependencies": ["b"]},
        {"name": "b", "dependencies": ["a"]},
    ]
    builds = [{"name": "build1", "tasks": ["a"]}]
    tasks_path, builds_path = make_yaml_files(tmp_path, tasks, builds)
    service = BuildService(tasks_path, builds_path)
    with pytest.raises(RuntimeError):
        service.get_sorted_tasks("build1") 