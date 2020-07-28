import os
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
    #shutil.rmtree('./repo', ignore_errors=True)
