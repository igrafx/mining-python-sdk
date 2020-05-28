from logpickr_sdk.graph import Graph

class Workgroup:
    """A Logpickr workgroup, which is used to log in and access projects"""
    def __init__(self, id, key):
        self.id = id
        self.key = key
        self._projects

    @property
    def projects(self):
        """Performs a REST request for projects, then gets project data for any projects that don't already exist
        in _projects"""

class Project:
    """A Logpickr project
    """

    def __init__(self, id):
        self.id = id
