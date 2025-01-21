from typing import Any, Mapping, Optional
from planning_center_python.api.abstract_http_client import AbstractHttpClient
from planning_center_python.data.api_response.pco_response import PCOResponse
from planning_center_python.models.pco_object import PCOObject


class PcoService(object):
    def __init__(self, http_client: AbstractHttpClient) -> None:
        self._http_client = http_client

    def get(self, id: str, params: Any = None) -> PCOObject:
        raise NotImplementedError

    def _request(
        self, verb: str, url: str, params: Optional[Mapping[str, str]] = None
    ) -> PCOResponse:
        if verb == "get":
            query = params
            payload = None
        else:
            query = None
            payload = params
        return self._http_client.request(verb, url, query, payload, {})
