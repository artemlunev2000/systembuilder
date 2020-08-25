import json
import subprocess
from subprocess import Popen
from datetime import datetime


class Builder:
    def __init__(self, manifest):
        self.__manifest = manifest

    def clone_repo(self, url):
        Popen(['git', 'clone', url, './repo/'])

    @staticmethod
    def generate_status_file(version, json_status=None):
        if json_status:
            status = dict(status=json_status, datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), version=version)
            with open('status.json', 'w') as outfile:
                json.dump(status, outfile)

    @staticmethod
    def generate_status(status, message=""):
        json_status = {}
        json_status['status'] = status
        json_status['message'] = message
        return json_status

    def create_dockerfile(self):
        data = self.__manifest.data
        with open('Dockerfile', 'w') as outfile:
            docker_data = data['docker']['dockerfile']
            if data['docker']['parameters']:
                docker_data += '\nLABEL parameter=' + data['docker']['parameters'].__str__()
            outfile.write(docker_data)

    def get_build(self):
        data = self.__manifest.data
        docker_build_cmd = ['docker', 'build']
        docker_build_arg = [data['path']]
        subprocess.check_call(docker_build_cmd + docker_build_arg)
