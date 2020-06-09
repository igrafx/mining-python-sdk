from logpickr_sdk.graph import Graph
import requests as req

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
            self._projects = [Project(x, self) for x in response.json()]

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
            self._datasources = [Datasource(x["name"], x["type"], x["host"], x["port"]) for x in response.json()]

        except req.HTTPError as error:
            print(f"HTTP Error occurred: {error}")

        return self._datasources

    def add_file(self, path):
        """Adds a file to the projects
        @:param: path, string path to the file"""
        try:
            file = open(path)
            headerdict = {"X-Logpickr-API-Token": self.owner.token, "accept": "application/json",
                          "Content-Type": "form-data; boundary=--aniania--"}

            response = req.post(f"{API_URL}/project/{self.id}/file?teamId={self.owner.id}",
                                files={'file': (path.split("/")[-1], open(path, 'rb'), "text/csv")},
                                headers={"X-Logpickr-API-Token": self.owner.token,
                                         "accept": "application/json, text/plain, */*"}
                                )
            print(response.request.method)
            print(response.request.url)
            print(response.request.headers)
            print(response.request.body.decode("utf-8"))
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        return True


class Datasource:
    """An SQL table that can be sent requests by the user"""

    # TODO: just about all of this man, let's hope I don't utterly fuck up because I have no idea how any of this works
    def __init__(self, name: str, type: str, host: str, port: str):
        self.name = name
        self.type = type
        self.host = host
        self.port = port

    def request(self, commande):
        """Placeholder method header, ends an SQL request to the table
        @:param: command, the request to send"""
        return None
