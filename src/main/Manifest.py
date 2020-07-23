import os

import yaml


class Manifest:
    arguments = ['name', 'description', 'author', 'url', 'documentation'
        , 'version', 'vendor', 'license', 'avatar'
        , 'platform', 'update', 'keywords']

    @staticmethod
    def check_existent(path):
        return os.path.exists(path)

    def load_file(self, path):
        if self.check_existent(path):
            with open(path) as f:
                return yaml.safe_load(f)
        else:
            return None

    def validation(self, data, level=0):
        if level == 0:
            if 'name' not in data:
                raise KeyError(f'Required argument "name" no exist')

            if 'description' not in data:
                raise KeyError(f'Required argument "description" no exist')

        for item in data.items():
            if type(item[1]) is dict:
                self.validation(item[1], level=level + 1)
            if type(item[1]) is list:
                for l in item[1]:
                    self.validation(l, level=level + 1)
            if item not in self.arguments:
                raise KeyError(f'Unknown argument {item}')
