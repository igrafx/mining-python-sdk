

# iGrafx P360 Live Mining SDK


[![PyPI pyversions](https://img.shields.io/pypi/pyversions/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![PyPi version](https://badgen.net/pypi/v/pip/)](https://pypi.org/project/pip)
[![PyPI download month](https://img.shields.io/pypi/dm/ansicolortags.svg)](https://pypi.python.org/pypi/ansicolortags/)
[![Downloads](https://img.shields.io/github/downloads/igrafx/mining-python-sdk/)](https://github.com/igrafx/mining-python-sdk)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/igrafx/mining-python-sdk/blob/main/LICENSE)
[![GitHub forks](https://badgen.net/github/forks/igrafx/mining-python-sdk)](https://github.com/igrafx/mining-python-sdk/forks)
[![Issues](https://img.shields.io/github/issues/{username}/{repo-name}.svg)](github issues link)
[![Project Status](http://www.repostatus.org/badges/latest/active.svg)](http://www.repostatus.org/#active)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Open Source Love svg2](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

***

## Introduction
***
The **iGrafx P360 Live Mining SDK** is an open source application that can be used to manage your mining projects.
It is a python implementation of the iGrafx P360 Live Mining API.

With this SDK, you will be able to create workgroups, projects, datasources and graphs (and graph instances). You will also be able to create and 
add a column mapping.

Please note that you must have an iGrafx account in order to be able to use the SDK properly. Please contact us to create an account.

The iGrafx P360 Live Mining SDK uses Python.

A detailed tutorial can be found in the [howto.md]() file.


## Requirements
***

This package requires python 3.6.8 or above. Get the latest version of [Python](https://www.python.org/).

The required packages should be installed via the ```pyproject.toml``` when running the  ```poetry install``` command. 

## Installing
***
### With pip:
To install the current release of the iGrafx P360 Live Mining SDK with **pip**, simply navigate to the console and type the following command: 
````shell
pip install igrafx_mining_sdk
````

### From Wheel:

Download the latest version of the wheel [here](https://gitlab.com/igrafx/logpickr/logpickr-sdk). Then, navigate to your download folder and run: 
```shell
pip install igrafx_mining_sdk.whl
```
### To begin:
Go ahead and **import** the package:
```python
import igrafx_mining_sdk as igx   # the 'as igx' is entirely optional, but it will make the rest of our code much more readable
```

## Documentation
***
The full documentation can be found in the ```howto.md``` file [here](https://github.com/igrafx/).
Follow the instructions to try out the SDK.

## Download packages
***
Download the corresponding wheel package to the Mining platform version
* [2.17.0 and above](https://gitlab.com/igrafx/logpickr/logpickr-sdk/-/jobs/artifacts/2.17.0/download?job=build_wheel)
* [2.16.0 and above](https://gitlab.com/igrafx/logpickr/logpickr-sdk/-/jobs/artifacts/2.16.0/download?job=build_wheel)
* [2.15.1 and above](https://gitlab.com/igrafx/logpickr/logpickr-sdk/-/jobs/artifacts/2.15.1/download?job=build_wheel)
* [2.15.0 and above](https://gitlab.com/igrafx/logpickr/logpickr-sdk/-/jobs/artifacts/2.15.0/download?job=build_wheel)
* [2.14.0 and above](https://gitlab.com/igrafx/logpickr/logpickr-sdk/-/jobs/artifacts/2.14.0/download?job=build_wheel)
* [2.13.1 and above](https://gitlab.com/igrafx/logpickr/logpickr-sdk/-/jobs/artifacts/2.13.1/download?job=build_wheel)
* [2.13.0](https://gitlab.com/igrafx/logpickr/logpickr-sdk/-/jobs/artifacts/2.13.0/download?job=build_wheel)
* [2.12.1 and below](https://gitlab.com/igrafx/logpickr/logpickr-sdk/-/jobs/artifacts/2.12.1/download?job=build_wheel)

## Contributing
***
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

For more information on how to contribute, please see the ````CONTRIBUTING.md```` file.

## Support
***
Support is available at the following address: [support@igrafx.com](mailto:support@igrafx.com).

## Notice
***
Your feedback and contributions are important to us. Don't hesitate to contribute to the project.

## License
***
This SDK is licensed under the MIT License. See the ````LICENSE```` file for more details.