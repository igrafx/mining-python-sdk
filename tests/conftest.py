# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE

import pytest
from mining-python-sdk.igrafx_mining_sdk.workgroup import Workgroup
# from igrafx_mining_sdk.workgroup import Workgroup
import os


@pytest.fixture(scope="session")
def workgroup():
    """Fixture to create the workgroup instance."""
    # Replace the placeholders with your actual values
    workgroup_id = os.environ.get('WG_ID')
    workgroup_key = os.environ.get('WG_KEY')
    api_url = os.environ.get('WG_URL')
    auth_url = os.environ.get('WG_AUTH')

    # Create the workgroup instance
    wg = Workgroup(workgroup_id, workgroup_key, api_url, auth_url)
    yield wg

    # Perform any necessary cleanup after the test session (if needed)


@pytest.fixture(scope="session")
def project(request, workgroup):
    """Fixture to create and delete the project for all tests in a session."""
    # Replace the placeholders with your desired project name and description
    project_name = "Test Project"
    description = "This is a test project."

    # Create the project
    created_project = workgroup.create_project(project_name, description)
    yield created_project

    # Delete the project after all tests in the session
    def cleanup_project():
        created_project.delete_project()

    # Register the cleanup function to be called after all tests in the session
    request.addfinalizer(cleanup_project)
