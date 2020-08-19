import argparse
import os

from src.main.builder import Builder
from src.main.manifest import Manifest


def build_projects(path, filename):
	with open('version.txt', 'r') as version_file:
		version = float(version_file.read())
	os.chdir(path)
	folders = [f for f in os.listdir('.') if os.path.isdir(f)]
	status_obj = {}

	for project in folders:
		os.chdir(project)
		status_obj[project] = build_project(filename)
		os.chdir('..')
	Builder.generate_status_file(version, status_obj)


def build_project(path):
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
		return Builder.generate_status(status, message)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('--path', type=str)
	parser.add_argument('--filename', type=str)
	args = parser.parse_args()
	build_projects(**vars(args))
