from typing import Optional, TypedDict


class PaginationParams(TypedDict):
    per_page: Optional[int]
    offset: Optional[int]
