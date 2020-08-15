import argparse

from src.main.builder import Builder
from src.main.manifest import Manifest


def build(path):
	status = True
	message = None

	try:
		manifest = Manifest(path)
		builder = Builder(manifest)
		builder.create_dockerfile()
		builder.get_build()
	except Exception as e:
		status = False
		message = str(e)
	finally:
		Builder.generate_status_file(status, message)


parser = argparse.ArgumentParser()
parser.add_argument('--path', type=inner_function)
parser.parse_args()
