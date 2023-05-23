# Apache License 2.0, Copyright 2020 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE
from pathlib import Path

import pytest
from igrafx_mining_sdk import Project
from igrafx_mining_sdk.workgroup import Workgroup
from igrafx_mining_sdk.graph import Graph


class TestGraph:
    """Tests for the Graph class.
    ID, SECRET, API, AUTH and PROJECT_ID are pytest fixtures defined in conftest.py file.
    """

    def test_graph_creation(self, ID, SECRET, API, AUTH, PROJECT_ID):
        """Test the creation of a Graph object."""
        w = Workgroup(ID, SECRET, API, AUTH)
        project = Project(PROJECT_ID, w.api_connector)
        g = project.graph()
        assert isinstance(g, Graph)

    def test_graph_instance(self, ID, SECRET, API, AUTH, PROJECT_ID):
        """Test the creation of a Graph object."""
        w = Workgroup(ID, SECRET, API, AUTH)
        project = Project(PROJECT_ID, w.api_connector)
        g = project.get_graph_instances(limit=1)[0]
        assert g.rework_total is not None
        assert g.concurrency_rate is not None

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
