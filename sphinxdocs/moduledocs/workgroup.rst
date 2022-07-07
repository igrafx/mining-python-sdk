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
You can create a column mapping and send file.
Each project allows you to get the various `graphs`_ it contains, and access its `Datasources`_.

.. autoclass:: Project
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