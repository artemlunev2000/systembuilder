import os

import yaml


class Manifest:
    def __init__(self, path):
        self.data = self.load_file(path)
        self.validation(self.data)

    required_arg = ['name', 'description', 'docker', 'path']
    optional_arg = ['author', 'url', 'documentation',
                    'version', 'vendor', 'license', 'avatar',
                    'update', 'keywords', 'dockerfile', 'parameters']

    @staticmethod
    def check_existent(path):
        return os.path.exists(path)

    def load_file(self, path):
        if self.check_existent(path):
            with open(path) as f:
                return yaml.safe_load(f)
        else:
            raise ValueError("Incorrect file path")

    def validation(self, data, level=0):
        if level == 0:
            for arg in self.required_arg:
                if arg not in data:
                    raise KeyError(f'Required argument {arg} no exist')

        for item in data.items():
            if type(item[1]) is dict:
                self.validation(item[1], level=level + 1)
            if type(item[1]) is list:
                for lst in item[1]:
                    if type(lst) is dict:
                        self.validation(lst, level=level + 1)
            if item[0] not in self.optional_arg and item[0] not in self.required_arg:
                raise KeyError(f'Unknown argument {item}')
