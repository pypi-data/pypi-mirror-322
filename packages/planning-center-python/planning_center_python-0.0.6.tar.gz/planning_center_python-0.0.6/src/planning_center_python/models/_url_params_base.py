from dataclasses import dataclass
from typing import Any, Dict, Optional

from planning_center_python.models._pagination_params import PaginationParams


@dataclass
class UrlParamsBase:
    include: Optional[list[str]] = None
    order: Optional[str] = None
    pagination: Optional[PaginationParams] = None
    query_params: Optional[dict[str, Any]] = None

    def serialize(self) -> Dict[str, Any]:
        params = {}
        if self.include:
            params["include"] = ",".join(self.include)
        if self.order:
            params["order"] = self.order
        if self.pagination:
            params.update(self.pagination)  # type: ignore
        return params
