import json
import subprocess
from subprocess import Popen
from datetime import datetime
from src.main.manifest import Manifest


class Builder:
    def clone_repo(self, url):
        Popen(['git', 'clone', url, './repo/'])

    @staticmethod
    def generate_status_file(status, message=""):
        json_status = {}
        with open('version.txt', 'r') as version_file:
            json_status['release'] = float(version_file.read())
        json_status['datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        json_status['status'] = status
        json_status['message'] = message
        with open('status.json', 'w') as outfile:
            json.dump(json_status, outfile)

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
