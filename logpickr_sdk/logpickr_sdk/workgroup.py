# Apache License 2.0, Copyright 2022 Logpickr
# https://gitlab.com/logpickr/logpickr-sdk/-/blob/master/LICENSE

from logpickr_sdk.graph import Graph, GraphInstance
import requests as req
import pydruid.db
import pandas
from enum import Enum
from typing import List

class Workgroup:
    """A Logpickr workgroup, which is used to log in and access projects"""

    def __init__(self, client_id: str, key: str, apiurl: str, authurl: str, ssl_verify = True):
        """ Creates a Logpickr Workgroup and automatically logs in to the Logpickr API using the provided client id and secret key

        :param client_id: the workgroup ID, which can be found in Process Explorer 360
        :param key: the workgroup's secret key, used for authetication, also found in Process Explorer 360
        :param apiurl: the url of the api found in Process Explorer 360
        :param authurl: the url of the authentication found in Process Explorer 360
        :param ssl_verify: verify SSL certificates"""
        self.id = client_id
        self._apiurl = apiurl
        self._authurl = authurl
        self.key = key
        self._projects = []
        self._datasources = []
        self.token = self.login()
        self.header = "Authorization"
        self.ssl_verify = ssl_verify


    @property
    def apiurl(self):
        """get api url used for the Workgroup"""
        if self._apiurl.find("/pub") != -1:
            return self._apiurl
        else:
            return self._apiurl + "/pub"

    @property
    def projects(self):
        """Performs a REST request for projects, then gets project data for any projects that don't already exist in the Workgroup"""
        try:
            response = req.get(f"{self.apiurl}/projects", headers={"X-Logpickr-API-Token": self.token}, verify=self.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.token = self.login()
                response = req.get(f"{self.apiurl}/projects", headers={"X-Logpickr-API-Token": self.token}, verify=self.ssl_verify)
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

        login_url = f"{self._authurl}/auth/realms/logpickr/protocol/openid-connect/token"  # Note to self: ask if this will always be the same login url structure
        login_data = {
            "grant_type": "urn:ietf:params:oauth:grant-type:uma-ticket",
            "audience": self.id,
            "client_id": self.id,
            "client_secret": self.key
        }

        try:
            response = req.post(login_url, login_data, verify=self.ssl_verify)
            response.raise_for_status()
            return response.json()["access_token"]

        except req.exceptions.HTTPError as error:
            print(f"HTTP Error occured: {error}")
            if error.response.reason == 'Bad Request':
                raise Exception("Invalid login credentials")


class FileStructure:
    """FileStructure used to create a column mapping"""

    def __init__(self, charset: str, delimiter: str, quoteChar: str, escapeChar: str, eolChar: str, commentChar: str, header: bool = True):
        """ Creates a FileStructure used to create a column mapping

        :param charset: the charset of the file (UTF-8, ..)
        :param delimiter: the delimeter of the file (';', ',', ..)
        :param quoteChar: the character to quote field in the file ('\',...)
        :param escapeChar: the character to ('\\', ...)
        :param eolChar: the character for the end of line ('\\n')
        :param commentChar: the character to comment ('#')
        :param header: boolean to say if the file contains a header"""
        self._charset = charset
        self._delimiter = delimiter
        self._quoteChar = quoteChar
        self._escapeChar = escapeChar
        self._eolChar = eolChar
        self._header = header
        self._commentChar = commentChar

    @property
    def charset(self):
        """Returns the charset of the FileStructure"""
        return self._charset

    @property
    def delimiter(self):
        """Returns the delimiter of the FileStructure"""
        return self._delimiter

    @property
    def quoteChar(self):
        """Returns the quoteChar of the FileStructure"""
        return self._quoteChar

    @property
    def escapeChar(self):
        """Returns the escapeChar of the FileStructure"""
        return self._escapeChar

    @property
    def eolChar(self):
        """Returns the eolChar of the FileStructure"""
        return self._eolChar

    @property
    def header(self):
        """Returns the header of the FileStructure"""
        return self._header

    @property
    def commentChar(self):
        """Returns the commentChar of the FileStructure"""
        return self._commentChar

    def tojson(self):
        """Returns Json format of FileStructure"""
        return {
            'charset': self._charset,
            'delimiter': self._delimiter,
            'quoteChar': self._quoteChar,
            'escapeChar': self._escapeChar,
            'eolChar': self._eolChar,
            'header': self._header,
            'commentChar': self._commentChar
        }


class CaseIdOrActivityMapping:
    """CaseId or Activity column mapping"""

    def __init__(self, columnIndex: int):
        """ Creates a CaseIdOrActivityMapping used to create a column mapping

        :param columnIndex: an integer of the column (start at 0)"""
        self._columnIndex = columnIndex

    @property
    def columnIndex(self):
        """Returns the columnIndex of the CaseIdOrActivityMapping"""
        return self._columnIndex

    def tojson(self):
        """Returns json of CaseIdOrActivityMapping"""
        return {
            'columnIndex': self._columnIndex
        }


class TimeMapping:
    """Time mapping used in column mapping"""

    def __init__(self, columnIndex: int, Timeformat: str):
        """ Creates a TimeMapping used to create a column mapping

        :param columnIndex: an integer of the column (start at 0)
        :param format: a string of the format of the time column"""
        self._columnIndex = columnIndex
        self._format = Timeformat

    @property
    def columnIndex(self):
        """Returns the columnIndex of the TimeMapping"""
        return self._columnIndex

    @property
    def format(self):
        """Returns the format of the TimeMapping"""
        return self._format

    def tojson(self):
        """Returns the json format of TimeMapping"""
        return {
            'columnIndex': self._columnIndex,
            'format': self._format
        }


class DimensionAggregation(Enum):
    FIRST = "FIRST"
    LAST = "LAST"
    DISTINCT = "DISTINCT"


class DimensionMapping:
    """Dimension mapping used in column mapping"""

    def __init__(self, name: str, columnIndex: int, isCaseScope: bool, aggregation: DimensionAggregation = None):
        """ Creates a DimensionMapping used to create a column mapping

        :param name: the name of the dimension
        :param columnIndex: an integer of the column (start at 0)
        :param isCaseScope: a boolean to define the scope of the dimension (True if Case Dimension, False for Task Dimension)
        :param aggregation: Enum for the aggregation type (FIRST, LAST, DISTINCT). Can be None."""
        self._name = name
        self._columnIndex = columnIndex
        self._isCaseScope = isCaseScope
        self._aggregation = aggregation

    @property
    def name(self):
        """Returns the name of the DimensionMapping"""
        return self._name

    @property
    def columnIndex(self):
        """Returns the columnIndex of the DimensionMapping"""
        return self._columnIndex

    @property
    def isCaseScope(self):
        """Returns if isCaseScope of the DimensionMapping"""
        return self._isCaseScope

    @property
    def aggregation(self):
        """Returns aggregation of the DimensionMapping"""
        return self._aggregation

    def tojson(self):
        """Returns the json format of the DimensionMapping"""
        return {
            'name': self._name,
            'columnIndex': self._columnIndex,
            'isCaseScope': self._isCaseScope,
            'aggregation': self._aggregation
        } if self._aggregation else {
            'name': self._name,
            'columnIndex': self._columnIndex,
            'isCaseScope': self._isCaseScope        
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
        """ Creates a DimensionMapping used to create a column mapping

        :param name: the name of the metric
        :param columnIndex: an integer of the column (start at 0)
        :param isCaseScope: a boolean to define the scope of the dimension (True if Case Dimension, False for Task Dimension)
        :param unit: a string which describe the unit of the metric. Can be None
        :param aggregation: Enum for the aggregation type (FIRST, LAST, MIN, MAX, SUM, AVG, MEDIAN). Can be None."""
        self._name = name
        self._columnIndex = columnIndex
        self._unit = unit
        self._isCaseScope = isCaseScope
        self._aggregation = aggregation

    @property
    def name(self):
        """Returns the name of the MetricMapping"""
        return self._name

    @property
    def columnIndex(self):
        """Returns the columnIndex of the MetricMapping"""
        return self._columnIndex

    @property
    def unit(self):
        """Returns the unit of the MetricMapping"""
        return self._unit

    @property
    def isCaseScope(self):
        """Returns if isCaseScope of the MetricMapping"""
        return self._isCaseScope

    @property
    def aggregation(self):
        """Returns aggregation of the MetricMapping"""
        return self._aggregation

    def tojson(self):
        """Returns the json format of the MetricMapping"""
        return {
            'name': self._name,
            'columnIndex': self._columnIndex,
            'unit': self._unit if self._unit else '',
            'isCaseScope': self._isCaseScope,
            'aggregation': self._aggregation
        } if self._aggregation else {
            'name': self._name,
            'columnIndex': self._columnIndex,
            'unit': self._unit if self._unit else '',
            'isCaseScope': self._isCaseScope        
        }


List_of_TimeMapping = List[TimeMapping]
List_of_DimensionMapping = List[DimensionMapping]
List_of_MetricMapping = List[MetricMapping]

class ColumnMapping:
    """Description of the columnMapping before sending a file"""

    def __init__(self, caseidmapping: CaseIdOrActivityMapping, activitymapping: CaseIdOrActivityMapping, timemappings: List_of_TimeMapping, dimensionmappings: List_of_DimensionMapping, metricmappings: List_of_MetricMapping ):
        """ Creates a ColumnMapping

        :param caseidmapping: the caseid mapping
        :param activitymapping: the activitymapping
        :param timemappings: List of one or two TimeMapping
        :param dimensionmappings: List of DimensionMapping. Can be None
        :param metricmappings: List of MetricMapping. Can be None."""
        self._caseidmapping = caseidmapping
        self._activitymapping = activitymapping
        self._timemappings = timemappings
        self._dimensionmappings = dimensionmappings
        self._metricmappings = metricmappings

    @property
    def caseidmapping(self):
        """Returns the caseidmapping of the ColumnMapping"""
        return self._caseidmapping

    @property
    def activitymapping(self):
        """Returns the activitymapping of the ColumnMapping"""
        return self._activitymapping

    @property
    def timemappings(self):
        """Returns the timemappings of the ColumnMapping"""
        return self._timemappings

    @property
    def dimensionmappings(self):
        """Returns the dimensionmappings of the ColumnMapping"""
        return self._dimensionmappings

    @property
    def metricmappings(self):
        """Returns the metricmappings of the ColumnMapping"""
        return self._metricmappings

    def tojson(self):
        """Returns the json format of the ColumnMapping"""
        return {
            'caseIdMapping': self._caseidmapping.tojson(),
            'activityMapping': self._activitymapping.tojson(),
            'timeMappings': [tm.tojson() for tm in self._timemappings],
            'dimensionsMappings': [dm.tojson() for dm in self._dimensionmappings] if self._dimensionmappings else [],
            'metricsMappings': [mm.tojson() for mm in self._metricmappings] if self._metricmappings else []
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
            response = req.get(f"{self.owner.apiurl}/project/{self.id}/graph", params=parameters,
                               headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{self.owner.apiurl}/project/{self.id}/graph", params=parameters,
                                   headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)  # trying again
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
            response = req.get(f"{self.owner.apiurl}/project/{self.id}/graphInstance",
                               params=parameters,
                               headers={"X-Logpickr-API-Token": self.owner.token},
                               verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{self.owner.apiurl}/project/{self.id}/graphInstance",
                                   params=parameters,
                                   headers={"X-Logpickr-API-Token": self.owner.token},
                                   verify=self.owner.ssl_verify)  # try again
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
            response = req.get(f"{self.owner.apiurl}/datasources", params={"id": f"{self.id}"},
                               headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{self.owner.apiurl}/datasources", params={"id": f"{self.id}"},
                                   headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)  # try again
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

    def reset(self):
        """Reset all project data except name, description and users rights."""
        try:
            response = req.post(f"{self.owner.apiurl}/project/{self.id}/reset", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.post(f"{self.owner.apiurl}/project/{self.id}/reset", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        
        return response.status_code == 204

    def column_mapping_exists(self):
        """Check if a column mapping to the project"""
        try:
            response = req.get(f"{self.owner.apiurl}/project/{self.id}/column-mapping-exists", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{self.owner.apiurl}/project/{self.id}/column-mapping-exists", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        
        return bool(response.json()["exists"])

    def create_column_mapping(self, filestructure:FileStructure, columnmapping: ColumnMapping):
        """Create a column mapping to the project

        :param filestructure: the filestructure
        :param columnmapping: the columnmapping"""
        try:
            response = req.post(f"{self.owner.apiurl}/project/{self.id}/column-mapping",
                                json={'fileStructure': filestructure.tojson(), 'columnMapping': columnmapping.tojson()},
                                headers={"X-Logpickr-API-Token": self.owner.token,
                                         "content-type": "application/json"},
                                verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.post(f"{self.owner.apiurl}/project/{self.id}/column-mapping",
                                    json={'fileStructure': filestructure.tojson(), 'columnMapping': columnmapping.tojson()},
                                    headers={"X-Logpickr-API-Token": self.owner.token,
                                            "content-type": "application/json"},
                                    verify=self.owner.ssl_verify)  # try again
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        return response.status_code==204

    def reset(self):
        """Makes an API call to manually reset a project"""
        try:
            response = req.post(f"{self.owner.apiurl}/project/{self.id}/reset",headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.post(f"{self.owner.apiurl}/project/{self.id}/reset",headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)  # try again
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        return response.status_code==204

    def add_file(self, path):
        """Adds a file to the project

        :param path: the path to the file"""
        try:
            response = req.post(f"{self.owner.apiurl}/project/{self.id}/file?teamId={self.owner.id}",
                                files={'file': (path.split("/")[-1], open(path, 'rb'), "text/csv")},
                                headers={"X-Logpickr-API-Token": self.owner.token,
                                         "accept": "application/json, text/plain, */*"},
                                verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.post(f"{self.owner.apiurl}/project/{self.id}/file?teamId={self.owner.id}",
                                    files={'file': (path.split("/")[-1], open(path, 'rb'), "text/csv")},
                                    headers={"X-Logpickr-API-Token": self.owner.token,
                                             "accept": "application/json, text/plain, */*"},
                                    verify=self.owner.ssl_verify)  # try again
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        return response.status_code == 201

    @property
    def train_status(self):
        """Returns True if the train is currently running, False otherwise"""
        try:
            response = req.get(f"{self.owner.apiurl}/train/{self.id}", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{self.owner.apiurl}/train/{self.id}", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        
        return response.json()["isTrainRunning"]

    def launch_train(self):
        """Makes an API call to manually launch the train of a project"""
        try:
            response = req.post(f"{self.owner.apiurl}/train/{self.id}/launch", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.post(f"{self.owner.apiurl}/train/{self.id}/launch", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)

    def stop_train(self):
        """Makes an API call to manually stop the train of a project"""
        try:
            response = req.delete(f"{self.owner.apiurl}/train/{self.id}", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.delete(f"{self.owner.apiurl}/train/{self.id}", headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)

    def prediction(self, case_ids):
        """Queries the API to make a prediction for certain cases of the project
        :param case_ids: list of the ids of the cases we want to make predictions on"""

        try:
            response = req.post(f"{self.owner.apiurl}/project/{self.id}/prediction", params={"caseIds": case_ids},
                                headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.post(f"{self.owner.apiurl}/project/{self.id}/prediction", params={"caseIds": case_ids},
                                    headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
            return

        prediction_id = response.json()["resultUrl"].split("/")[-1]

        try:
            response = req.get(f"{self.owner.apiurl}/project/prediction/{prediction_id}",
                               headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.owner.token = self.owner.login()
                response = req.get(f"{self.owner.apiurl}/project/prediction/{prediction_id}",
                                   headers={"X-Logpickr-API-Token": self.owner.token}, verify=self.owner.ssl_verify)
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
        cols = [i[0] for i in self.cursor.description]
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
