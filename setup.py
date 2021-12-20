from pydoc import doc
from setuptools import setup
import docker_image_updater

setup(
    name = docker_image_updater.__name__,
    version = docker_image_updater.__version__,
    author = docker_image_updater.__author__,
    author_email = docker_image_updater.__author_email__,
    maintainer = docker_image_updater.__author__,
    maintainer_email = docker_image_updater.__author_email__,
    url = docker_image_updater.__url__,
    packages = ["docker_image_updater"],
    scripts = ["bin/diu"],
)
