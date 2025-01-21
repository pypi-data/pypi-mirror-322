from typing import Optional
from planning_center_python.api._person_service import PersonService
from planning_center_python.api.abstract_http_client import AbstractHttpClient
from planning_center_python.api.credentials import Credentials
from planning_center_python.api.http_client import HttpClient
from planning_center_python.errors import PCOClientInitializationError
from planning_center_python.util._singleton_meta import SingletonMeta


class PCOClient(metaclass=SingletonMeta):
    def __init__(
        self,
        credentials: Optional[Credentials] = None,
        http_client: Optional[AbstractHttpClient] = None,
    ) -> None:
        if not credentials and not http_client:
            raise PCOClientInitializationError()

        if http_client:
            self._http_client = http_client
        if credentials:
            self._http_client = HttpClient(credentials=credentials)

        self.person = PersonService(self._http_client)
