# Apache License 2.0, Copyright 2022 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE

import json
import graphviz
import os


class Graph:
    """A graph from a Logpickr project, created with the parent Project's ID, a list of vertices and a list of edges
    """

    def __init__(self, project_id: str, vertices: list, edges: list):
        """

        :param project_id: the ID of the parent project
        :param vertices: the list of vertices
        :param edges: the list of edges
        """
        self.project_id = project_id
        self.vertices = vertices
        self.edges = edges

    @staticmethod
    def from_json(project_id, jsstring):
        """Static method that creates a Graph based on the json representation returned by the Logpickr API

        :param project_id: the ID of the project this graph is in
        :param jsstring: the json string we want to parse the graph from
        """
        jgraph = json.loads(jsstring)
        jverts = jgraph["vertices"]
        jedges = jgraph["edges"]
        vertices = [Vertex(vertex["id"], vertex["name"], vertex["category"]) if "category" in vertex.keys()
                    else Vertex(vertex["id"], vertex["name"]) for vertex in jverts]
        edges = []
        for edge in jedges:
            source = next((x for x in vertices if x.id == edge["source"]), None)
            dest = next((x for x in vertices if x.id == edge["destination"]), None)
            if source is not None and dest is not None:
                edges.append(Edge(edge["id"], source, dest))
            else:
                raise Exception("Invalid edge")

        return Graph(project_id, vertices, edges)

    def display(self):
        """Renders and displays the graph using Graphviz"""
        graphname = str(self).split("x")[-1].strip(">")  # Name is basically the pointer
        dot = graphviz.Digraph(name=graphname, format="svg")

        for e in self.edges:
            vs = e.source
            vd = e.destination
            nodeshape = "ellipse"
            vsname = vs.name
            if vs.is_gateway:
                nodeshape = "diamond"
                vsname = "×" if "XOR" in vs.category else "+"
            elif vs.name == "START":
                nodeshape = "doublecircle"
            dot.node(vs.graphviz_id, vsname, shape=nodeshape, style="filled", fillcolor=vs.color)

            vdname = vd.name
            nodeshape = "ellipse"
            if vd.is_gateway:
                nodeshape = "diamond"
                vdname = "×" if "XOR" in vd.category else "+"
            elif vd.name == "END":
                nodeshape = "doublecircle"
            dot.node(vd.graphviz_id, vdname, shape=nodeshape, style="filled", fillcolor=vd.color)

            dot.edge(vs.graphviz_id, vd.graphviz_id)

        if not os.path.isdir(".lpk_graphs"):
            os.makedirs(".lpk_graphs")

        dot.render(f".lpk_graphs/graph{graphname}.gv", view=True)


class GraphInstance(Graph):
    """A graph instance from a Logpickr project, created with the parent Project's ID, a list of vertex instances and a list of edge instances
    """

    def __init__(self, project_id: str, vertices: list, edges: list, rework_total: int, concurrency_rate: float):
        super().__init__(project_id, vertices, edges)
        self.rework_total = rework_total
        self.concurrency_rate = concurrency_rate

    @staticmethod
    def from_json(project_id, jgraph):
        """Static method that creates a GraphInstance based on the json representation returned by the Logpickr API

        :param project_id: the ID of the project the graph is in
        :param jgraph: the json dictionary containing the graph data"""
        jverts = jgraph["vertexInstances"]
        jedges = jgraph["edgeInstances"]

        vertices = [VertexInstance.from_json(v) for v in jverts]
        for vertex in vertices:
            # replace the list of "ids" with a list of the proper objects
            oldconcurr = vertex.concurrent_vertices
            vertex.concurrent_vertices = [v for v in vertices if (v.name + str(v.event_instance)) in oldconcurr]
        edges = [EdgeInstance.from_json(e, vertices) for e in jedges]

        for edge in edges:
            concurrent_ids = edge.concurrent_edges
            edge.concurrent_edges = [e for e in edges if (edge_to_str(e) in concurrent_ids and e != edge)]

        return GraphInstance(project_id, vertices, edges, jgraph["reworkTotal"], jgraph["concurrencyRate"])


category_dict = {
    "start": "START",
    "end": "END",
    "gateway_and_split": "AND_SPLIT",
    "gateway_xor_split": "XOR_SPLIT",
    "gateway_and_join": "AND_JOIN",
    "gateway_xor_join": "XOR_JOIN",
}


class Vertex:
    """Vertex of a Logpicker Graph.
    """

    def __init__(self, vid: str, name: str, category: str = None, color: str = "white", parent: Graph = None):
        """Creates a Vertex

        :param vid: the vertex's ID
        :param name: the vertex's name
        :param category: the vertex's category. Can be none, in which case the category will be extrapolated from the name
        :param color: the color you want the vertex to have in the displayed graph, white by default
        :param parent: the graph the vertex belongs to. Can be useful for graph operations. None by default"""
        self.id = vid
        self.name = name
        self.category = category if category in category_dict.values()\
            else (category_dict.get(category.lower(), "TASK") if category else category_dict.get(name.lower(), "TASK"))
        self.is_gateway = self.category.find('AND') >= 0 or self.category.find('XOR') >= 0
        self.color = color
        self.parent = parent

    @property
    def graphviz_id(self):
        """Generates a unique id for the Vertex, to be used in displaying it through graphviz"""
        return self.name.replace(" ", "") + self.id


class VertexInstance(Vertex):
    """Vertex of a Logpickr Graph Instance. Has a unique id, a name, an event instance and a lis t of concurrent vertices"""

    def __init__(self, vid: str, name: str, event_instance: int, concurrent_vertices: list, category: str = None):
        super().__init__(vid, name, category)
        self.event_instance = event_instance
        self.concurrent_vertices = concurrent_vertices

    @staticmethod
    def from_json(jvert):
        """Static method that creates a VertexInstance from its json representation"""
        # If there are no concurrent vertices, there's going to be no concurrentVertices argument, instead of an empty
        # list, so I have to do this nonsense instead to make sure I don't get key errors
        conc = [v["name"] + str(v["eventInstance"]) for v in
                jvert["concurrentVertices"]] if "concurrentVertices" in jvert.keys() else []
        # Note: the concurrent vertices are currently just ids constructed from the event instance and name. While it
        # should be unique, this method is only called right before these weird ids get replaced with actual pointers
        return VertexInstance(jvert["id"], jvert["name"], jvert["eventInstance"], conc,
                              jvert["category"]) if "catergory" in jvert.keys() else VertexInstance(jvert["id"],
                                                                                                    jvert["name"],
                                                                                                    jvert["eventInstance"],
                                                                                                    conc)

    @property
    def graphviz_id(self):
        """Generates a unique id for the Vertex, to be used in displaying it through graphviz"""
        return self.name.replace(" ", "") + self.id + str(self.event_instance)


class Edge:
    """Edge between two vertices of a Logpickr Graph. Has a unique id, a source and a destination 
    """

    def __init__(self, eid: str, source: Vertex, destination: Vertex):
        self.id = eid
        self.source = source
        self.destination = destination


class EdgeInstance:
    """Edge between two vertices of a Logpickr Graph Instance. Has a source and a destination, and a list of concurrent edges"""

    def __init__(self, source: VertexInstance, destination: VertexInstance, concurrent_edges: list):
        self.source = source
        self.destination = destination
        self.concurrent_edges = concurrent_edges

    @staticmethod
    def from_json(jedge, vertices):
        """Static method that created an EdgeInstance from its json representation"""
        conc = [edge_dict_to_str(e) for e in jedge["concurrentEdges"]] if "concurrentEdges" in jedge.keys() else []
        jedge_s = jedge["source"]
        jedge_d = jedge["destination"]
        source = next(v for v in vertices if v.id == jedge_s["id"] and v.event_instance == jedge_s["eventInstance"])
        dest = next(v for v in vertices if v.id == jedge_d["id"] and v.event_instance == jedge_d["eventInstance"])
        # Note: the concurrent edges are currently just ids constructed from the edge vertices' ids. While it
        # should be unique, this method is only called right before these weird ids get replaced with actual pointers
        return EdgeInstance(source, dest, conc)


def edge_dict_to_str(edge):
    """Helper method for comparison that creates a unique string from a json edge instance

    :param edge: the json dictionary to turn into a string"""
    csource = edge["source"]
    cdest = edge["destination"]
    return (str(csource["id"]) + csource["name"] + str(csource["eventInstance"]) +
            str(cdest["id"]) + cdest["name"] + str(cdest["eventInstance"]))


def edge_to_str(edge):
    """Helper method that creates a unique string from an EdgeInstance

    :param edge: the Edge to turn into a string"""
    csource = edge.source
    cdest = edge.destination
    return (str(csource.id) + csource.name + str(csource.event_instance) +
            str(cdest.id) + cdest.name + str(cdest.event_instance))
