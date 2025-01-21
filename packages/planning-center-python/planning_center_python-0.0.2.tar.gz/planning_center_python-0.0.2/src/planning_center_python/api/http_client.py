import json
from typing import Any, Mapping, Optional
from planning_center_python.api import AbstractHttpClient
from planning_center_python.api.credentials import Credentials
from planning_center_python.api.session import Session
from planning_center_python.data.api_response.pco_response import PCOResponse
from planning_center_python.errors import RequestFailedError


class HttpClient(AbstractHttpClient):
    """An HTTP Client implementation of the AbstractClient. Handles auth and making requests to
    the planning center api.
    """

    def __init__(self, credentials: Credentials):
        self.base_url = "https://api.planningcenteronline.com"
        self.session = Session(credentials)

    def request(
        self,
        verb: str,
        endpoint: str,
        query: Optional[Mapping[str, str]] = None,
        payload: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> PCOResponse:
        url = f"{self.base_url}/{endpoint}"
        body = json.dumps(payload) if payload else payload
        response = self.session.request(
            method=verb,
            url=url,
            params=query,
            json=body,
            headers=headers,
        )
        print(vars(response.request))  ## TODO: Migrate to logging hooks
        print(response.text)  # TODO: Migrate to logging hooks
        if not response.ok:
            raise RequestFailedError(
                message="API Returned an Error", status_code=response.status_code
            )

        return PCOResponse(response.text, response.status_code, response.headers)
