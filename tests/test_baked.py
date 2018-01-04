from pathlib import Path


def test_default(cookies, project_checker):
    result = cookies.bake()
    project_checker(result)

    # check files in project
    path = Path(result.project)
    assert not (path / 'worker.py').exists()
    assert (path / 'Dockerfile').exists()


def test_worker(cookies, project_checker):
    result = cookies.bake(extra_context={'worker_example': 'y'})
    project_checker(result)

    path = Path(result.project)
    assert (path / 'worker.py').exists()


def test_docker(cookies, project_checker):
    result = cookies.bake(extra_context={'docker': 'n'})
    project_checker(result)

    path = Path(result.project)
    assert not (path / 'Dockerfile').exists()