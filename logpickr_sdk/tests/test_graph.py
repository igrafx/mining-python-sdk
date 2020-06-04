from logpickr_sdk.workgroup import Workgroup, Project, Datasource
from logpickr_sdk.graph import Graph, Vertex, Edge
from random import randint, choice

ID = "fb6eeb8f-574c-469b-8eef-276ed6cfa823"
SECRET = "c0927608-47cf-465f-a683-6ec2bae48e1d"

try:
    w = Workgroup(ID, SECRET)
    project = Project(w.projects[0])  # Creates a project with the first possible ID
except Exception as e:
    project = Project(0)

class TestGraph:
    def test_graph_creation(self):
        g = project.graph
        assert g.parent_id == project.id
        assert len(g.vertices) > 0
        assert len(g.edges) > 0
        assert g.rework_total == -1  # Since this is a graph, not a graph instance
        assert g.concurrency_rate == -1

    def test_graph_instance(self):
        g = project.graph_instances[0]
        assert g.rework_total >= 0
        assert g.concurrency_rate >= 0

    def test_from_json(self):
        text = open("graph.json").readline().strip("\n")
        g = Graph.from_json(0, text)
        assert len(g.vertices) == 6
        assert len(g.edges) == 10


class TestVertex:

    def random_vertex(self):
        g = project.graph
        return choice(g.vertices)

    def random_vertex_instance(self):
        g = project.graph_instances[0]
        return choice(g.vertices)

    def test_created_vertex(self):
        v = self.random_vertex()
        assert v.id is not None
        assert v.name != ""
        assert v.event_instance == -1  # vertex non instancié
        assert v.concurrent_vertices is None
        assert v.parent == project.graph

    def test_vertex_instance(self):
        v = self.random_vertex_instance()
        assert v.event_instance != -1
        assert v.concurrent_vertices is not None


class TestEdge:

    def random_edge(self):
        g = project.graph
        return choice(g.edges)

    def random_edge_instance(self):
        g = project.graph_instances[0]
        return choice(g.edges)

    def test_created_edge(self):
        e = self.random_edge()
        assert e.id is not None
        assert e.parent == project.graph
        assert e.source is not None
        assert type(e.source) == Vertex
        assert e.destination is not None
        assert type(e.destination) == Vertex
        assert e.concurrent_edges is None

    def test_edge_instance(self):
        e = self.random_edge_instance()
        assert e.concurrent_edges is not None