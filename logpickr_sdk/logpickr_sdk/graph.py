class Graph:
    """A graph from a Logpickr project
    """

    def __init__(self, id, vertices, edges, rework_total=-1, concurrency_rate=-1):
        self.project_id = id
        self.vertices = vertices
        self.edges = edges
        self.rework_total = rework_total
        self.concurrency_rate = concurrency_rate


class Vertex:
    """Vertex of a Logpicker Graph
    """

    def __init__(self, parent, id, name, event_instance=-1, concurrent_vertices=None):
        self.id = id
        self.name = name
        self.event_instance = event_instance
        self.concurrent_vertices = concurrent_vertices
        self.parent = parent


class Edge:
    """Edge between two vertices of a Logpickr graph
    """

    def __init__(self, parent, id, source, destination, concurrent_edges=None):
        self.parent = parent
        self.id = id
        self.source = source
        self.destination = destination
        self.concurrent_edges = concurrent_edges
