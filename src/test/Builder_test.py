import os
import json
import shutil

from src.main.Builder import Builder
from time import sleep


def test_clone_repo():
    builder = Builder()
    builder.clone_repo('https://github.com/antonkurenkov/systembuilder.git')
    # waiting while cloning
    sleep(5)
    assert os.path.isfile('./repo/README.md')
    # deleting directory after testing, might not work on windows because can't delete .git file.
    # shutil.rmtree('./repo', ignore_errors=True)


def test_generate_status_file_with_error():
    builder = Builder()
    builder.generate_status_file(False, 'error')
    assert os.path.isfile('status.json')
    with open('status.json') as status_file:
        status = json.load(status_file)
    assert not status['status']
    assert status['message'] == 'error'
    os.remove('status.json')


def test_generate_status_file_without_error():
    builder = Builder()
    builder.generate_status_file(True)
    assert os.path.isfile('status.json')
    with open('status.json') as status_file:
        status = json.load(status_file)
    assert status['status']
    assert status['message'] == ""
    os.remove('status.json')
