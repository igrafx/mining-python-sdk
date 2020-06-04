from logpickr_sdk.graph import Graph
import requests as req

API_URL = "http://localhost:8080/pub"
AUTH_URL = "http://localhost:28080"


class Workgroup:
    """A Logpickr workgroup, which is used to log in and access projects"""

    def __init__(self, id, key):
        self.id = id
        self.key = key
        self._projects = []
        self.token = self.login()

    @property
    def projects(self):
        """Performs a REST request for projects, then gets project data for any projects that don't already exist
        in _projects"""
        return []

    @property
    def tables(self):
        """Requests and returns the list of tables associated with the workgroup"""
        return []

    def login(self):
        """Logs in to the Logpickr API with the Workgroup's credentials and retrieves a token for later requests"""
        login_url = f"{AUTH_URL}/auth/realms/master/protocol/openid-connect/token"
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

        except req.exceptions.HTTPError as err:
            print(f"HTTP Error occured: {err}")

        return ""


class Project:
    """A Logpickr project
    """

    def __init__(self, id):
        self.id = id
        self._graph = None
        self._graph_instances = []
        self._tables = []

    @property
    def graph(self):
        """Performs a REST for the project model graph if it hasn't already been retrieved"""
        return None

    @property
    def graph_instances(self):
        """Performs a REST for the graph instances contained in the project"""
        return None

    @property
    def datasources(self):
        """Requests and returns the list of tables associated with the project"""
        return []

    def add_file(self, path):
        """Adds a file to the projects
        @:param: path, string path to the file"""
        return True


class Datasource:
    """An SQL table that can be sent requests by the user"""

    def __init__(self, name, type, host, port):
        self.name = name
        self.type = type
        self.host = host
        self.port = port

    def request(self,commande):
        """Placeholder method header, ends an SQL request to the table
        @:param: command, the request to send"""
        return None