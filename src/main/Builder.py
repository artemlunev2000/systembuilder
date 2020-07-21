from subprocess import Popen


class Builder:
    def clone_repo(self, url):
        Popen(['git', 'clone', url, './repo/'])
