from contextlib import contextmanager

import docker
import py
import pytest
import sh
import time
from pytest_cookies import Cookies


@pytest.fixture(scope='session')
def cookies(request, _cookiecutter_config_file):
    # Customize directory to bake projects
    template_dir = request.config.option.template
    p = py.path.local('tests/projects')
    if p.exists():
        p.remove()
    output_factory = py.path.local('tests').mkdir('projects').mkdir

    return Cookies(template_dir, output_factory, _cookiecutter_config_file)


@pytest.fixture
def project_checker():
    def check(result):
        assert result.exit_code == 0
        assert result.exception is None
        assert result.project.isdir()

        # Check project with flake8
        try:
            sh.flake8(str(result.project))
        except sh.ErrorReturnCode as e:
            pytest.fail(e)
    return check


@pytest.fixture(scope='session')
def docker_client():
    return docker.from_env()


@pytest.fixture(scope='session')
def image_prefix():
    return 'integration/'


@pytest.fixture
def wait_for_message():
    def waiter(container, message, max_time=10):
        i = 0
        while i < max_time:
            for log in container.logs().decode('utf-8').split('\n'):
                if message in log:
                    time.sleep(1)
                    return
            time.sleep(1)
            i += 1
        raise pytest.fail(f'No message in log: {message}')
    return waiter


@pytest.fixture
def service_builder(cookies, image_prefix, docker_client):
    @contextmanager
    def builder(name=None, config=None):
        result = cookies.bake(extra_context=config)
        tag = image_prefix + name if name else None
        image = docker_client.images.build(path=result.project.strpath, tag=tag)
        container = docker_client.containers.run(image, detach=True)

        yield container

        container.kill()
        container.remove()

    return builder
