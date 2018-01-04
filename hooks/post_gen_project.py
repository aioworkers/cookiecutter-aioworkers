from pathlib import Path

PROJECT_PATH = Path.cwd()

if '{{ cookiecutter.worker_example }}'.lower() == 'n':
    (PROJECT_PATH / 'worker.py').unlink()

if '{{ cookiecutter.docker }}'.lower() == 'n':
    (PROJECT_PATH / 'Dockerfile').unlink()
