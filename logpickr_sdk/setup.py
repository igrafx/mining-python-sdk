from setuptools import setup

setup(name="logpickr_sdk",
      version="0.1",
      description="A python implementation of Logpickr's public API",
      url="logpickr.com",
      author="Theotime Dugois",
      author_email="theotime.dugois@gmail.com",
      packages=["logpickr_sdk"],
      install_requires=['requests', 'pandas', 'pydruid==0.5.9', 'graphviz', 'sphinx', 'pytest', 'sphinx-rtd-theme'],
      licence="Apache License 2.0"
      )
