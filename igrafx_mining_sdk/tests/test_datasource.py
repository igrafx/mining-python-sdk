# Apache License 2.0, Copyright 2020 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE

import pytest
from igrafx_mining_sdk import Project
from igrafx_mining_sdk.datasource import Datasource
from igrafx_mining_sdk.workgroup import Workgroup

NAME = "22"
TYPE = "events"
HOST = "allinone"
PORT = "8082"


class TestDatasource:
    """Class for testing Datasource class.
    ID, SECRET, API, AUTH and PROJECT_ID are pytest fixtures defined in conftest.py file.
    """

    def test_create_datasource(self, ID, SECRET, API, AUTH, PROJECT_ID):
        """Test creating a Datasource"""
        wg = Workgroup(ID, SECRET, API, AUTH)
        ds = Datasource(NAME, TYPE, HOST, PORT, wg.api_connector)
        assert isinstance(ds, Datasource)

    def test_columns(self, ID, SECRET, API, AUTH,  PROJECT_ID):
        """Test the columns of a Datasource"""
        wg = Workgroup(ID, SECRET, API, AUTH)
        p = Project(PROJECT_ID, wg.api_connector)
        ds = p.edges_datasource
        assert ds.columns != []

    def test_non_empty_ds(self, ID, SECRET, API, AUTH, PROJECT_ID):
        """Test that the datasource is not empty"""
        wg = Workgroup(ID, SECRET, API, AUTH)
        p = Project(PROJECT_ID, wg.api_connector)
        for pr in wg.projects:
            try:
                len(pr.process_keys)
                p = pr
                break
            except Exception:
                continue

        ds = p.nodes_datasource
        assert 0 < len(ds.load_dataframe(load_limit=10)) <= 10

    def test_read_only(self, ID, SECRET, API, AUTH, PROJECT_ID):
        """Test that the datasource is read only"""
        wg = Workgroup(ID, SECRET, API, AUTH)
        p = Project(PROJECT_ID, wg.api_connector)
        for pr in wg.projects:
            try:
                len(pr.process_keys)
                p = pr
                break
            except Exception:
                continue

        ds = p.edges_datasource
        pk = p.process_keys[0]
        # Test that all of those requests will fail
        with pytest.raises(Exception):
            assert ds.request(f'DELETE FROM "{ds.name}" WHERE processkey = \'{pk}\'')
        with pytest.raises(Exception):
            assert ds.request(f'INSERT INTO "{ds.name}"(processkey) VALUES (\'{pk}\')')
        with pytest.raises(Exception):
            assert ds.request(f'DROP TABLE "{ds.name}"')
            ds.drop()
        with pytest.raises(Exception):
            assert ds.request(f'ALTER TABLE "{ds.name}" DROP COLUMN processkey')

    def test_close(self, ID, SECRET, API, AUTH, PROJECT_ID):
        wg = Workgroup(ID, SECRET, API, AUTH)
        ds = Datasource(NAME, TYPE, HOST, PORT, wg.api_connector)
        # ensure connection and cursor are none
        assert ds._cursor is None
        assert ds._connection is None

        # initialize both cursor and connection
        cursor = ds.cursor
        connection = ds.connection
        assert cursor is not None
        assert connection is not None

        # close cursor and connection then check that they are none again
        ds.close()
        assert ds._cursor is None
        assert ds._connection is None
