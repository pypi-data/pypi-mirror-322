import json
from typing import Mapping


class PCOResponse(object):
    def __init__(
        self,
        body: str,
        code: int,
        headers: Mapping[str, str],
    ) -> None:
        self.code = code
        self.headers = headers
        self.body = body
        self.data = json.loads(body)
