from setuptools import setup
import toml

# Parse pyproject.toml file
with open('../pyproject.toml', 'r') as f:
    pyproject_data = toml.load(f)

# Extract package information
package_infos = {
    "__author__": pyproject_data['tool']['poetry']['authors'][0],
    "__version__": pyproject_data['tool']['poetry']['version'],
    "__doc__": pyproject_data['tool']['poetry']['description']
}

# Extract requirements
requirements = list(pyproject_data['tool']['poetry']['dependencies'].values())

setup(
    name="igrafx_mining_sdk",
    version=package_infos['__version__'],
    description=package_infos['__doc__'],
    url="logpickr.com",
    author=package_infos['__author__'],
    author_email=package_infos['__email__'],
    packages=["igrafx_mining_sdk"],
    install_requires=requirements,
    licence="Apache License 2.0"
)
