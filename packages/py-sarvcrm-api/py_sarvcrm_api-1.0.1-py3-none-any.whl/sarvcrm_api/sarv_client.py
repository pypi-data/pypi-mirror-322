import json, hashlib
from requests import Response, request
from typing import Optional, Self
from datetime import datetime, timedelta, timezone

from .sarv_url import SarvFrontend, SarvURL

from .exceptions import SarvException
from ._mixins import ModulesMixin
from .type_hints import TimeOutput, SarvLanguageType, RequestMethod, SarvGetMethods

from .modules._base import SarvModule


class SarvClient(ModulesMixin):
    """
    SarvClient provides methods for interacting with the SarvCRM API. 
    It supports authentication, data retrieval, and other API functionalities.
    """

    def __init__(
            self,
            utype: str,
            username: str,
            password: str,
            api_url: str = SarvURL,
            frontend_url: str = SarvFrontend,
            login_type: Optional[str] = None, 
            language: SarvLanguageType = 'en_US',
            is_password_md5: bool = False,
            ) -> None:
        """
        Initialize the SarvClient.

        Args:
            utype (str): The user type for authentication.
            username (str): The username for authentication.
            password (str): The password for authentication.
            api_url (str): URL of the sarvcrm API, if you dont use the cloud version specify the local server.
            frontend_url (str): Frontend url for link generation, if you dont use the cloud version specify the local server.
            login_type (Optional[str]): The login type for authentication.
            language (SarvLanguageType): The language to use, default is 'en_US'.
            is_password_md5 (bool): Whether the password is already hashed using MD5.
        """

        self.utype = utype
        self.username = username
        self.login_type = login_type
        self.language = language
        self.api_url = api_url
        self.frontend_url = frontend_url

        if is_password_md5 == True:
            self.password = password
        else:
            self.password = hashlib.md5(password.encode('utf-8')).hexdigest()

        self.token: str = ''

        super().__init__()


    def create_get_parms(
            self, 
            sarv_get_method: Optional[SarvGetMethods] = None,
            sarv_module: Optional[SarvModule | str] = None,
            **addition
            ) -> dict:
        """
        Create the GET parameters with the method and module.

        Args:
            sarv_get_method (SarvGetMethods): The API method to call.
            sarv_module (Optional[SarvModule | str]): The module name or object.
            addition: Additional parameters to include in the GET request.

        Returns:
            dict: The constructed GET parameters.
        """
        module_name = None

        if sarv_module is not None:
            if isinstance(sarv_module, SarvModule):
                module_name = sarv_module._module_name
            elif isinstance(sarv_module, str):
                module_name = sarv_module
            else:
                raise TypeError(f'Module type must be instance of SarvModule or str not {sarv_module.__class__.__name__}')
        
        get_parms = {
            'method': sarv_get_method,
            'module': module_name,
        }
        get_parms = {k: v for k, v in get_parms.items() if v is not None}

        if addition:
            get_parms.update(**addition)

        return get_parms


    def iso_time_output(output_method: TimeOutput, dt: datetime | timedelta) -> str:
        """
        Generate a formatted string from a datetime or timedelta object.

        These formats are compliant with the SarvCRM API time standards.

        Args:
            output_method (TimeOutput): Determines the output format ('date', 'datetime', or 'time').
            dt (datetime | timedelta): A datetime or timedelta object.

        Returns:
            str: A string representing the date, datetime, or time.
                - date: "YYYY-MM-DD"
                - datetime: "YYYY-MM-DDTHH:MM:SS+HH:MM"
                - time: "HH:MM:SS"
        """
        if isinstance(dt, timedelta):
            dt = datetime.now(timezone.utc) + dt

        if output_method == 'date':
            return dt.date().isoformat()

        elif output_method == 'datetime':
            return dt.astimezone().isoformat(timespec="seconds")

        elif output_method == 'time':
            return dt.time().isoformat(timespec="seconds")

        else:
            raise TypeError(f'Invalid output method: {output_method}')


    def send_request(
            self, 
            request_method: RequestMethod, 
            head_parms: Optional[dict] = None,
            get_parms: Optional[dict] = None,
            post_parms: Optional[dict] = None,
            ) -> dict:
        """
        Send a request to the Sarv API and return the response data.

        Args:
            request_method (RequestMethod): The HTTP method for the request ('GET', 'POST', etc.).
            head_parms (dict): The headers for the request.
            get_parms (dict): The GET parameters for the request.
            post_parms (dict): The POST parameters for the request.

        Returns:
            dict: The data parameter from the server response.

        Raises:
            SarvException: If the server returns an error response.
        """

        head_parms = head_parms or {}
        get_parms = get_parms or {}
        post_parms = post_parms or {}

        # Default Header
        head_parms['Content-Type'] = 'application/json'

        if self.token:
            head_parms['Authorization'] = f'Bearer {self.token}'

        response:Response = request(
            method=request_method,
            url = self.api_url,
            params = get_parms,
            headers = head_parms,
            json = post_parms,
            verify = True,
            )

        # Check for Server respond
        if 200 <= response.status_code < 500:
            try:
                # Deserialize sarvcrm servers response
                response_dict: dict = json.loads(response.text)

            # Checking for invalid response
            except json.decoder.JSONDecodeError:
                if 'MySQL Error' in response.text:
                    response_dict: dict = {
                        'message': 'There are Errors in the database\nif you are sending raw SQL Query to server please check syntax and varibles'
                    }

                else:
                    response_dict: dict = {'message': 'Unkhown error'}

            except Exception as e:
                raise SarvException(
                    f'There is problem while converting response to json: {e}'
                    )

        else:
            # Raise on server side http error
            response.raise_for_status()

        # Initiate server response
        if 200 <= response.status_code < 300:
            data = response_dict.get('data', {})
            return data

        elif 300 <= response.status_code < 400:
            raise SarvException(
                f"Redirection Response: {response.status_code} - {response_dict.get('message', 'Unknown error')}"
            )

        else:
            raise SarvException(
                f"{response.status_code} - {response_dict.get('message', 'Unknown error')}"
            )


    def login(self) -> str:
        """
        Authenticate the user and retrieve an access token.

        Returns:
            str: The access token for authenticated requests.
        """
        post_parms = {
            'utype': self.utype,
            'user_name': self.username,
            'password': self.password,
            'login_type': self.login_type,
            'language': self.language,
            }
        post_parms = {k: v for k, v in post_parms.items() if v is not None}

        data = self.send_request(
            request_method='POST',
            get_parms=self.create_get_parms('Login'), 
            post_parms=post_parms,
            )

        if data:
            self.token = data.get('token')

        return self.token


    def logout(self) -> None:
        """
        Clears the access token from the instance.

        This method should be called to invalidate the session.
        """
        if self.token:
            self.token = ''


    def search_by_number(
            self,
            number: str,
            module: Optional[SarvModule | str] = None
            ) -> list[dict]:
        """
        Search the CRM by phone number and retrieve the module item.

        Args:
            number (str): The phone number to search for.
            module (Optional[SarvModule | str]): The module to search in.

        Returns:
            dict: The data related to the phone number if found.
        """
        return self.send_request(
            request_method='GET',
            get_parms=self.create_get_parms('SearchByNumber', sarv_module=module, number=number),
            )


    def get_detail_url_by_number(
            self,
            number: str,
    ) -> str:
        """
        Returns the frontned url of full detail view of number.

        Args:
            number (str): The phone number to create url.
        
        Returns:
            str: url of the detail detail view.
        """
        return f'{self.frontend_url}?utype={self.utype}&module=Customer_Console&callerid={number}'
        

    def __enter__(self) -> Self:
        """Basic Context Manager for clean code execution"""
        self.login()
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        """Basic Context Manager for clean code execution"""
        self.logout()


    def __repr__(self):
        """
        Provides a string representation for debugging purposes.

        Returns:
            str: A string containing the class name and key attributes.
        """
        return f'{self.__class__.__name__}(utype={self.utype}, username={self.username})'


    def __str__(self) -> str:
        """
        Provides a human-readable string representation of the instance.

        Returns:
            str: A simplified string representation of the instance.
        """
        return f'<SarvClient {self.utype}>'
