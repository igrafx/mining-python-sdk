# Apache License 2.0, Copyright 2022 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE

import requests as req
from igrafx_mining_sdk.project import Project
from igrafx_mining_sdk.api_connector import APIConnector


class Workgroup:
    """A Logpickr workgroup, which is used to log in and access projects"""

    def __init__(self, w_id: str, w_key: str, apiurl: str, authurl: str, ssl_verify=True):
        """ Creates a Logpickr Workgroup and automatically logs into the Logpickr API using the provided client id and
        secret key

        :param w_id: the workgroup ID, which can be found in Process Explorer 360
        :param w_key: the workgroup's secret key, used for authetication, also found in Process Explorer 360
        :param apiurl: the URL of the api found in Process Explorer 360
        :param authurl: the URL of the authentication found in Process Explorer 360
        :param ssl_verify: verify SSL certificates
        """
        self.w_id = w_id
        self.w_key = w_key
        self._projects = []
        self._datasources = []
        self.api_connector = APIConnector(w_id, w_key, apiurl, authurl, ssl_verify)

    @property
    def projects(self):
        """Performs a REST request for projects, then gets project data for any projects that don't already exist
        in the Workgroup"""
        # Get list of project ids from api response
        response_project_list = self.api_connector.get_request("projects").json()

        # Remove any projects that no longer exist
        self._projects = [p for p in self._projects if p.id in response_project_list]

        # Add new projects to the list
        for pid in response_project_list:
            if pid not in [p.id for p in self._projects]:
                self._projects.append(Project(pid, self.api_connector))
        return self._projects

    @property
    def datasources(self):
        """Requests and returns the list of datasources associated with the workgroup"""
        try:
            self._datasources = []
            for p in self.projects:
                self._datasources.append(p.nodes_datasource)
                self._datasources.append(p.edges_datasource)
                self._datasources.append(p.cases_datasource)

        except req.HTTPError as error:
            print(f"HTTP Error occurred: {error}")

        return self._datasources

    def project_from_id(self, pid):
        """Returns a project based on its id, or None if no such project exists

        :param pid: the id of the project"""
        p = Project(pid, self.api_connector)
        return p if p.exists else None
