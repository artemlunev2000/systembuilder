from src.main.builder import Builder
from src.main.manifest import Manifest

builder = Builder(Manifest())

try:
	builder.get_build()
	message = ""
	status = True
except Exception as e:
	message = str(e) 
	status = False

builder.generate_status_file(status, message)