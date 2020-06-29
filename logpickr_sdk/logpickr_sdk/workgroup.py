from logpickr_sdk.graph import Graph, GraphInstance
import requests as req
import pydruid.db

API_URL = "http://localhost:8080/pub"
AUTH_URL = "http://localhost:28080"


class Workgroup:
    """A Logpickr workgroup, which is used to log in and access projects"""

    def __init__(self, client_id: str, key: str):
        """ Creates a Logpickr Workgroup and automatically logs in to the Logpickr API using the provided client id and secret key"""
        self.id = client_id
        self.key = key
        self._projects = []
        self._datasources = []
        self.token = self.login()

    @property
    def projects(self):
        """Performs a REST request for projects, then gets project data for any projects that don't already exist in the Workgroup"""
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
            print(f"HTTP Error occured: {error}")
            if error.response.reason == 'Bad Request':
                raise Exception("Invalid login credentials")


class Project:
    """A Logpickr project
    """

    def __init__(self, pid: str, owner: Workgroup):
        """Create a Logpickr project from a project ID and the Workgroup it was created by"""
        self.id = pid
        self.owner = owner
        self._graph = None
        self._graph_instances = []
        self._datasources = []
        self._process_keys = []

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
        """Returns all of the project's Graph Instances, performing and REST request for any instances that don't already exist within the project."""
        if len(self._graph_instances) < len(self.process_keys): # IE if there are new graph instances available
            self._graph_instances = []
            for k in self.process_keys:
                self._graph_instances.append(self.graph_instance_from_key(k))
        return self._graph_instances

    def graph_instance_from_key(self, process_id):
        """Performs a REST request for the graph instance associated with a process key, and returns it"""
        try:
            response = req.get(f"{API_URL}/project/{self.id}/graphInstance",
                               params={"processId": process_id},
                               headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
            graph = response.json()
            graph_instance = GraphInstance.from_json(self.id, graph)
        except req.HTTPError as error:
            print(f"HTTP Error occured: {error}")
            return None
        except Exception as error:
            print(f"Could not parse graph: {error}")
            print(response.json())
            return None
        return graph_instance

    @property
    def datasources(self):
        """Requests and returns the list of datasources associated with the project"""
        try:
            response = req.get(f"{API_URL}/datasources", params={"id": f"{self.id}"},
                               headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
            self._datasources = [Datasource(x["name"], x["type"], x["host"], x["port"], self) for x in response.json()]

        except req.HTTPError as error:
            print(f"HTTP Error occurred: {error}")

        return self._datasources

    @property
    def process_keys(self):
        """Queries the datasources to find the different process keys of the project"""
        if len(self._process_keys) == 0:
            ds = self.datasources[0]
            rows = ds.request(f"SELECT DISTINCT processkey FROM \"{ds.name}\"")
            self._process_keys = [pk[0] for pk in rows]

        return self._process_keys

    def add_file(self, path):
        """Adds a file to the project"""
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
    """An Druid table that can be sent requests by the user"""

    def __init__(self, name: str, dstype: str, host: str, port: str, project: Project):
        self.name = name
        self.type = dstype
        self.host = host
        self.port = port
        self.project = project
        self._connection = None
        self._cursor = None
        self._columns = None

    def request(self, sqlreq):
        """Sends an SQL request to the datasource and returns the results"""
        self.cursor.execute(sqlreq)
        return self.cursor.fetchall()

    @property
    def columns(self):
        """Returns the columns of the datasource"""
        if self._columns is None:
            cols = self.request(
                f"SELECT COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self.name}' ORDER BY 2")
            self._columns = [x[0] for x in cols]
        return self._columns

    @property
    def connection(self):
        """Returns the pydruid connection to the datasource, after initializing it if need be"""
        if self._connection is None:
            self._connection = pydruid.db.connect("localhost", self.port, path="/druid/v2/sql",
                                                  user=self.project.owner.id, password=self.project.owner.key)
        return self._connection

    @property
    def cursor(self):
        """Returns the pydruid cursor on the datasource, after initializing it if it doesn't exist"""
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        return self._cursor
