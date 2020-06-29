# logpickr-sdk

## Installing

To install the SDK from source, simply navigate to `logpickr_sdk`, and run `pip install .`  
Alternatively, if you plan to modify the SDK, use `pip install -e .`.
This will create a symlink to the current directory instead of compressing and installing the source.
This means that any changes made to the source will be instantly reflected anywhere the module is used.

## Docs

The documentation is built with [Sphinx 1.8.0](https://www.sphinx-doc.org/en/master/) and can be found at `sphinxdocs/_build/index.html`. 
To regenerate the doc, simply go to `sphinxdocs` and use the command `make html` (this requires Sphinx, which can be installed through pip)