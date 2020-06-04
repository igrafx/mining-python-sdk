import json


class Graph:
    """A graph from a Logpickr project
    """

    def __init__(self, id, vertices, edges):
        self.project_id = id
        self.vertices = vertices
        self.edges = edges

    @staticmethod
    def from_json(project_id, jsstring):
        jgraph = json.loads(jsstring)
        jverts = jgraph["vertices"]
        jedges = jgraph["edges"]
        vertices = [Vertex(vertex["id"], vertex["name"]) for vertex in jverts]
        edges = []
        for edge in jedges:
            source = next((x for x in vertices if x.id == edge["source"]), None)
            dest = next((x for x in vertices if x.id == edge["destination"]), None)
            if source is not None and dest is not None:
                edges.append(Edge(edge["id"], source, dest))
            else:
                raise Exception("Invalid edge")

        return Graph(project_id, vertices, edges)


class GraphInstance(Graph):

    def __init__(self, id, vertices, edges, rework_total, concurrency_rate):
        super().__init__(id, vertices, edges)
        self.rework_total = rework_total
        self.concurrency_rate = concurrency_rate


class Vertex:
    """Vertex of a Logpicker Graph
    """

    def __init__(self, id, name):
        self.id = id
        self.name = name


class VertexInstance(Vertex):

    def __init__(self, id, name, event_instance, concurrent_vertices):
        super().__init__(id, name)
        self.event_instance = event_instance
        self.concurrent_vertices = concurrent_vertices


class Edge:
    """Edge between two vertices of a Logpickr graph
    """

    def __init__(self, id, source, destination):
        self.id = id
        self.source = source
        self.destination = destination


class EdgeInstance(Edge):

    def __init__(self, id, source, destination, concurrent_edges=None):
        super().__init__(id, source, destination)
        self.concurrent_edges = concurrent_edges
