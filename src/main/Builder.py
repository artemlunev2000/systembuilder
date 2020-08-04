import json
import subprocess
from subprocess import Popen
from datetime import datetime
from src.main.Manifest import Manifest


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

    # @staticmethod
    # def get_parse():
    #     parser = argparse.ArgumentParser()
    #     parser.add_argument('--platform', type=str, help='Set target platform for build', dest='platform')
    #     parser.add_argument('--path', type=str, help='Set path to docker file', default='.', dest='path')
    #     return parser

    @staticmethod
    def get_build():
        yaml = Manifest()
        data = yaml.load_file('.').items()
        docker_build_cmd = ['docker', 'buildx', 'build']
        docker_build_arg = ['--platform', data['platform'], data['path']]
        subprocess.check_call(docker_build_cmd + docker_build_arg)
