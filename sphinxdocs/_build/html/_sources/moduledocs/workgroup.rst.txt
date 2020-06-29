Workgroups and Projects
=======================

Workgroups
----------

Workgroups are the first and essential step to accessing your Logpickr data. They are instanciated with a valid workgroup ID and Secret key (which can be found in your Workgroup settings in Process Explorer 360). Workgroups allow you to access the projects created within the workgroup and the associated datasources.

.. autoclass:: logpickr_sdk.workgroup.Workgroup
   :members:
   
Projects
--------

A Project object contains the the information about a (drumroll please) Logpickr project! *note to self: remove the sarcasm.* Each project allows you to get the various `graphs`_ it contains, and access its `Datasources`_.

.. autoclass:: logpickr_sdk.workgroup.Project
   :members:
   
   
Datasources
-----------

Datasources allow you to perform custom SQL requests to the Druid databases containing the data for your projects. Datasources are always obtained through the Workgroups_ or the Projects_, so you shouldn't need to instanciate one on your lonesome.

.. autoclass:: logpickr_sdk.workgroup.Datasource
   :members:
   
.. _graphs: graph.html
