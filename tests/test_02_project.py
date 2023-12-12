# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE
import time
import pytest
from pathlib import Path
from igrafx_mining_sdk.project import FileStructure
from igrafx_mining_sdk.column_mapping import Column, ColumnType, ColumnMapping, FileType
from igrafx_mining_sdk.datasource import Datasource
from igrafx_mining_sdk.dtos.PredictionStatusDto import PredictionStatusDto
from igrafx_mining_sdk.dtos.PredictionTaskTypeDto import PredictionTaskTypeDto
from igrafx_mining_sdk.dtos.PredictionLaunchErrorStatusDto import PredictionLaunchErrorStatusDto
from igrafx_mining_sdk.dtos.PredictionPossibilityDto import PredictionPossibilityDto
from igrafx_mining_sdk.dtos.PredictionErrorStatusDto import PredictionErrorStatusDto
from igrafx_mining_sdk.dtos.WorkflowStatusDto import WorkflowStatusDto
from igrafx_mining_sdk.project import Project
from igrafx_mining_sdk.api_connector import APIConnector
import unittest
from unittest.mock import patch
from unittest.mock import MagicMock
import json
import uuid
import requests as req
from typing import List, Optional, Dict
from datetime import datetime

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

    @pytest.mark.dependency(depends=['reset'])
    def test_prediction_possibility_no_data(self):
        assert pytest.project.prediction_possibility() == PredictionPossibilityDto.NO_DATA_IN_PROJECT

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

    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_prediction_possibility_no_end_case_rule(self):
        assert pytest.project.prediction_possibility() == PredictionPossibilityDto.NO_END_CASE_RULE

    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_prediction_status_no_end_case_rule(self):
        assert len(pytest.project.predictions_status()) == 0

    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_prediction_not_exists(self):
        assert pytest.project.is_ready_prediction_exists() == False

    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_prediction_launch_impossible(self):
        assert pytest.project.launch_prediction() == PredictionLaunchErrorStatusDto.NOTHING_TO_PREDICT

    @pytest.mark.dependency(depends=['project_contains_data'])
    def test_predictions_delete(self):
        assert pytest.project.delete_predictions() is None

    def test_prediction_possibility_success(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"isPredictionLaunchPossible": "CAN_LAUNCH_PREDICTION"}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.prediction_possibility()

        assert result == PredictionPossibilityDto.CAN_LAUNCH_PREDICTION

    def test_prediction_possibility_invalid_response(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"isPredictionLaunchPossible": "toto"}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.prediction_possibility()

        assert result == PredictionPossibilityDto.INVALID_RESPONSE

    def test_prediction_possibility_unreadable_response(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"falseArgument": "CAN_LAUNCH_PREDICTION"}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.prediction_possibility()

        assert result == PredictionPossibilityDto.INVALID_RESPONSE

    def test_prediction_non_activated(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 402

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.prediction_possibility()

        assert result == PredictionPossibilityDto.NON_ACTIVATED_PREDICTION

    def test_prediction_forbidden(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 403

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.prediction_possibility()

        assert result == PredictionPossibilityDto.FORBIDDEN

    def test_prediction_unknown_error(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 500

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.prediction_possibility()

        assert result == PredictionPossibilityDto.UNKNOWN_ERROR

    def test_predictions_status_success(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps([
            {
                "workflowId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "status": "RUNNING",
                "projectId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "completedTasks": ["TRAIN_TOPOLOGY"],
                "startTime": "2023-12-12T13:24:11.929Z",
                "endTime": "2023-12-12T13:24:11.929Z"
            }
        ]), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.predictions_status()
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        expected_result = WorkflowStatusDto(
            uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            PredictionStatusDto.RUNNING,
            datetime.strptime("2023-12-12T13:24:11.929Z", date_format),
            datetime.strptime("2023-12-12T13:24:11.929Z", date_format),
            [PredictionTaskTypeDto.TRAIN_TOPOLOGY]
        )

        assert result[0] == expected_result

    def test_predictions_status_success_no_end_date(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps([
            {
                "workflowId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "status": "RUNNING",
                "projectId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "startTime": "2023-12-12T13:24:11.929Z"
            }
        ]), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.predictions_status()
        date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        expected_result = WorkflowStatusDto(
            uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6"),
            PredictionStatusDto.RUNNING,
            datetime.strptime("2023-12-12T13:24:11.929Z", date_format),
            None,
            []
        )

        assert result[0] == expected_result

    def test_predictions_status_invalid_response_if_one_invalid_field(self, mocker):
        """Test successful prediction status."""
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps([
            {
                "workflowId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "status": "RUNNING",
                "projectId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "completedTasks": ["TRAIN_TOPOLOGY"],
                "startTime": "2023-12-12T13:24:11.929Z",
                "endTime": "2023-12-12T13:24:11.929Z"
            },
            {
                "invalidField": "3fa45f64-5717-4562-b3fc-2c963f66afa6",
                "status": "RUNNING",
                "projectId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "completedTasks": ["TRAIN_TOPOLOGY"],
                "startTime": "2023-12-12T13:24:11.929Z",
                "endTime": "2023-12-12T13:24:11.929Z"
            }
        ]), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.predictions_status()

        assert result == PredictionErrorStatusDto.INVALID_RESPONSE

    def test_predictions_status_empty_response(self, mocker):
        """Test successful prediction status."""
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps([]), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.predictions_status()

        assert len(result) == 0

    def test_predictions_status_non_active(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 402

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.predictions_status()

        assert result == PredictionErrorStatusDto.NON_ACTIVATED_PREDICTION

    def test_predictions_status_forbidden(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 403

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.predictions_status()

        assert result == PredictionErrorStatusDto.FORBIDDEN

    def test_predictions_status_failure(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 424

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.predictions_status()

        assert result == PredictionErrorStatusDto.PREDICTION_SERVICE_FAILURE

    def test_predictions_status_unkown_failure(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 500

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.predictions_status()

        assert result == PredictionErrorStatusDto.UNKNOWN_ERROR

    def test_ready_prediction_exists(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"isPredictionReady": True}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.is_ready_prediction_exists()

        assert result == True

    def test_ready_prediction_not_exists(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"isPredictionReady": False}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.is_ready_prediction_exists()

        assert result == False

    def test_ready_prediction_exists_invalid_result(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"isPredictionReady": "toto"}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.is_ready_prediction_exists()

        assert result == PredictionErrorStatusDto.INVALID_RESPONSE

    def test_ready_prediction_exists_invalid_response(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"invalidField": "toto"}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.is_ready_prediction_exists()

        assert result == PredictionErrorStatusDto.INVALID_RESPONSE

    def test_ready_prediction_exists_non_active_prediction(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 402

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.is_ready_prediction_exists()

        assert result == PredictionErrorStatusDto.NON_ACTIVATED_PREDICTION

    def test_ready_prediction_exists_forbidden(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 403

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.is_ready_prediction_exists()

        assert result == PredictionErrorStatusDto.FORBIDDEN


    def test_ready_prediction_exists_forbidden(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 500

        mocker.patch.object(api_connector, 'get_request', return_value= expected_response)

        result = project.is_ready_prediction_exists()

        assert result == PredictionErrorStatusDto.UNKNOWN_ERROR

    def test_launch_prediction_success(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"predictionTrainId": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'post_request', return_value= expected_response)

        result = project.launch_prediction()

        assert result == uuid.UUID("3fa85f64-5717-4562-b3fc-2c963f66afa6")

    def test_launch_prediction_bad_response_uuid(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"predictionTrainId": "toto"}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'post_request', return_value= expected_response)

        result = project.launch_prediction()

        assert result == PredictionLaunchErrorStatusDto.INVALID_RESPONSE

    def test_launch_prediction_bad_response_field(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 200
        expected_response.headers = None
        expected_response._content = bytes(json.dumps({"invalidField": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}), 'utf-8')
        expected_response.json = lambda: json.loads(expected_response.content)

        mocker.patch.object(api_connector, 'post_request', return_value= expected_response)

        result = project.launch_prediction()

        assert result == PredictionLaunchErrorStatusDto.INVALID_RESPONSE

    def test_launch_prediction_non_active(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 402

        mocker.patch.object(api_connector, 'post_request', return_value= expected_response)

        result = project.launch_prediction()

        assert result == PredictionLaunchErrorStatusDto.NON_ACTIVATED_PREDICTION

    def test_launch_prediction_forbidden(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 403

        mocker.patch.object(api_connector, 'post_request', return_value= expected_response)

        result = project.launch_prediction()

        assert result == PredictionLaunchErrorStatusDto.FORBIDDEN

    def test_launch_prediction_impossible(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 409

        mocker.patch.object(api_connector, 'post_request', return_value= expected_response)

        result = project.launch_prediction()

        assert result == PredictionLaunchErrorStatusDto.NOTHING_TO_PREDICT

    def test_launch_prediction_failure(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 424

        mocker.patch.object(api_connector, 'post_request', return_value= expected_response)

        result = project.launch_prediction()

        assert result == PredictionLaunchErrorStatusDto.PREDICTION_SERVICE_FAILURE

    def test_launch_prediction_unknown_failure(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 500

        mocker.patch.object(api_connector, 'post_request', return_value= expected_response)

        result = project.launch_prediction()

        assert result == PredictionLaunchErrorStatusDto.UNKNOWN_ERROR

    def test_delete_predictions_success(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 204

        mocker.patch.object(api_connector, 'delete_request', return_value= expected_response)

        result = project.delete_predictions()

        assert result is None

    def test_delete_predictions_non_active(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 402

        mocker.patch.object(api_connector, 'delete_request', return_value= expected_response)

        result = project.delete_predictions()

        assert result == PredictionErrorStatusDto.NON_ACTIVATED_PREDICTION

    def test_delete_predictions_forbidden(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 403

        mocker.patch.object(api_connector, 'delete_request', return_value= expected_response)

        result = project.delete_predictions()

        assert result == PredictionErrorStatusDto.FORBIDDEN

    def test_delete_predictions_fails(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 424

        mocker.patch.object(api_connector, 'delete_request', return_value= expected_response)

        result = project.delete_predictions()

        assert result == PredictionErrorStatusDto.PREDICTION_SERVICE_FAILURE

    def test_delete_predictions_fails(self, mocker):
        api_connector = APIConnector(wg_id='bd4f84d9-34ec-4943-b37a-c025ebaa840c', wg_key='83de1a05-06ad-4757-9855-926ef696463f', apiurl='https://truc.com', authurl='https://truc.com/realms/realm/', ssl_verify=False)

        project = Project(pid = str(uuid.uuid4()), api_connector = api_connector)
        # Set up the expected response
        expected_response = req.Response()
        expected_response.status_code = 500

        mocker.patch.object(api_connector, 'delete_request', return_value= expected_response)

        result = project.delete_predictions()

        assert result == PredictionErrorStatusDto.UNKNOWN_ERROR
