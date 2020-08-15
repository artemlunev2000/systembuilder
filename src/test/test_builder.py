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
                'name': 'test', 'description': 'test'}
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
        builder.generate_status_file(False, 'error')
        assert os.path.isfile('status.json')
        with open('status.json') as status_file:
            status = json.load(status_file)
        assert not status['status']
        assert status['message'] == 'error'
        os.remove('status.json')

    def test_generate_status_file_without_error(self):
        builder = Builder(Manifest('info.yaml'))
        builder.generate_status_file(True)
        assert os.path.isfile('status.json')
        with open('status.json') as status_file:
            status = json.load(status_file)
        assert status['status']
        assert status['message'] == ""
        os.remove('status.json')

    def test_create_dockerfile(self):
        data = {'docker': {'dockerfile': 'FROM python:latest\nENTRYPOINT ["python"]', 'parameters': ['some parameter']},
                'name': 'test', 'description': 'test'}
        with open('info.yaml', 'w') as file:
            yaml.dump(data, file)
        builder = Builder(Manifest('info.yaml'))
        builder.create_dockerfile()
        assert os.path.isfile('DOCKERFILE')
        with open('DOCKERFILE', 'r') as dockerfile:
            fst_line = dockerfile.readline()
        assert fst_line == 'FROM python:latest\n'
        os.remove('info.yaml')
        os.remove('DOCKERFILE')
