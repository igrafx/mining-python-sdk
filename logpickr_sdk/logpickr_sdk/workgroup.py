from logpickr_sdk.graph import Graph
import requests as req
import pydruid.db

API_URL = "http://localhost:8080/pub"
AUTH_URL = "http://localhost:28080"


class Workgroup:
    """A Logpickr workgroup, which is used to log in and access projects"""

    def __init__(self, client_id: str, key: str):
        self.id = client_id
        self.key = key
        self._projects = []
        self._datasources = []
        self.token = self.login()

    @property
    def projects(self):
        """Performs a REST request for projects, then gets project data for any projects that don't already exist
        in _projects"""
        try:
            response = req.get(f"{API_URL}/projects", headers={"X-Logpickr-API-Token": self.token})
            response.raise_for_status()
            for pid in response.json():
                if len([pro for pro in self._projects if pro.id == pid]) == 0:  # If there are no projects with that ID
                    self._projects.append(Project(pid, self))

        except req.HTTPError as error:
            print(f"HTTP Error occurred: {error}")

        return self._projects

    @property
    def datasources(self):
        """Requests and returns the list of datasources associated with the workgroup"""
        try:
            tmp = []
            for p in self.projects:
                tmp += p.datasources
            self._datasources = tmp

        except req.HTTPError as error:
            print(f"HTTP Error occurred: {error}")

        return self._datasources

    def login(self):
        """Logs in to the Logpickr API with the Workgroup's credentials and retrieves a token for later requests"""

        login_url = f"{AUTH_URL}/auth/realms/logpickr/protocol/openid-connect/token"  # Note to self: ask if this will always be the same login url structure
        login_data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
            "audience": self.id,
            "client_id": self.id,
            "client_secret": self.key
        }

        try:
            response = req.post(login_url, login_data)
            response.raise_for_status()
            return response.json()["access_token"]

        except req.exceptions.HTTPError as error:
            # TODO: handle different errors differently (good words buddy)
            print(f"HTTP Error occured: {error}")

        return ""


class Project:
    """A Logpickr project
    """

    def __init__(self, id: str, owner: Workgroup):
        self.id = id
        self.owner = owner
        self._graph = None
        self._graph_instances = []
        self._datasources = []

    @property
    def graph(self):
        """Performs a REST for the project model graph if it hasn't already been retrieved"""
        try:
            response = req.get(f"{API_URL}/project/{self.id}/graph", headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
            self._graph = Graph.from_json(self.id, response.text)
        except req.HTTPError as error:
            print(f"HTTP Error occurred: {error}")
        return self._graph

    @property
    def graph_instances(self):
        """Performs a REST for the graph instances contained in the project"""
        return None

    @property
    def datasources(self):
        """Requests and returns the list of tables associated with the project"""
        try:
            response = req.get(f"{API_URL}/datasources", params={"id": f"{self.id}"},
                               headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
            self._datasources = [Datasource(x["name"], x["type"], x["host"], x["port"], self) for x in response.json()]

        except req.HTTPError as error:
            print(f"HTTP Error occurred: {error}")

        return self._datasources

    def add_file(self, path):
        """Adds a file to the projects
        @:param: path, string path to the file"""
        try:
            response = req.post(f"{API_URL}/project/{self.id}/file?teamId={self.owner.id}",
                                files={'file': (path.split("/")[-1], open(path, 'rb'), "text/csv")},
                                headers={"X-Logpickr-API-Token": self.owner.token,
                                         "accept": "application/json, text/plain, */*"}
                                )
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        return True


class Datasource:
    """An SQL table that can be sent requests by the user"""

    def __init__(self, name: str, dstype: str, host: str, port: str, project: Project):
        self.name = name
        self.type = dstype
        self.host = host
        self.port = port
        self.project = project
        self._connection = None
        self._cursor = None
        self._columns = None

    def request(self, command):
        """Placeholder method header, sends an SQL request to the table
        @:param: command, the request to send"""
        self.cursor.execute(command)
        return self.cursor.fetchall()

    @property
    def columns(self):
        if self._columns is None:
            cols = self.request(
                f"SELECT COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self.name}' ORDER BY 2")
            self._columns = [x[0] for x in cols]
        return self._columns

    @property
    def connection(self):
        if self._connection is None:
            self._connection = pydruid.db.connect("localhost", self.port, path="/druid/v2/sql",
                                                  user=self.project.owner.id, password=self.project.owner.key)
        return self._connection

    @property
    def cursor(self):
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        return self._cursor
