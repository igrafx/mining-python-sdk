# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE
import os
import pytest
import pandas as pd
from igrafx_mining_sdk.datasource import Datasource


NAME = os.environ.get('NAME')
TYPE = os.environ.get('TYPE')


class TestDatasource:
    """Class for testing Datasource class.
    Workgroup and project are pytest fixtures defined in conftest.py file.
    """
    @pytest.mark.dependency(depends=['workgroup'], scope='session')
    def test_create_datasource(self):
        """Test creating a Datasource"""
        ds = Datasource(NAME, TYPE, pytest.workgroup.api_connector)
        assert isinstance(ds, Datasource)

    @pytest.mark.dependency(depends=['project_contains_data'], scope='session')
    def test_columns(self):
        """Test the columns of a Datasource"""
        ds = pytest.project.edges_datasource
        # This method uses the columns method and is also based on the connection with jdbc
        assert ds.columns != []

    @pytest.mark.dependency(depends=['project_contains_data'], scope='session')
    def test_load_ds(self):
        """Test that the datasource is not empty and respects the load limit."""
        ds = pytest.project.cases_datasource
        # Load a small number of rows
        load_limit = 10
        df = ds.load_dataframe(load_limit=load_limit)
        # Ensure the result is a DataFrame
        assert isinstance(df, pd.DataFrame)

    @pytest.mark.dependency(depends=['project_contains_data'], scope='session')
    def test_non_empty_ds(self):
        """Test that the datasource is not empty"""
        ds = pytest.project.nodes_datasource
        # This method uses the load_dataframe method and is also based on the connection with jdbc
        df = ds.load_dataframe(load_limit=10)
        assert not df.empty
        assert 0 < len(df) <= 10

    @pytest.mark.dependency(depends=['project_contains_data'], scope='session')
    def test_request(self):
        """ Test that the request method works """
        ds = pytest.project.nodes_datasource
        simple_sql = f'SELECT * FROM "{ds.name}" LIMIT 1'
        df = ds.request(simple_sql)
        # Verify that the result is a pandas DataFrame
        assert isinstance(df, pd.DataFrame)
        # Verify that at least one row is returned
        assert not df.empty

    @pytest.mark.dependency(depends=['project_contains_data'], scope='session')
    def test_read_only(self):
        """Test that the datasource is read only"""
        ds = pytest.project.edges_datasource
        # This method uses the process_keys method and is also based on the connection with jdbc.
        pk = pytest.project.process_keys[0]
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

    @pytest.mark.dependency(depends=['workgroup'], scope='session')
    def test_close(self):
        """Test that the Datasource can be closed"""
        ds = Datasource(NAME, TYPE, pytest.workgroup.api_connector)
        # ensure connection and cursor are none
        assert ds._cursor is None
        assert ds._connection is None

        # initialize both cursor and connection
        cursor = ds.cursor
        connection = ds.connection
        assert cursor is not None
        assert connection is not None

        # close cursor and connection then check that they are none again
        ds.close_ds_connection()
        assert ds._cursor is None
        assert ds._connection is None
