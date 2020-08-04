import json

from subprocess import Popen
from datetime import datetime


class Builder:
    def clone_repo(self, url):
        Popen(['git', 'clone', url, './repo/'])

    def generate_status_file(self):
        status = {}
        with open('version.txt', 'r') as version_file:
            status['release'] = float(version_file.read())
        status['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status['status'] = True
        with open('status.json', 'w') as outfile:
            json.dump(status, outfile)

    def generate_status_file_with_error(self, error):
        status = {}
        with open('version.txt', 'r') as version_file:
            status['release'] = float(version_file.read())
        status['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status['status'] = False
        status['message'] = error
        with open('status.json', 'w') as outfile:
            json.dump(status, outfile)
