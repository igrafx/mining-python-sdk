from logpickr_sdk.graph import Graph


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
        """Logs in to the Logpickr API and retrieves a token to use for later requests"""
        raise Exception("Invalid credentials")
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