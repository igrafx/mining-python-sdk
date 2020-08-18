# logpickr-sdk

## Requirements

This package requires python 3.6 or above. Get the latest version of python at https://www.python.org/.

The required packages should be automatically installed when installing the package for the first time. If they somehow don't, they are:

* requests `pip3 install requests`
* pydruid (version 0.5.9 is used here, as version 0.6.0 and 0.6.1 have a currently unresolved bug that prevents from connecting to the databases) `pip3 install pydruid==0.5.9`
* pandas `pip3 install pandas`
* graphviz to display the graphs `pip3 install graphviz`
* sphinx and the Read the Docs theme for the documentation `pip3 install sphinx sphinx-rtd-theme`
* pytest for the unittests `pip3 install pytest`

## Installing

To install the SDK from source, simply navigate to `logpickr_sdk`, and run `pip install .`  
Alternatively, if you plan to modify the SDK, use `pip install -e .`.
This will create a symlink to the current directory instead of compressing and installing the source.
This means that any changes made to the source will be instantly reflected anywhere the module is used.

## Docs

The documentation is built with [Sphinx 1.8.0](https://www.sphinx-doc.org/en/master/) and can be found at https://logpickr.gitlab.io/logpickr-sdk/. 
To regenerate the doc, simply go to `sphinxdocs` and use the command `make html` (this requires Sphinx, which can be installed through pip, see [above](#requirements)). The documentation will be built in the `sphinxdocs/_build/html` folder. Alternatively, any push to the master branch will trigger a rebuild of the online docs.

## Running the tests

The tests are written for pytest, which should be installed with this package. Navigate to the test folder and run `pytest -v --id "workgroup id" --key "workgroup key" --project "the id of a project"`, replacing what's in quotes with the appropriate values (keeping them in quotes, as the id and key contain some hyphens, which messes with parsing). The -v (verbose) flag is optional, but it can help see what went wrong.