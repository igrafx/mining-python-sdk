from logpickr_sdk.project import Project

class Graph:
    """A graph from a Logpickr project
    """

    def __init__(self, id):
        self.id = id


class Vertex:
    """Vertex of a Logpicker Graph
    """

    def __init__(self, parent):
        self.parent = parent

class Edge:
    """Edge between two vertices of a Logpickr graph
    """

    def __init__(self, parent, source, destination):
        self.parent = parent
        self.source = source
        self.dest = destination
