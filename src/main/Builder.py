import json

from subprocess import Popen
from datetime import datetime


class Builder:
    def clone_repo(self, url):
        Popen(['git', 'clone', url, './repo/'])

    def generate_status_file(self, status, message=""):
        json_status = {}
        with open('version.txt', 'r') as version_file:
            json_status['release'] = float(version_file.read())
        json_status['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_status['status'] = status
        json_status['message'] = message
        with open('status.json', 'w') as outfile:
            json.dump(json_status, outfile)
