import json


class Graph:
    """A graph from a Logpickr project
    """

    def __init__(self, project_id: str, vertices: list, edges: list):
        self.project_id = project_id
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

    def __init__(self, project_id: str, vertices: list, edges: list, rework_total: int, concurrency_rate: float):
        super().__init__(project_id, vertices, edges)
        self.rework_total = rework_total
        self.concurrency_rate = concurrency_rate


class Vertex:
    """Vertex of a Logpicker Graph
    """

    def __init__(self, vid: str, name: str):
        self.id = vid
        self.name = name


class VertexInstance(Vertex):

    def __init__(self, vid: str, name: str, event_instance: int, concurrent_vertices: list):
        super().__init__(vid, name)
        self.event_instance = event_instance
        self.concurrent_vertices = concurrent_vertices


class Edge:
    """Edge between two vertices of a Logpickr graph
    """

    def __init__(self, eid: str, source: Vertex, destination: Vertex):
        self.id = eid
        self.source = source
        self.destination = destination


class EdgeInstance(Edge):

    def __init__(self, eid: str, source: VertexInstance, destination: VertexInstance, concurrent_edges: list):
        super().__init__(eid, source, destination)
        self.concurrent_edges = concurrent_edges
