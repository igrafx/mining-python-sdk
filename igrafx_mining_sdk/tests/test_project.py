# Apache License 2.0, Copyright 2020 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE

from igrafx_mining_sdk import Project, FileStructure, FileType
from igrafx_mining_sdk.column_mapping import Column, ColumnType, ColumnMapping
from igrafx_mining_sdk.datasource import Datasource
from igrafx_mining_sdk.workgroup import Workgroup

import pytest


class TestProject:
    """Tests for Project class.
    ID, SECRET, API, AUTH and PROJECT_ID are pytest fixtures defined in conftest.py file.
    """
    def test_project_with_nonexistent_pid(self, ID, SECRET, API, AUTH, PROJECT_ID):
        """Test a project with a non-existent id."""
        w = Workgroup(ID, SECRET, API, AUTH)
        project = Project("00000000-0000-0000-0000-000000000000", w.api_connector)
        assert not project.exists

    def test_create_project(self, ID, SECRET, API, AUTH,  PROJECT_ID):
        """Test the creation of a project."""
        wg = Workgroup(ID, SECRET, API, AUTH)
        p = Project(PROJECT_ID, wg.api_connector)
        assert isinstance(p, Project)

    def test_graph(self, ID, SECRET, API, AUTH, PROJECT_ID):
        """Test the creation of a graph."""
        wg = Workgroup(ID, SECRET, API, AUTH)
        p = Project(PROJECT_ID, wg.api_connector)
        assert p.graph is not None

    def test_graph_instances(self, ID, SECRET, API, AUTH, PROJECT_ID):
        """Test the graph instances."""
        wg = Workgroup(ID, SECRET, API, AUTH)
        p = Project(PROJECT_ID, wg.api_connector)
        assert len(p.get_graph_instances(limit=3, shuffle=False)) == 3
        assert len(p.get_graph_instances(limit=3, shuffle=True)) == 3

    def test_datasources_types(self, ID, SECRET, API, AUTH, PROJECT_ID):
        """Test the types of the datasources"""
        wg = Workgroup(ID, SECRET, API, AUTH)
        p = Project(PROJECT_ID, wg.api_connector)
        assert p.nodes_datasource.__class__ == Datasource
        assert p.edges_datasource.__class__ == Datasource
        assert p.cases_datasource.__class__ == Datasource

    @pytest.mark.dependency()
    def test_reset(self, API, AUTH):
        """Test that a project can be reset."""
        wg = Workgroup("ed77e5ff-978b-4aca-8bad-40834b1b3ff6", "1dd9c5d1-8aa5-4662-8fab-6bcff3bf4481", API, AUTH)
        p = Project("c86f5f16-8d46-43d9-a1fd-0e804a31d1cb", wg.api_connector)
        assert p.reset()

    @pytest.mark.dependency(depends=["TestProject::test_reset"])  # Will skip test if test_reset fails
    def test_add_column_mapping(self, API, AUTH):
        """Test that a column mapping can be created."""
        wg = Workgroup("ed77e5ff-978b-4aca-8bad-40834b1b3ff6", "1dd9c5d1-8aa5-4662-8fab-6bcff3bf4481", API, AUTH)
        p = Project("c86f5f16-8d46-43d9-a1fd-0e804a31d1cb", wg.api_connector)
        filestructure = FileStructure(
            file_type=FileType.xlsx,
            sheet_name="Sheet1"
        )
        column_list = [
            Column('case_id', 0, ColumnType.CASE_ID),
            Column('task_name', 1, ColumnType.TASK_NAME),
            Column('time', 2, ColumnType.TIME, time_format='%Y-%m-%dT%H:%M')
        ]
        column_mapping = ColumnMapping(column_list)
        assert p.add_column_mapping(filestructure, column_mapping)

    def test_column_mapping_exists(self, API, AUTH):
        """Test that a column mapping can be created."""
        wg = Workgroup("ed77e5ff-978b-4aca-8bad-40834b1b3ff6", "1dd9c5d1-8aa5-4662-8fab-6bcff3bf4481", API, AUTH)
        p = Project("c86f5f16-8d46-43d9-a1fd-0e804a31d1cb", wg.api_connector)
        assert p.column_mapping_exists

    def test_mapping_infos(self, API, AUTH):
        wg = Workgroup("ed77e5ff-978b-4aca-8bad-40834b1b3ff6", "1dd9c5d1-8aa5-4662-8fab-6bcff3bf4481", API, AUTH)
        p = Project("c86f5f16-8d46-43d9-a1fd-0e804a31d1cb", wg.api_connector)
        print(p.mapping_infos)
        assert p.mapping_infos()

    def test_add_csv_file(self, API, AUTH):
        wg = Workgroup("ed77e5ff-978b-4aca-8bad-40834b1b3ff6", "1dd9c5d1-8aa5-4662-8fab-6bcff3bf4481", API, AUTH)
        p = Project("c86f5f16-8d46-43d9-a1fd-0e804a31d1cb", wg.api_connector)
        p.reset()
        filestructure = FileStructure(
            file_type=FileType.csv,
        )
        column_list = [
            Column('Case ID', 0, ColumnType.CASE_ID),
            Column('Activity', 1, ColumnType.TASK_NAME),
            Column('Start Date', 2, ColumnType.TIME, time_format='%d/%m/%Y %H:%M'),
            Column('End Date', 3, ColumnType.TIME, time_format='%d/%m/%Y %H:%M'),
        ]
        column_mapping = ColumnMapping(column_list)
        assert p.add_column_mapping(filestructure, column_mapping)
        assert p.add_file("data/tables/testdata.csv")

    def test_add_xlsx_file(self, API, AUTH):
        """Test that an xlsx file can be added to a project."""
        wg = Workgroup("ed77e5ff-978b-4aca-8bad-40834b1b3ff6", "1dd9c5d1-8aa5-4662-8fab-6bcff3bf4481", API, AUTH)
        p = Project("c86f5f16-8d46-43d9-a1fd-0e804a31d1cb", wg.api_connector)
        p.reset()
        filestructure = FileStructure(
            file_type=FileType.xlsx,
            sheet_name="Sheet1"
        )
        column_list = [
            Column('Case ID', 0, ColumnType.CASE_ID),
            Column('Start Timestamp', 1, ColumnType.TIME, time_format='%Y/%m/%d %H:%M:%S.%f'),
            Column('Complete Timestamp', 2, ColumnType.TIME, time_format='%Y/%m/%d %H:%M:%S.%f'),
            Column('Activity', 3, ColumnType.TASK_NAME),
            Column('Ressource', 4, ColumnType.DIMENSION),
        ]
        column_mapping = ColumnMapping(column_list)
        assert p.add_column_mapping(filestructure, column_mapping)
        assert p.add_file("data/tables//p2pShortExcel.xlsx")

    def test_add_xls_file(self, API, AUTH):
        """Test that an xls file can be added to a project."""
        wg = Workgroup("ed77e5ff-978b-4aca-8bad-40834b1b3ff6", "1dd9c5d1-8aa5-4662-8fab-6bcff3bf4481", API, AUTH)
        p = Project("c86f5f16-8d46-43d9-a1fd-0e804a31d1cb", wg.api_connector)
        p.reset()
        filestructure = FileStructure(
            file_type=FileType.xls,
            sheet_name="Sheet1"
        )
        column_list = [
            Column('Case ID', 0, ColumnType.CASE_ID),
            Column('Start Timestamp', 1, ColumnType.TIME, time_format='%Y/%m/%d %H:%M:%S.%f'),
            Column('Complete Timestamp', 2, ColumnType.TIME, time_format='%Y/%m/%d %H:%M:%S.%f'),
            Column('Activity', 3, ColumnType.TASK_NAME),
            Column('Ressource', 4, ColumnType.DIMENSION),
        ]
        column_mapping = ColumnMapping(column_list)
        assert p.add_column_mapping(filestructure, column_mapping)
        assert p.add_file("data/tables//p2pShortExcel.xls")
