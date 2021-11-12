from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in app_aqua/__init__.py
from app_aqua import __version__ as version

setup(
	name="app_aqua",
	version=version,
	description="Sistema Integral Para la Gestion de Juntas Comunitarias de Agua Potable",
	author="Francisco Adame",
	author_email="sebas.franksys@gmail.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
