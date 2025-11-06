# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE
import time
from unittest.mock import MagicMock
from pathlib import Path
from datetime import datetime
import uuid
import pytest
from igrafx_mining_sdk.project import FileStructure
from igrafx_mining_sdk.column_mapping import Column, ColumnType, ColumnMapping, FileType
from igrafx_mining_sdk.datasource import Datasource
from igrafx_mining_sdk.api_connector import APIConnector


class TestProject:
    """Tests for Project class.
    Workgroup and project are pytest fixtures defined in conftest.py file.
    """

    @pytest.fixture
    def api_connector(self):
        """Mock the APIConnector class."""
        return MagicMock()

    @pytest.mark.dependency(depends=['project'], scope='session')
    def test_project_exists(self):
        """Test that a project exists."""
        project_exists = pytest.project.exists
        assert project_exists is True

    @pytest.mark.dependency(depends=['project'], scope='session')
    def test_unarchive(self):
        """Test that a project can be unarchived."""
        assert pytest.project.unarchive()

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
            file_type=FileType.XLSX,
            sheet_name="Sheet1"
        )
        column_list = [
            Column('case_id', 0, ColumnType.CASE_ID),
            Column('task_name', 1, ColumnType.TASK_NAME),
            Column('time', 2, ColumnType.TIME, time_format="yyyy-MM-dd'T'HH:mm")
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
        """Test that a xlsx file can be added to a project."""
        pytest.project.reset()
        filestructure = FileStructure(
            file_type=FileType.XLSX,
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
        """Test that a xls file can be added to a project."""
        pytest.project.reset()
        filestructure = FileStructure(
            file_type=FileType.XLS,
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
            file_type=FileType.CSV,
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

    @pytest.mark.dependency(name='add_csv_file', depends=['reset', 'add_column_mapping'], scope='session')
    def test_add_zip_csv_file(self):
        """Test that a zip file can be added to a project."""
        pytest.project.reset()
        filestructure = FileStructure(
            file_type=FileType.CSV,
        )
        column_list = [
            Column('Case ID', 0, ColumnType.CASE_ID),
            Column('Activity', 1, ColumnType.TASK_NAME),
            Column('Start Date', 2, ColumnType.TIME, time_format='dd/MM/yyyy HH:mm'),
            Column('End Date', 3, ColumnType.TIME, time_format='dd/MM/yyyy HH:mm'),
        ]
        column_mapping = ColumnMapping(column_list)
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'tables' / 'testdata_zip.zip'
        assert pytest.project.add_column_mapping(filestructure, column_mapping)
        assert pytest.project.add_file(str(file_path))

    def test_get_column_mapping_not_exist(self):
        """Test that if there is no column mapping, a ValueError is raised"""
        pytest.project.reset()
        with pytest.raises(ValueError):
            pytest.project.get_column_mapping()

    @pytest.mark.dependency(name='add_csv_file', depends=['reset', 'add_column_mapping'], scope='session')
    def test_add_csv_file_from_json_column_mapping(self):
        """Test that a csv file can be added to a project. Using a json column mapping that contains grouped tasks"""
        pytest.project.reset()
        filestructure = FileStructure(
            file_type=FileType.CSV,
        )
        column_dict = '''{
        "col1": {"name": "Case ID", "columnIndex": "0", "columnType":   "CASE_ID"},
        "col2": {"name": "Activity", "columnIndex": "1", "columnType": "TASK_NAME", "groupedTasksColumns": [1, 2, 3]},
        "col3": {"name": "Start Date", "columnIndex": "2", "columnType": "TIME", "format": "dd/MM/yyyy HH:mm"},
        "col4": {"name": "End Date", "columnIndex": "3", "columnType": "TIME", "format": "dd/MM/yyyy HH:mm"},
        "col5": {"name": "Price", "columnIndex": "4", "columnType": "METRIC", "isCaseScope": false,
        "groupedTasksAggregation": "SUM", "aggregation": "SUM", "unit": "円"},
        "col6": {"name": "Forme", "columnIndex": "5", "columnType": "DIMENSION", "isCaseScope": false,
         "groupedTasksAggregation": "LAST", "aggregation": "DISTINCT"}
        }'''
        column_mapping = ColumnMapping.from_json(column_dict)
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'tables' / 'testdata.csv'
        assert pytest.project.add_column_mapping(filestructure, column_mapping)
        assert pytest.project.add_file(str(file_path))

    @pytest.mark.dependency(name='add_csv_file', depends=['reset', 'add_column_mapping'], scope='session')
    def test_get_column_mapping_add_csv_groupedtasks(self):
        """Test that the the column mapping that was recuperated can be used to add a csv file containing grouped_tasks"""
        column_mapping_dict = pytest.project.get_column_mapping()
        pytest.project.reset()
        filestructure = FileStructure(
            file_type=FileType.CSV,
        )
        column_mapping = ColumnMapping.from_json(column_mapping_dict)
        base_dir = Path(__file__).resolve().parent
        file_path = base_dir / 'data' / 'tables' / 'testdata.csv'
        assert pytest.project.add_column_mapping(filestructure, column_mapping)
        assert pytest.project.add_file(str(file_path))
        assert pytest.project.get_column_mapping()

    def test_get_project_files_metadata(self):
        """Test that the project file ingestion status can be returned"""
        assert pytest.project.get_project_files_metadata(1, 3)

    def test_get_file_metadata(self):
        """Test that the file metadata can be returned"""
        file_id = pytest.project.get_project_files_metadata(1, 3)['files'][0]['id']
        assert pytest.project.get_file_metadata(file_id)

    def test_get_specific_file_ingestion_status(self):
        """Test that the file ingestion status can be returned"""
        file_id = pytest.project.get_project_files_metadata(1, 3)['files'][0]['id']
        assert pytest.project.get_file_ingestion_status(file_id)

    @pytest.mark.dependency(name='project_contains_data', depends=['add_csv_file'])
    def test_project_contains_data(self):
        """Test that the project contains data"""
        count = 0
        while pytest.project.nodes_datasource.__class__ != Datasource:
            time.sleep(3)
            count += 1
            if count > 100:
                assert False, 'Timeout reached'
        assert True

    @pytest.mark.dependency(depends=['project'], scope='session')
    def test_get_project_lookups(self):
        """Test that the project lookups list can be returned"""
        assert pytest.project.get_project_lookups()

    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_get_column_mapping(self):
        """Test that the correct column mapping can be returned"""
        assert pytest.project.get_column_mapping()

    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_datasources_types(self):
        """Test the types of the datasources"""
        assert pytest.project.nodes_datasource.__class__ == Datasource
        assert pytest.project.edges_datasource.__class__ == Datasource
        assert pytest.project.cases_datasource.__class__ == Datasource

    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_get_project_variants(self):
        """Test that the project variants can be returned"""
        time.sleep(3)
        assert pytest.project.get_project_variants(1, 3)
