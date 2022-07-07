# Apache License 2.0, Copyright 2022 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE

from logpickr_sdk.graph import Graph, GraphInstance
import requests as req
import pydruid.db
import pandas
from enum import Enum

API_URL = "http://localhost:8080/pub"
AUTH_URL = "http://localhost:28080"


def set_api_url(url):
    """Sets the API url

    :param url: the url to query for API calls"""
    global API_URL
    if url.find("/pub") != -1:
        API_URL = url
    else:
        API_URL = url + "/pub"


def set_auth_url(url):
    """Sets the authentication url

    :param url: the url to query for authentication calls"""
    global AUTH_URL
    AUTH_URL = url


class Workgroup:
    """A Logpickr workgroup, which is used to log in and access projects"""

    def __init__(self, client_id: str, key: str):
        """ Creates a Logpickr Workgroup and automatically logs in to the Logpickr API using the provided client id and secret key

        :param client_id: the workgroup ID, which can be found in Process Explorer 360
        :param key: the workgroup's secret key, used for authetication, also found in Process Explorer 360"""
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
            if response.status_code == 401:  # Only possible if the token has expired
                self.token = self.login()
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

    def project_from_id(self, pid):
        """Returns a project based on its id, or None if no such project exists"""

        return next((p for p in self.projects if p.id == pid), None)

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

class FileStructure:
    """FileStrucutre used to create a column mapping"""

    def __init__(self, charset: str, delimiter: str, quoteChar: str, escapeChar: str, colChar: str, commentChar: str, columnSeparator: str, header: bool = True):
        self.charset = charset
        self.delimiter = delimiter
        self.quoteChar = quoteChar
        self.escapeChar = escapeChar
        self.colChar = colChar
        self.header = header
        self.commentChar = commentChar
        self.columnSeparator = columnSeparator

    @property
    def charset(self):
        """Returns the charset of the FileStructure"""
        return self.charset

    @property
    def delimiter(self):
        """Returns the delimiter of the FileStructure"""
        return self.delimiter

    @property
    def quoteChar(self):
        """Returns the quoteChar of the FileStructure"""
        return self.quoteChar

    @property
    def escapeChar(self):
        """Returns the escapeChar of the FileStructure"""
        return self.escapeChar

    @property
    def colChar(self):
        """Returns the colChar of the FileStructure"""
        return self.colChar

    @property
    def header(self):
        """Returns the header of the FileStructure"""
        return self.header

    @property
    def commentChar(self):
        """Returns the commentChar of the FileStructure"""
        return self.commentChar

    @property
    def columnSeparator(self):
        """Returns the columnSeparator of the FileStructure"""
        return self.columnSeparator

    def tojson(self):
        return {
            'charset': self.charset,
            'delimiter': self.delimiter,
            'quoteChar': self.quoteChar,
            'escapeChar': self.escapeChar,
            'colChar': self.colChar,
            'header': self.header,
            'commentChar': self.commentChar,
            'columnSeparator': self.columnSeparator
        }

class CaseIdOrActivityMapping:
    """CaseId or Activity column mapping"""

    def __init__(self, columnIndex: int):
        self.columnIndex = columnIndex

    @property
    def columnIndex(self):
        """Returns the columnIndex of the CaseIdOrActivityMapping"""
        return self.columnIndex

    def tojson(self):
        {
            'columnIndex': self.columnIndex
        }

class TimeMapping:
    """Time mapping used in column mapping"""

    def __init__(self, columnIndex: int, Timeformat: str):
        self.columnIndex = columnIndex
        self.format = Timeformat

    @property
    def columnIndex(self):
        """Returns the columnIndex of the TimeMapping"""
        return self.columnIndex

    @property
    def format(self):
        """Returns the format of the TimeMapping"""
        return self.format

    def tojson(self):
        {
            'columnIndex': self.columnIndex,
            'format': self.format
        }

class DimensionAggregation(Enum):
    FIRST = "FIRST"
    LAST = "LAST"
    DISTINCT = "DISTINCT"

class DimensionMapping:
    """Dimension mapping used in column mapping"""
    def __init__(self, name: str, columnIndex: int, isCaseScope: bool, aggregation: DimensionAggregation = None):
        self.name = name
        self.columnIndex = columnIndex
        self.isCaseScope = isCaseScope
        self.aggregation = aggregation

    @property
    def name(self):
        """Returns the name of the DimensionMapping"""
        return self.name

    @property
    def columnIndex(self):
        """Returns the columnIndex of the DimensionMapping"""
        return self.columnIndex

    @property
    def isCaseScope(self):
        """Returns if isCaseScope of the DimensionMapping"""
        return self.isCaseScope

    @property
    def aggregation(self):
        """Returns aggregation of the DimensionMapping"""
        return self.aggregation

    def tojson(self):
        return {
            'name': self.name,
            'columnIndex': self.columnIndex,
            'isCaseScope': self.isCaseScope,
            'aggregation': self.aggregation
        }

class MetricAggregation(Enum):
    FIRST = "FIRST"
    LAST = "LAST"
    MIN = "MIN"
    MAX = "MAX"
    SUM = "SUM"
    AVG = "AVG"
    MEDIAN = "MEDIAN"

class MetricMapping:
    """Metric mapping used in column mapping"""
    def __init__(self, name: str, columnIndex: int, isCaseScope: bool, unit: str = None, aggregation: MetricAggregation = None):
        self.name = name
        self.columnIndex = columnIndex
        self.unit = unit
        self.isCaseScope = isCaseScope
        self.aggregation = aggregation

    @property
    def name(self):
        """Returns the name of the MetricMapping"""
        return self.name

    @property
    def columnIndex(self):
        """Returns the columnIndex of the MetricMapping"""
        return self.columnIndex

    @property
    def unit(self):
        """Returns the unit of the MetricMapping"""
        return self.unit

    @property
    def isCaseScope(self):
        """Returns if isCaseScope of the MetricMapping"""
        return self.isCaseScope

    @property
    def aggregation(self):
        """Returns aggregation of the MetricMapping"""
        return self.aggregation

    def tojson(self):
        return {
            'name': self.name,
            'columnIndex': self.columnIndex,
            'unit': self.unit,
            'isCaseScope': self.isCaseScope,
            'aggregation': self.aggregation
        }

class ColumnMapping:
    """Description of the columnMapping before sending a file"""

    def __init__(self, caseidmapping: CaseIdOrActivityMapping, activitymapping: CaseIdOrActivityMapping, timemappings: list[TimeMapping], dimensionmappings: list[DimensionMapping], metricmappings: list[MetricMapping] ):
        self.caseidmapping = caseidmapping
        self.activitymapping = activitymapping
        self.timemappings = timemappings
        self.dimensionmappings = dimensionmappings
        self.metricmappings = metricmappings

    @property
    def caseidmapping(self):
        """Returns the caseidmapping of the ColumnMapping"""
        return self.caseidmapping

    @property
    def activitymapping(self):
        """Returns the activitymapping of the ColumnMapping"""
        return self.activitymapping

    @property
    def timemappings(self):
        """Returns the timemappings of the ColumnMapping"""
        return self.timemappings

    @property
    def dimensionmappings(self):
        """Returns the dimensionmappings of the ColumnMapping"""
        return self.dimensionmappings

    @property
    def metricmappings(self):
        """Returns the metricmappings of the ColumnMapping"""
        return self.metricmappings

    def tojson(self):
        return {
            'caseIdMapping': self.caseidmapping.tojson,
            'activityMapping': self.activitymapping.tojson,
            'timeMappings': [tm.tojson for tm in self.timemappings],
            'dimensionsMappings': [dm.tojson for tm in self.dimensionmappings],
            'metricsMappings': [mm.tojson for tm in self.metricmappings]
        }

class Project:
    """A Logpickr project
    """

    def __init__(self, pid: str, owner: Workgroup):
        """Create a Logpickr project from a project ID and the Workgroup it was created by

        :param pid: the Project's ID
        :param owner: the Workgroup that the Project belongs to"""
        self.id = pid
        self.owner = owner
        self._graph = None
        self._graph_instances = []
        self._datasources = []
        self._process_keys = []

    def graph(self, gateways=False):
        """Performs a REST for the project model graph if it hasn't already been retrieved
        :param gateways: Boolean that controls whether the graph returned will be BPMN-like or not"""
        parameters = {"mode": "gateways"} if gateways else {}
        try:
            response = req.get(f"{API_URL}/project/{self.id}/graph", params=parameters,
                               headers={"X-Logpickr-API-Token": self.owner.token})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{API_URL}/project/{self.id}/graph", params=parameters,
                                   headers={"X-Logpickr-API-Token": self.owner.token})  # trying again
            response.raise_for_status()
            self._graph = Graph.from_json(self.id, response.text)
        except req.HTTPError as error:
            print(f"HTTP Error occurred: {error}")
        return self._graph

    @property
    def graph_instances(self):
        """Returns all of the project's Graph Instances, performing and REST request for any instances that don't already exist within the project."""
        if len(self._graph_instances) < len(self.process_keys):  # IE if there are new graph instances available
            self._graph_instances = []
            for k in self.process_keys:
                self._graph_instances.append(self.graph_instance_from_key(k))
        return self._graph_instances

    def graph_instance_from_key(self, process_id, detailed=False):
        """Performs a REST request for the graph instance associated with a process key, and returns it

        :param process_id: the id of the process whose graph we want to get"""
        parameters = {"processId": process_id, "mode": "gateways"} if detailed else {"processId": process_id, "mode": "simplified"}
        try:
            response = req.get(f"{API_URL}/project/{self.id}/graphInstance",
                               params=parameters,
                               headers={"X-Logpickr-API-Token": self.owner.token})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{API_URL}/project/{self.id}/graphInstance",
                                   params=parameters,
                                   headers={"X-Logpickr-API-Token": self.owner.token})  # try again
            response.raise_for_status()
            graph = response.json()["value"]
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
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{API_URL}/datasources", params={"id": f"{self.id}"},
                                   headers={"X-Logpickr-API-Token": self.owner.token})  # try again
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
            res = ds.request(f"SELECT DISTINCT processkey FROM \"{ds.name}\"")
            self._process_keys = [key for key in res['processkey']]

        return self._process_keys

    def column_mapping_exists(self):
        """Check if a column mapping to the project"""
        try:
            response = req.get(f"{API_URL}/project/{self.id}/column-mapping-exists", headers={"X-Logpickr-API-Token": self.owner.token})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{API_URL}/project/{self.id}/column-mapping-exists", headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        
        return bool(response.json()["exists"])

    def create_column_mapping(self, filestructure:FileStructure, columnmapping: ColumnMapping):
        """Create a column mapping to the project

        :param 
            filestructure: the filestructure
            columnmapping: the columnmapping"""
        try:
            response = req.post(f"{API_URL}/project/{self.id}/column-mapping",
                                json={'fileStructure': filestructure.tojson, 'columnMapping': columnmapping.tojson},
                                headers={"X-Logpickr-API-Token": self.owner.token,
                                         "accept": "application/json, text/plain, */*"})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.post(f"{API_URL}/project/{self.id}/column-mapping",
                                    json={'fileStructure': filestructure.tojson, 'columnMapping': columnmapping.tojson},
                                    headers={"X-Logpickr-API-Token": self.owner.token,
                                            "accept": "application/json, text/plain, */*"})  # try again
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        return True

    def add_file(self, path):
        """Adds a file to the project

        :param path: the path to the file"""
        try:
            response = req.post(f"{API_URL}/project/{self.id}/file?teamId={self.owner.id}",
                                files={'file': (path.split("/")[-1], open(path, 'rb'), "text/csv")},
                                headers={"X-Logpickr-API-Token": self.owner.token,
                                         "accept": "application/json, text/plain, */*"})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.post(f"{API_URL}/project/{self.id}/file?teamId={self.owner.id}",
                                    files={'file': (path.split("/")[-1], open(path, 'rb'), "text/csv")},
                                    headers={"X-Logpickr-API-Token": self.owner.token,
                                             "accept": "application/json, text/plain, */*"})  # try again
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        return True

    @property
    def train_status(self):
        """Returns True if the train is currently running, False otherwise"""
        try:
            response = req.get(f"{API_URL}/train/{self.id}", headers={"X-Logpickr-API-Token": self.owner.token})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{API_URL}/train/{self.id}", headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        
        return response.json()["isTrainRunning"]

    def launch_train(self):
        """Makes an API call to manually launch the train of a project"""
        try:
            response = req.post(f"{API_URL}/train/{self.id}/launch", headers={"X-Logpickr-API-Token": self.owner.token})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{API_URL}/train/{self.id}/launch", headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)

    def stop_train(self):
        """Makes an API call to manually stop the train of a project"""
        try:
            response = req.delete(f"{API_URL}/train/{self.id}", headers={"X-Logpickr-API-Token": self.owner.token})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.delete(f"{API_URL}/train/{self.id}", headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)

    def prediction(self, case_ids):
        """Queries the API to make a prediction for certain cases of the project
        :param case_ids: list of the ids of the cases we want to make predictions on"""

        try:
            response = req.post(f"{API_URL}/project/{self.id}/prediction", params={"caseIds": case_ids},
                                headers={"X-Logpickr-API-Token": self.owner.token})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.post(f"{API_URL}/project/{self.id}/prediction", params={"caseIds": case_ids},
                                    headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
            return

        prediction_id = response.json()["resultUrl"].split("/")[-1]

        try:
            response = req.get(f"{API_URL}/project/prediction/{prediction_id}",
                               headers={"X-Logpickr-API-Token": self.owner.token})
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{API_URL}/project/prediction/{prediction_id}",
                                   headers={"X-Logpickr-API-Token": self.owner.token})
            response.raise_for_status()
            return response.json()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)


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
        """Sends an SQL request to the datasource and returns the results as a pandas Dataframe

        :param sqlreq: the SQL request to execute"""
        self.cursor.execute(sqlreq)
        rows = self.cursor.fetchall()
        cols = list(rows[0]._fields)
        data = [list(r) for r in rows]
        return pandas.DataFrame(data, columns=cols)

    @property
    def columns(self):
        """Returns the columns of the datasource"""
        if self._columns is None:
            res = self.request(
                f"SELECT COLUMN_NAME, ORDINAL_POSITION, DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{self.name}' ORDER BY 2")
            self._columns = [x for x in res["COLUMN_NAME"]]
        return self._columns

    @property
    def connection(self):
        """Returns the pydruid connection to the datasource, after initializing it if need be"""
        if self._connection is None:
            self._connection = pydruid.db.connect(self.host, self.port, path="/druid/v2/sql",
                                                  user=self.project.owner.id, password=self.project.owner.key)
        return self._connection

    @property
    def cursor(self):
        """Returns the pydruid cursor on the datasource, after initializing it if it doesn't exist"""
        if self._cursor is None:
            self._cursor = self.connection.cursor()
        return self._cursor
