from setuptools import setup

setup(name="logpickr_sdk",
      version="2.21.0",
      description="A python implementation of Logpickr's public API",
      url="logpickr.com",
      author="Logpickr",
      author_email="contact@logpickr.com",
      packages=["logpickr_sdk"],
      install_requires=['requests', 'pandas', 'sqlalchemy', 'pydruid==0.6.3', 'graphviz', 'sphinx', 'pytest', 'sphinx-rtd-theme'],
      licence="Apache License 2.0"
      )
