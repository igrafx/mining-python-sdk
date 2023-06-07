import requests as req


class APIConnector:
    """Class to connect to the API. It allows us to log into the Logpickr API and retrive a token.
    It also allows us to do HTTP GET, POST and DELETE requests."""
    def __init__(self, wg_id: str, wg_key: str, apiurl: str, authurl: str, ssl_verify: bool):
        """Initializes the APIConnector class.

        :param wg_id: The ID of the workgroup
        :param wg_key: The secret key of the workgroup
        :param apiurl: The URL of the API
        :param authurl: The URL of the authentication
        :param ssl_verify: Verify SSL certificates
        """

        self.wg_id = wg_id
        self.wg_key = wg_key
        self.apiurl = self.__process_apiurl(apiurl)
        self._authurl = authurl
        self.ssl_verify = ssl_verify
        self.token_header = self.__login()

    def __process_apiurl(self, apiurl):
        """Ensure that the API URL ends with  /pub

        :param apiurl: The URL of the API
        """
        return apiurl if apiurl.endswith("/pub") else apiurl + "/pub"

    def __login(self):
        """Logs into the Logpickr API with the Workgroup's credentials and retrieves a token for later requests"""

        # authurl now contains the realm /realm/logpickr
        login_url = f"{self._authurl}/protocol/openid-connect/token"
        login_data = {
            "grant_type": "client_credentials",
            "client_id": self.wg_id,
            "client_secret": self.wg_key
        }

        try:
            response = req.post(login_url, login_data, verify=self.ssl_verify)
            response.raise_for_status()
            return {"Authorization": "Bearer " + response.json()["access_token"]}

        except req.exceptions.HTTPError as error:
            print(f"HTTP Error occured: {error}")
            if error.response.reason == 'Bad Request':
                raise Exception("Invalid login credentials")

    def get_request(self, route, *, params=None):
        """Does an HTTP GET request to the Logpickr API by simply taking the route and eventual parameters

        :param route: The route of the request
        :param params: The parameters of the request
        """

        response = None
        route = self.apiurl + route if route.startswith('/') else self.apiurl + '/' + route
        try:
            response = req.get(route,
                               params=params,
                               headers=self.token_header,
                               verify=self.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.token_header = self.__login()
                self.get_request(route, params=params)
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        return response

    def post_request(self, route, *, json=None, files=None, headers={}):
        """Does an HTTP POST request to the Logpickr API by simply taking the route, an eventual JSON, files and headers

        :param route: The route of the request
        :param json: A given JSON object
        :param files: Eventual files
        :param headers: Additional headers
        """

        response = None
        route = self.apiurl + route if route.startswith('/') else self.apiurl + '/' + route
        try:
            response = req.post(route,
                                json=json,
                                files=files,
                                headers={**self.token_header, **headers},
                                verify=self.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.token_header = self.__login()
                self.post_request(route, json=json, files=files, headers=headers)
            response.raise_for_status()
        except req.HTTPError as error:
            if response is not None:
                print(f"Http error occured: {error}")
                print(response.text)
        return response

    def delete_request(self, route):
        """Does an HTTP DELETE request to the Logpickr API by simply taking the route

        :param route: The route of the request
        """

        response = None
        route = self.apiurl + route if route.startswith('/') else self.apiurl + '/' + route
        try:
            response = req.delete(route,
                                  headers=self.token_header,
                                  verify=self.ssl_verify)
            if response.status_code == 401:  # Only possible if the token has expired
                self.token_header = self.__login()
                self.delete_request(route)
            response.raise_for_status()
        except req.HTTPError as error:
            print(f"Http error occured: {error}")
            print(response.text)
        return response.json()
