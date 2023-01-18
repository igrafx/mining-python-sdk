from setuptools import setup

setup(name="logpickr_sdk",
      version="2.15.2",
      description="A python implementation of Logpickr's public API",
      url="logpickr.com",
      author="Logpickr",
      author_email="contact@logpickr.com",
      packages=["logpickr_sdk"],
      install_requires=['requests', 'pandas', 'sqlalchemy', 'pydruid', 'graphviz', 'sphinx', 'pytest', 'sphinx-rtd-theme'],
      licence="Apache License 2.0"
      )
