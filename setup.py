from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

setup(
  name = "Fitbyte",
  version = "1.0.0",
  description = "",
  long_description = "",
  packages = find_packages(where='src'),
  install_requires = ['bcrypt', 'mysql', 'tabulate', 'matplotlib'],
)