# Apache License 2.0, Copyright 2020 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE

import pytest
from igrafx_mining_sdk.workgroup import Workgroup


class TestWorkgroup:
    """Tests for Workgroup class.
    ID, SECRET, API, AUTH and PROJECT_ID are pytest fixtures defined in conftest.py file.
    """

    def test_create_workgroup(self, ID, SECRET, API, AUTH):
        """Test to create a workgroup."""
        w = Workgroup(ID, SECRET, API, AUTH)
        print(f"\nID is {ID}, \nSECRET is {SECRET}, \nAPI is {API}, \nAUTH is {AUTH}")
        assert isinstance(w, Workgroup)

    def test_wrong_login(self):
        """Test the login with wrong credentials."""
        with pytest.raises(Exception):
            assert Workgroup("a", "b")

    def test_projects(self, ID, SECRET, API, AUTH):
        """Test that there are projects in the workgroup."""
        w = Workgroup(ID, SECRET, API, AUTH)
        print(f"\nID is {ID}, \nSECRET is {SECRET}, \nAPI is {API}, \nAUTH is {AUTH}")
        assert len(w.projects) > 0  # Since there should be projects in the workgroup

    def test_tables(self, ID, SECRET, API, AUTH):
        """Test that there are tables in the workgroup."""
        w = Workgroup(ID, SECRET, API, AUTH)
        assert len(w.datasources) > 0  # Since there should be tables in the workgroup
