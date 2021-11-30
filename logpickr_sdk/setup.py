from setuptools import setup

setup(name="logpickr_sdk",
      version="0.2",
      description="A python implementation of Logpickr's public API",
      url="logpickr.com",
      author="Logpickr",
      author_email="contact@logpickr.com",
      packages=["logpickr_sdk"],
      install_requires=['requests', 'pandas', 'pydruid==0.5.9', 'graphviz', 'sphinx', 'pytest'],
      licence="Apache License 2.0"
      )
