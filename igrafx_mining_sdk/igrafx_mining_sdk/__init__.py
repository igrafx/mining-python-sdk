# Apache License 2.0, Copyright 2023 iGrafx
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE

from igrafx_mining_sdk.column_mapping import FileType, FileStructure, ColumnMapping, MetricAggregation, DimensionAggregation
from igrafx_mining_sdk.datasource import Datasource
from igrafx_mining_sdk.workgroup import Workgroup
from igrafx_mining_sdk.project import Project
from igrafx_mining_sdk.graph import Graph, GraphInstance
import toml

with open('../../pyproject.toml', 'r') as f:
    pyproject_data = toml.load(f)


__author__ = pyproject_data['tool']['poetry']['authors'][0]
__email__ = 'contact@igrafx.com'
__version__ = pyproject_data['tool']['poetry']['version']

__doc__ = """
igrafx_mining_sdk
================

Description
-----------
igrafx_mining_sdk is a Python package created by iGrafx. 
The iGrafx P360 Live Mining SDK is an open source application that can be used to manage your mining projects.
This information will show up when using the help function.
"""