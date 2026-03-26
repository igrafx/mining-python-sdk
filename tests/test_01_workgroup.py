# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE
import os
import pytest
import requests as req
from unittest.mock import MagicMock, patch, PropertyMock
from igrafx_mining_sdk import Project
from igrafx_mining_sdk.workgroup import Workgroup


class TestWorkgroup:
    """Tests for Workgroup class.
    Workgroup and project are pytest fixtures defined in conftest.py file.
    """

    @pytest.mark.dependency(name='workgroup', scope='session')
    def test_create_workgroup(self):
        """Test to create a workgroup."""
        workgroup_id = os.environ.get('WG_ID')
        workgroup_key = os.environ.get('WG_KEY')
        api_url = os.environ.get('WG_URL')
        auth_url = os.environ.get('WG_AUTH')
        jdbc_url = os.environ.get('WG_JDBC')

        # Create the workgroup instance
        wg = Workgroup(workgroup_id, workgroup_key, api_url, auth_url, jdbc_url)

        pytest.workgroup = wg
        assert isinstance(wg, Workgroup)

    def test_wrong_login(self):
        """Test the login with wrong credentials."""
        with pytest.raises(Exception):
            assert Workgroup("a", "b", "c", "d", "e")

    def test_get_app_version(self):
        """Test the get_app_version method."""
        assert pytest.workgroup.get_app_version()

    @pytest.mark.dependency(name='project', depends=['workgroup'], scope='session')
    def test_create_project(self):
        """Test initialization of a project."""
        project_name = "Mining SDK Test Project"
        description = "This is a test project."

        # Clean up any leftover test project from a previous interrupted run
        # (e.g. debug mode stopped, crash before reaching deletion test)
        for pid in pytest.workgroup.get_project_list():
            existing = pytest.workgroup.project_from_id(pid)
            if existing is not None and existing.get_project_name() == project_name:
                existing.delete_project()

        # Create the project
        project = pytest.workgroup.create_project(project_name, description)
        pytest.project = project
        assert isinstance(project, Project)

    @pytest.mark.dependency(depends=['workgroup'])
    def test_projects(self):
        """Test that there are projects in the workgroup."""
        # There should be at least one project in the workgroup
        assert len(pytest.workgroup.get_project_list()) > 0

    @pytest.mark.dependency(depends=['workgroup'])
    def test_project_from_id(self):
        """Test that the project ID can be retrieved."""
        assert pytest.workgroup.project_from_id(pytest.project.id)

    @pytest.mark.dependency(depends=['workgroup'])
    def test_get_workgroup_metadata(self):
        """Test that the workgroup metadata can be retrieved."""
        assert pytest.workgroup.get_workgroup_metadata
        assert pytest.workgroup.get_workgroup_metadata.get("name")
        assert pytest.workgroup.get_workgroup_metadata.get("creationDate")
        assert pytest.workgroup.get_workgroup_metadata.get("startValidityDate")
        assert pytest.workgroup.get_workgroup_metadata.get("isDemoWorkgroup")

    @pytest.mark.dependency(depends=['workgroup'])
    def test_get_workgroup_data_version(self):
        """Test that the workgroup data version can be retrieved."""
        assert pytest.workgroup.get_workgroup_data_version

    # replaces Workgroup.__init__ with a no-op function during the test.
    # This lets you create a Workgroup instance without it actually trying to log in to the API
    # (which the real __init__ does on line 26 via APIConnector).
    @patch.object(Workgroup, '__init__', lambda self, *args, **kwargs: None)
    def test_create_project_error(self):
        """Test that create_project raises ValueError when status code is not 201"""
        wg = Workgroup.__new__(Workgroup)
        wg.w_id = "test_wg"
        wg.api_connector = MagicMock()
        wg.api_connector.post_request.return_value.status_code = 500
        with pytest.raises(ValueError, match="Failed to create project"):
            wg.create_project("test_project")

    @patch.object(Workgroup, '__init__', lambda self, *args, **kwargs: None)
    def test_datasources(self):
        """Test that datasources property returns datasources from all projects"""
        wg = Workgroup.__new__(Workgroup)
        wg._datasources = []
        wg.api_connector = MagicMock()

        mock_project = MagicMock()
        mock_project.nodes_datasource = "nodes"
        mock_project.edges_datasource = "edges"
        mock_project.cases_datasource = "cases"

        wg.get_project_list = MagicMock(return_value=["project_1"])
        wg.project_from_id = MagicMock(return_value=mock_project)

        result = wg.datasources
        assert len(result) == 3
        assert "nodes" in result
        assert "edges" in result
        assert "cases" in result

    @patch.object(Workgroup, '__init__', lambda self, *args, **kwargs: None)
    def test_datasources_http_error(self):
        """Test that datasources property handles HTTPError gracefully"""
        wg = Workgroup.__new__(Workgroup)
        wg._datasources = []
        wg.api_connector = MagicMock()

        wg.get_project_list = MagicMock(side_effect=req.HTTPError("HTTP Error"))

        result = wg.datasources
        assert result == []

    @patch.object(Workgroup, '__init__', lambda self, *args, **kwargs: None)
    def test_datasources_empty(self):
        """Test that datasources property returns empty list when no projects exist"""
        wg = Workgroup.__new__(Workgroup)
        wg._datasources = []
        wg.api_connector = MagicMock()

        wg.get_project_list = MagicMock(return_value=[])

        result = wg.datasources
        assert result == []
