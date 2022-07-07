from setuptools import setup

setup(name="logpickr_sdk",
      version="0.3",
      description="A python implementation of Logpickr's public API",
      url="logpickr.com",
      author="Logpickr",
      author_email="contact@logpickr.com",
      packages=["logpickr_sdk"],
      install_requires=['requests', 'pandas', 'pydruid==0.6.3', 'sqlalchemy', 'graphviz', 'sphinx', 'pytest', 'sphinx-rtd-theme'],
      licence="Apache License 2.0"
      )
