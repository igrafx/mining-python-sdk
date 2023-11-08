# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE
import time
import pytest
from pathlib import Path
from igrafx_mining_sdk.project import FileStructure
from igrafx_mining_sdk.column_mapping import Column, ColumnType, ColumnMapping, FileType
from igrafx_mining_sdk.datasource import Datasource


class TestProject:
    """Tests for Project class.
    Workgroup and project are pytest fixtures defined in conftest.py file.
    """
    @pytest.mark.dependency(depends=['project'], scope='session')
    def test_project_exists(self):
        """Test that a project exists."""
        project_exists = pytest.project.exists
        assert project_exists is True

    @pytest.mark.dependency(depends=['project'], scope='session')
    def test_get_project_name(self):
        """ Test that the project name is returned and correct."""
        project_name = pytest.project.get_project_name()
        assert project_name == "Test Project"

    @pytest.mark.dependency(depends=['project', 'column_mapping'], scope='session')
    def test_column_mapping_dont_exists(self):
        """Test that a column mapping can be created."""
        assert not pytest.project.column_mapping_exists

    @pytest.mark.dependency(name='add_column_mapping', depends=['project', 'column_mapping'], scope='session')
    def test_add_column_mapping(self):
        """Test that a column mapping can be created."""
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
        assert pytest.project.add_column_mapping(filestructure, column_mapping)

    @pytest.mark.dependency(depends=['project'], scope='session')
    def test_get_mapping_infos(self):
        """Test that the correct mapping infos can be returned"""
        assert pytest.project.get_mapping_infos()

    @pytest.mark.dependency(name='reset', depends=['project'], scope='session')
    def test_reset(self):
        """Test that a project can be reset."""
        assert pytest.project.reset()

    @pytest.mark.dependency(depends=['reset', 'add_column_mapping'])
    def test_add_xlsx_file(self):
        """Test that an xlsx file can be added to a project."""
        pytest.project.reset()
        filestructure = FileStructure(
            file_type=FileType.xlsx,
            sheet_name="Sheet1"
        )
        column_list = [
            Column('Case ID', 0, ColumnType.CASE_ID),
            Column('Start Timestamp', 1, ColumnType.TIME, time_format='yyyy/MM/dd HH:mm:ss.SSS'),
            Column('Complete Timestamp', 2, ColumnType.TIME, time_format='yyyy/MM/dd HH:mm:ss.SSS'),
            Column('Activity', 3, ColumnType.TASK_NAME),
            Column('Ressource', 4, ColumnType.DIMENSION),
        ]
        column_mapping = ColumnMapping(column_list)
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'tables' / 'p2pShortExcel.xlsx'
        assert pytest.project.add_column_mapping(filestructure, column_mapping)
        assert pytest.project.add_file(str(file_path))

    @pytest.mark.dependency(depends=['reset', 'add_column_mapping'])
    def test_add_xls_file(self):
        """Test that an xls file can be added to a project."""
        pytest.project.reset()
        filestructure = FileStructure(
            file_type=FileType.xls,
            sheet_name="Sheet1"
        )
        column_list = [
            Column('Case ID', 0, ColumnType.CASE_ID),
            Column('Start Timestamp', 1, ColumnType.TIME, time_format='yyyy/MM/dd HH:mm:ss.SSS'),
            Column('Complete Timestamp', 2, ColumnType.TIME, time_format='yyyy/MM/dd HH:mm:ss.SSS'),
            Column('Activity', 3, ColumnType.TASK_NAME),
            Column('Ressource', 4, ColumnType.DIMENSION),
        ]
        column_mapping = ColumnMapping(column_list)
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'tables' / 'p2pShortExcel.xls'
        assert pytest.project.add_column_mapping(filestructure, column_mapping)
        assert pytest.project.add_file(str(file_path))

    @pytest.mark.dependency(name='add_csv_file', depends=['reset', 'add_column_mapping'], scope='session')
    def test_add_csv_file(self):
        """Test that a csv file can be added to a project."""
        pytest.project.reset()
        filestructure = FileStructure(
            file_type=FileType.csv,
        )
        column_list = [
            Column('Case ID', 0, ColumnType.CASE_ID),
            Column('Activity', 1, ColumnType.TASK_NAME),
            Column('Start Date', 2, ColumnType.TIME, time_format='dd/MM/yyyy HH:mm'),
            Column('End Date', 3, ColumnType.TIME, time_format='dd/MM/yyyy HH:mm'),
        ]
        column_mapping = ColumnMapping(column_list)
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'tables' / 'testdata.csv'
        assert pytest.project.add_column_mapping(filestructure, column_mapping)
        assert pytest.project.add_file(str(file_path))

    @pytest.mark.dependency(name='project_contains_data', depends=['add_csv_file'])
    def test_project_contains_data(self):
        count = 0
        while pytest.project.nodes_datasource.__class__ != Datasource:
            time.sleep(3)
            count += 1
            if count > 100:
                assert False, 'Timeout reached'
        assert True



    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_datasources_types(self):
        """Test the types of the datasources"""
        assert pytest.project.nodes_datasource.__class__ == Datasource
        assert pytest.project.edges_datasource.__class__ == Datasource
        assert pytest.project.cases_datasource.__class__ == Datasource

    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_get_project_variants(self):
        """Test that the project correct variants are returned."""
        assert pytest.project.get_project_variants(1, 3)
