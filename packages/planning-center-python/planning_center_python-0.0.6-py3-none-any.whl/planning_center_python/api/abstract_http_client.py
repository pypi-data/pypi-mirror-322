from abc import ABC
from collections.abc import Mapping
from typing import Any, Optional

from planning_center_python.data.api_response.pco_response import PCOResponse


class AbstractHttpClient(ABC):
    """Abstract base class representation for the HTTP client. Should be inherited and overridden."""

    def request(
        self,
        verb: str,
        endpoint: str,
        query: Optional[Mapping[str, str]] = None,
        payload: Optional[Mapping[str, Any]] = None,
        headers: Optional[Mapping[str, str]] = None,
    ) -> PCOResponse:
        raise NotImplementedError
