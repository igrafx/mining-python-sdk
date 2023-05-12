from setuptools import setup
import re

# # Extract the version from the init file.
init_file = "igrafx_mining_sdk/__init__.py"
package_infos = {"__author__": None, "__email__": None, "__version__": None, "__doc__": None}
for k in package_infos:
    res = re.search(r"^%s = ['\"]([^'\"]*)['\"]" % k, open(init_file, "rt").read(), re.M)
    if res:
        package_infos[k] = res.group(1)
    else:
        raise RuntimeError(f'Unable to find {k} element in {init_file}')

with open('../requirements.txt', 'r') as f:
    requirements = [line.strip() for line in f if line.strip()]


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
