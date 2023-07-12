from setuptools import setup, find_packages
import toml
import re

# Parse pyproject.toml file
with open('./pyproject.toml', 'r') as f:
    pyproject_data = toml.load(f)

# Extract package information
package_infos = {
    "__author__": pyproject_data['tool']['poetry']['authors'][0].split('<')[0].rstrip(),
    "__version__": pyproject_data['tool']['poetry']['version'],
    "__doc__": pyproject_data['tool']['poetry']['description'],
    "__email__": re.findall("[0-9a-zA-z]+@[0-9a-zA-z]+\.[0-9a-zA-z]+", pyproject_data['tool']['poetry']['authors'][0])[0]
}

# Extract requirements
requirements = list(pyproject_data['tool']['poetry']['dependencies'].values())

setup(
    name="igrafx_mining_sdk",
    version=package_infos['__version__'],
    description=package_infos['__doc__'],
    url="https://www.logpickr.com/fr/accueil.html",
    author=package_infos['__author__'],
    author_email=package_infos['__email__'],
    packages=find_packages(),
    licence="Apache License 2.0"
)
