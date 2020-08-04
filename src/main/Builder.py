import subprocess
from subprocess import Popen
from manifest import Manifest


class Builder:
    def clone_repo(self, url):
        Popen(['git', 'clone', url, './repo/'])

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