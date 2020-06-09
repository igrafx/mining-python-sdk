import pytest
from logpickr_sdk.workgroup import Workgroup, Project, Datasource
import requests as req

ID = "fb6eeb8f-574c-469b-8eef-276ed6cfa823"
SECRET = "72deb3cf-502d-4d8e-ab69-513d3c2694fa"


class TestWorkgroup:

    def test_create_workgroup(self):
        w = Workgroup(ID, SECRET)
        assert w.id == ID
        assert w.key == SECRET
        assert w.token != ""
        assert w._projects == []

    def test_wrong_login(self):
        w = Workgroup("a", "b")
        assert w.token == ""

    def test_projects(self):
        w = Workgroup(ID, SECRET)
        assert len(w.projects) > 0  # Since there should be projects in the workgroup

    def test_tables(self):
        w = Workgroup(ID, SECRET)
        assert len(w.tables) > 0  # Since there should be projects in the workgroup


PROJECT_ID = 16


class TestProject():

    def test_create_project(self):
        p = Project(PROJECT_ID, Workgroup(ID, SECRET))
        assert p.id == PROJECT_ID
        assert p._graph is None
        assert len(p._graph_instances) == 0
        assert len(p._tables) == 0
        assert p.owner is not None

    def test_graph(self):
        p = Project(PROJECT_ID)
        assert p.graph is not None

    def test_graph_instances(self):
        p = Project(PROJECT_ID)
        assert len(p.graph_instances) > 0

    def test_datasources(self):
        p = Project(PROJECT_ID)
        assert len(p.datasources) > 0

    def test_add_file(self):
        p = Project(PROJECT_ID)
        assert p.add_file("testdata.csv")


# TODO: fill this in with the appropriate values
NAME = ""
TYPE = ""
HOST = ""
PORT = ""


class TestDatasource:

    def test_create_datasource(self):
        ds = Datasource(NAME, TYPE, HOST, PORT)
        assert ds.name == NAME
        assert ds.type == TYPE
        assert ds.host == HOST
        assert ds.port == PORT
