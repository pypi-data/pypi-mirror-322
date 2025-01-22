import requests
import json

class OpenHABConnector:
    def __init__(self, url: str, username: str = None, password: str = None):
        """
        Initializes the OpenHABConnector instance.

        :param url: The base URL of the OpenHAB server (e.g., "http://127.0.0.1:8080").
        :param username: Optional; The username for authentication (default is None).
        :param password: Optional; The password for authentication (default is None).
        """
        self.url = url
        self.username = username
        self.password = password
        self.isCloud = False
        self.isLoggedIn = False

        self.session = requests.Session()

        if self.username is not None and self.password is not None:
            self.auth = (self.username, self.password)
            self.session.auth = self.auth
        else:
            self.auth = None
            self.session.auth = None

        self.__login()

    def __login(self):
        """
        Attempts to log in to the OpenHAB server.

        If the server is "myopenhab.org", it sets the connection to the cloud service.
        Otherwise, it prepares a local connection and verifies login credentials.
        """
        if self.url == "https://myopenhab.org" or self.url == "https://myopenhab.org/":
            self.url = "https://myopenhab.org"
            self.isCloud = True
            url = self.url
        else:
            if self.url[-1] == "/":
                self.url = self.url[:-1]
            self.isCloud = False
            url = self.url + "/rest"

        try:
            login_response = self.session.get(url, auth=self.auth, timeout=8)
            login_response.raise_for_status()

            if login_response.ok or login_response.status_code == 200:
                self.isLoggedIn = True
        except requests.exceptions.HTTPError as errh:
            print(errh)
        except requests.exceptions.ConnectionError as errc:
            print(errc)
        except requests.exceptions.Timeout as errt:
            print(errt)
        except requests.exceptions.RequestException as err:
            print(err)

    def __executeRequest(self, header: dict = None, resourcePath: str = None, method: str = None, data = None):
        """
        Executes an HTTP request to the OpenHAB server.

        :param header: Optional; A dictionary of headers to be sent with the request.
        :param resourcePath: The path of the resource to interact with.
        :param method: The HTTP method (GET, POST, PUT, DELETE).
        :param data: Optional; The data to send in the request (for POST and PUT requests).
        :return: The response of the request, either as JSON or plain text.
        :raises ValueError: If the method is invalid or if the resource path is not provided.
        """
        if resourcePath is not None and method is not None:
            method = method.lower()

            # Set header to an empty dictionary if None
            header = header or {}

            if resourcePath[0] != "/":
                resourcePath = "/" + resourcePath

            if not "/rest" in resourcePath:
                resourcePath = "/rest" + resourcePath

            self.session.headers.update(header)

            try:
                if method == "get":
                    response = self.session.get(self.url + resourcePath, auth=self.auth, timeout=5)
                    response.raise_for_status()

                    if response.ok or response.status_code == 200:
                        if response.headers.get("Content-Type", "").startswith("application/json"):
                            return response.json()
                        else:
                            return response.text
                elif method == "put":
                    response = self.session.put(self.url + resourcePath, auth=self.auth, data = data, timeout=5)
                    response.raise_for_status()

                    return response
                elif method == "post":
                    response = self.session.post(self.url + resourcePath, auth=self.auth, data = data, timeout=5)
                    response.raise_for_status()

                    return response
                elif method == "delete":
                    response = self.session.delete(self.url + resourcePath, auth=self.auth, timeout=5)
                    response.raise_for_status()

                    return response
                else:
                    raise ValueError('The entered HTTP method is not valid for accessing the REST API!')
            except requests.exceptions.HTTPError as errh:
                print(errh)
            except requests.exceptions.ConnectionError as errc:
                print(errc)
            except requests.exceptions.Timeout as errt:
                print(errt)
            except requests.exceptions.RequestException as err:
                print(err)
        else:
            raise ValueError('You have to enter a valid resource path for accessing the REST API!')

    def get(self, endpoint: str, header: dict = None):
        """
        Sends a GET request to the OpenHAB server.

        :param endpoint: The endpoint for the GET request (e.g., "/items").
        :param header: Optional; Headers to be sent with the request.
        :return: The response from the GET request, either as JSON or plain text.
        """
        return self.__executeRequest(header, endpoint, "get")

    def post(self, endpoint: str, header: dict = None, data = None):
        """
        Sends a POST request to the OpenHAB server.

        :param endpoint: The endpoint for the POST request (e.g., "/items").
        :param header: Optional; Headers to be sent with the request.
        :param data: Optional; The data to send in the POST request.
        :return: The response from the POST request.
        """
        return self.__executeRequest(header, endpoint, "post", data = data)

    def put(self, endpoint: str, header: dict = None, data = None):
        """
        Sends a PUT request to the OpenHAB server.

        :param endpoint: The endpoint for the PUT request (e.g., "/items").
        :param header: Optional; Headers to be sent with the request.
        :param data: Optional; The data to send in the PUT request.
        :return: The response from the PUT request.
        """
        return self.__executeRequest(header, endpoint, "put", data = data)

    def delete(self, endpoint: str, header: dict = None, data = None):
        """
        Sends a DELETE request to the OpenHAB server.

        :param endpoint: The endpoint for the DELETE request (e.g., "/items").
        :param header: Optional; Headers to be sent with the request.
        :param data: Optional; The data to send in the DELETE request.
        :return: The response from the DELETE request.
        """
        return self.__executeRequest(header, endpoint, "delete", data = data)
