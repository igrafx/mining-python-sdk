.. py:currentmodule:: logpickr_sdk

Workgroups and Projects
=======================

Workgroups
----------

Workgroups are the first and essential step to accessing your Logpickr data. They are instanciated with a valid workgroup ID and Secret key (which can be found in your Workgroup settings in Process Explorer 360). Workgroups allow you to access the projects created within the workgroup and the associated datasources.

.. autoclass:: Workgroup
   :special-members: __init__
   :members:

   
Projects
--------

A Project object contains the the information about a Logpickr project. 
You can create a column mapping and send file. For that you need to provide a `ColumnMapping`_ and `FileStructure`_
Each project allows you to get the various `graphs`_ it contains, and access its `Datasources`_.

.. autoclass:: Project
   :special-members: __init__
   :members:


ColumnMapping
--------

ColumnMapping must be provided before sending a file.
ColumnMapping contains `CaseIdOrActivityMapping`_ for CaseIdMapping or ActivityMapping , list of `TimeMapping`_ , list of `DimensionMapping`_ and list of `MetricMapping`_.

.. autoclass:: ColumnMapping
   :special-members: __init__
   :members:


CaseIdOrActivityMapping
--------
A CaseIdOrActivityMapping that must be provided to ColumnMapping_

.. autoclass:: CaseIdOrActivityMapping
   :special-members: __init__
   :members:
   

TimeMapping
--------
A TimeMapping that must be provided to ColumnMapping_

.. autoclass:: TimeMapping
   :special-members: __init__
   :members:


DimensionMapping
--------
A DimensionMapping that must be provided to ColumnMapping_

.. autoclass:: DimensionMapping
   :special-members: __init__
   :members:


MetricMapping
--------
A MetricMapping that must be provided to ColumnMapping_

.. autoclass:: MetricMapping
   :special-members: __init__
   :members:


FileStructure
--------
FileStructure that must be provided to create_column_mapping

.. autoclass:: FileStructure
   :special-members: __init__
   :members:


Datasources
-----------

Datasources allow you to perform custom SQL requests to the Druid databases containing the data for your projects. Datasources are always obtained through the Workgroups_ or the Projects_, so you shouldn't need to instanciate one on your lonesome.

.. autoclass:: Datasource
   :special-members: __init__
   :members:
   
.. _graphs: graph.html

Utility functions
-----------------

.. autofunction:: set_api_url

.. autofunction:: set_auth_url