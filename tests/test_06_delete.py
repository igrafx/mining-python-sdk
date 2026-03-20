# MIT License, Copyright 2023 iGrafx
# https://github.com/igrafx/mining-python-sdk/blob/dev/LICENSE
import pytest


class TestDelete:
    """Final tests to verify project deletion.

    Note: Even if this test is skipped or never reached (crash, debug stop, etc.),
    the project is still cleaned up by pytest_sessionfinish in conftest.py.
    """

    @pytest.mark.dependency(depends=['project'], scope='session')
    def test_delete_project(self):
        """Test the deletion of a project."""
        pytest.project.delete_project()
        pytest.project = None  # Prevent double deletion in pytest_sessionfinish
