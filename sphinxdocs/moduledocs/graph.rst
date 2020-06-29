Graphs and Graph Instances
==========================

Difference between Graphs and GraphInstances:
---------------------------------------------

Each `project`_ has a single model graph, which is sometimes referred to as the model. This graph represents the whole of the organization whose processes you're analyzing. Each node is an event, and every edge represents a possible transition between two events.

.. image:: modelgraph.svg
   :width: 500
   :alt: A model graph
   
*The model graph represents all of the ways a bank loan application can be handled*
   
Each GraphInstance, in turn, represents the path through the model_ taken by a single process. Each project_ has a list of processes, and for every proccess there exists a graph instance. Similarly to the model graphs, the edges represent the path taken by the process through the possible events.

.. image:: processgraph.svg
   :width: 500
   :alt: A process/instance graph
   
*The process graph represents how one specific process (one client here) went through the loan application process*

Graphs
------

.. autoclass:: logpickr_sdk.graph.Graph
   :members:
   
.. autoclass:: logpickr_sdk.graph.Edge
   :members:
   
.. autoclass:: logpickr_sdk.graph.Vertex
   :members:
   
Graph Instances
---------------

**Note: GraphInstance and VertexInstance extend Graph and Vertex respectively**


.. autoclass:: logpickr_sdk.graph.GraphInstance
   :members:
   
.. autoclass:: logpickr_sdk.graph.EdgeInstance
   :members:
   
.. autoclass:: logpickr_sdk.graph.VertexInstance
   :members:

.. _project : workgroup.html#Projects
.. _model : Graphs
