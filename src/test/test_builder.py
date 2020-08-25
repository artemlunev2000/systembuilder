import os
import json
import yaml
import unittest
import shutil

from src.main.builder import Builder
from src.main.manifest import Manifest
from time import sleep


class BuilderTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        data = {'docker': {'dockerfile': 'FROM python:latest\nENTRYPOINT ["python"]', 'parameters': ['some parameter']},
                'name': 'test', 'description': 'test', 'path': 'test'}
        with open('info.yaml', 'w') as file:
            yaml.dump(data, file)
        unittest.TestCase.__init__(self, *args, **kwargs)

    def test_clone_repo(self):
        builder = Builder(Manifest('info.yaml'))
        builder.clone_repo('https://github.com/antonkurenkov/systembuilder.git')
        # waiting while cloning
        sleep(5)
        assert os.path.isfile('./repo/README.md')
        # deleting directory after testing, might not work on windows because can't delete .git file.
        # shutil.rmtree('./repo', ignore_errors=True)

    def test_generate_status_file_with_error(self):
        builder = Builder(Manifest('info.yaml'))
        project_status = builder.generate_status(False, "error")
        builder.generate_status_file(1.0, {"project": project_status})
        assert os.path.isfile('status.json')
        with open('status.json') as status_file:
            status = json.load(status_file)
        assert not status['status']['project']['status']
        assert status['status']['project']['message'] == 'error'
        os.remove('status.json')

    def test_generate_status_file_without_error(self):
        builder = Builder(Manifest('info.yaml'))
        project_status = builder.generate_status(True)
        builder.generate_status_file(1.0, {"project": project_status})
        assert os.path.isfile('status.json')
        with open('status.json') as status_file:
            status = json.load(status_file)
        assert status['status']['project']['status']
        assert status['status']['project']['message'] == ""
        assert status['version'] == 1.0
        os.remove('status.json')

    def test_create_dockerfile(self):
        builder = Builder(Manifest('info.yaml'))
        builder.create_dockerfile()
        assert os.path.isfile('Dockerfile')
        with open('Dockerfile', 'r') as dockerfile:
            fst_line = dockerfile.readline()
        assert fst_line == 'FROM python:latest\n'
        os.remove('info.yaml')
        os.remove('Dockerfile')
