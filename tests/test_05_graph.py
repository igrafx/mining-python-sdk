# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE
from pathlib import Path
import pytest
from igrafx_mining_sdk.graph import Graph, GraphInstance


class TestGraph:
    """Tests for the Graph class.
    Workgroup and project are pytest fixtures defined in conftest.py file.
    """
    @pytest.mark.dependency(depends=['project_contains_data'], scope='session')
    def test_graph_creation(self):
        """Test the creation of a Graph object."""
        g = pytest.project.graph()
        assert isinstance(g, Graph)

    @pytest.mark.dependency(depends=['project_contains_data'], scope='session')
    def test_graph_instance(self):
        """Test the creation of a Graph object."""

        # This method uses the process_keys method and is also based on the connection with jdbc
        list1 = pytest.project.get_graph_instances(limit=10, shuffle=False)
        list2 = pytest.project.get_graph_instances(limit=10, shuffle=True)
        assert len(list1) == len(list2)
        graph_instance = list1[0]
        assert graph_instance.rework_total is not None
        assert graph_instance.concurrency_rate is not None

    def test_graph_with_bad_edges(self):
        """Test a graph that has bad edges."""
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'graphs' / 'graph_with_invalid_edges.json'
        with pytest.raises(Exception):
            assert Graph.from_json(14, str(file_path))

    def test_from_json(self):
        """Test the creation of a Graph object from a json string and display."""
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'graphs' / 'graph.json'
        g = Graph.from_json(0, str(file_path))
        assert len(g) > 0

    def test_getattr_delegation(self):
        """Test that attribute access is delegated to the underlying NetworkX graph which triggers the __getattr__ method."""
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'graphs' / 'graph.json'
        g = Graph.from_json(0, str(file_path))
        # Accessing .nodes triggers __getattr__ delegation to the NetworkX DiGraph
        assert len(g.nodes) > 0

    def test_graph_property(self):
        """Test that the graph property returns the graph attributes dictionary, covering the graph property."""
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'graphs' / 'graph.json'
        g = Graph.from_json(0, str(file_path))
        assert 'project_id' in g.graph
        assert g.graph['project_id'] == 0

    def test_graph_instance_from_json(self):
        """ Calls GraphInstance.from_json() with the existing test data file, covering lines 89-91.
        Asserts the returned object has correct rework_total (4) and concurrency_rate (~0.0357)"""
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'graphs' / 'graph_with_invalid_edges.json'
        gi = GraphInstance.from_json("test_project", str(file_path))
        assert isinstance(gi, GraphInstance)
        assert gi.rework_total == 4
        assert gi.concurrency_rate == pytest.approx(0.0357, abs=0.001)
        assert len(gi) > 0
