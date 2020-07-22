# Apache License 2.0, Copyright 2020 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE

import pytest
from logpickr_sdk.workgroup import Workgroup, Project, Datasource
import requests as req

@pytest.fixture()
def ID(pytestconfig):
    return pytestconfig.getoption("id")

@pytest.fixture()
def SECRET(pytestconfig):
    return pytestconfig.getoption("key")
    
@pytest.fixture()
def PROJECT_ID(pytestconfig):
    return pytestconfig.getoption("project")


class TestWorkgroup:

    def test_create_workgroup(self, ID, SECRET):
        w = Workgroup(ID, SECRET)
        assert w.id == ID
        assert w.key == SECRET
        assert w.token != ""
        assert w._projects == []

    def test_wrong_login(self):
        with pytest.raises(Exception):
            assert Workgroup("a", "b")

    def test_projects(self, ID, SECRET):
        w = Workgroup(ID, SECRET)
        assert len(w.projects) > 0  # Since there should be projects in the workgroup

    def test_tables(self, ID, SECRET):
        w = Workgroup(ID, SECRET)
        assert len(w.datasources) > 0  # Since there should be projects in the workgroup




class TestProject:

    def test_create_project(self, ID, SECRET):
        wg = Workgroup(ID, SECRET)
        p = Project(PROJECT_ID, wg)
        assert p.id == PROJECT_ID
        assert p._graph is None
        assert len(p._graph_instances) == 0
        assert len(p._datasources) == 0
        assert p.owner is not None

    def test_graph(self, ID, SECRET, PROJECT_ID):
        wg = Workgroup(ID, SECRET)
        p = Project(PROJECT_ID, wg)
        assert p.graph is not None

    def test_graph_instances(self, ID, SECRET, PROJECT_ID):
        wg = Workgroup(ID, SECRET)
        p = Project(PROJECT_ID, wg)
        assert len(p.graph_instances) > 0

    def test_datasources(self, ID, SECRET, PROJECT_ID):
        wg = Workgroup(ID, SECRET)
        p = Project(PROJECT_ID, wg)
        assert len(p.datasources) > 0

    def test_add_file(self, ID, SECRET, PROJECT_ID):
        wg = Workgroup(ID, SECRET)
        p = Project(PROJECT_ID, wg)
        assert p.add_file("testdata.csv")


NAME = "22"
TYPE = "events"
HOST = "allinone"
PORT = "8082"


class TestDatasource:

    def test_create_datasource(self, ID, SECRET, PROJECT_ID):
        wg = Workgroup(ID, SECRET)
        p = Project(PROJECT_ID, wg)
        ds = Datasource(NAME, TYPE, HOST, PORT, p)
        assert ds.name == NAME
        assert ds.type == TYPE
        assert ds.host == HOST
        assert ds.port == PORT
        assert ds.project == p

        # TODO: add some tests to make sure you can't do forbidden things like create tables, add columns, edit values
        # Basically make sure you're in read-only mode

    def test_colums(self, ID, SECRET, PROJECT_ID):
        wg = Workgroup(ID, SECRET)
        p = Project(PROJECT_ID, wg)
        ds = p.datasources[0]
        assert ds.columns != []
