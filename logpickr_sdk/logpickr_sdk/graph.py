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

    @staticmethod
    def from_json(project_id, jsstring):
        jgraph = json.loads(jsstring)
        jverts = jgraph["vertexInstances"]
        jedges = jgraph["edgeInstances"]

        vertices = [VertexInstance.from_json(v) for v in jverts]
        for vertex in vertices:
            # replace the list of "ids" with a list of the proper objects
            oldconcurr = vertex.concurrent_vertices
            vertex.concurrent_vertices = [v for v in vertices if (v.name + str(v.event_instance)) in oldconcurr]
        # Up to this point: works fine, good job me
        print("oi")
        edges = [EdgeInstance.from_json(e, vertices) for e in jedges]

        for edge in edges:
            concurrent_ids = edge.concurrent_edges
            edge.concurrent_edges = [e for e in edges if (edge_to_str(e) in concurrent_ids and e != edge)]

        return GraphInstance(project_id, vertices, edges, jgraph["reworkTotal"], jgraph["concurrencyRate"])



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

    @staticmethod
    def from_json(jvert):
        # If there are no concurrent vertices, there's going to be no concurrentVertices argument, instead of an empty
        # list, so I have to do this nonsense instead to make sure I don't get key errors
        conc = [v["name"] +str(v["eventInstance"]) for v in jvert["concurrentVertices"]] if "concurrentVertices" in jvert.keys() else []
        # Note: the concurrent vertices are currently just ids constructed from the event instance and name. While it
        # should be unique, this method is only called right before these weird ids get replaced with actual pointers
        return VertexInstance(jvert["id"], jvert["name"], jvert["eventInstance"], conc)


class Edge:
    """Edge between two vertices of a Logpickr graph
    """

    def __init__(self, eid: str, source: Vertex, destination: Vertex):
        self.id = eid
        self.source = source
        self.destination = destination


class EdgeInstance:

    def __init__(self, source: VertexInstance, destination: VertexInstance, concurrent_edges: list):
        self.source = source
        self.destination = destination
        self.concurrent_edges = concurrent_edges

    @staticmethod
    def from_json(jedge, vertices):

        conc = [edge_dict_to_str(e) for e in jedge["concurrentEdges"]] if "concurrentEdges" in jedge.keys() else []
        source = next(v for v in vertices if v.id == jedge["source"]["id"])
        dest = next(v for v in vertices if v.id == jedge["destination"]["id"])
        # Note: the concurrent edges are currently just ids constructed from the edge vertices' ids. While it
        # should be unique, this method is only called right before these weird ids get replaced with actual pointers
        return EdgeInstance(source, dest, conc)


def edge_dict_to_str(edge):
    csource = edge["source"]
    cdest = edge["destination"]
    return (str(csource["id"]) + csource["name"] + str(csource["eventInstance"]) +
            str(cdest["id"]) + cdest["name"] + str(cdest["eventInstance"]))


def edge_to_str(edge):
    csource = edge.source
    cdest = edge.destination
    return (str(csource.id) + csource.name + str(csource.event_instance) +
            str(cdest.id) + cdest.name + str(cdest.event_instance))
