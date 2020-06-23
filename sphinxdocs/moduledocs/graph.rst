Graphs and Graph Instances
==========================

Graphs
------

Each `project`_ has a single model graph, which is sometimes referred to as the model. This graph represents the whole of your organization whose processes you're analyzing. Each node is an event, and every edge represents a possible transition between two events.

.. autoclass:: logpickr_sdk.graph.Graph
   :members:
   
.. autoclass:: logpickr_sdk.graph.Edge
   :members:
   
.. autoclass:: logpickr_sdk.graph.Vertex
   :members:
   
Graph Instances
---------------

Each GraphInstance represents the path through the model_ taken by a single process. Each project_ has a list of processes, and for every proccess there exists a graph instance.

.. autoclass:: logpickr_sdk.graph.GraphInstance
   :members:
   
.. autoclass:: logpickr_sdk.graph.EdgeInstance
   :members:
   
.. autoclass:: logpickr_sdk.graph.VertexInstance
   :members:

.. _project : workgroup.html#Projects
.. _model : Graphs
