from typing import Any, List, Mapping, cast
import datetime as dt


class PCOToken:
    def __init__(self, params: Mapping[str, Any]) -> None:
        self.token_type = "bearer"
        self.access_token = cast(str, params.get("access_token"))
        self.refresh_token = cast(str, params.get("refresh_token"))
        self.scope = cast(List[str], params.get("scope"))
        self.created_at = cast(float, params.get("created_at"))
        self.expires_at = cast(float, params.get("expires_at"))

    @property
    def expires_in(self) -> float:
        if not self.expires_at:
            return 1

        print("calculating expires_in")
        # time in seconds
        expires_at = dt.datetime.fromtimestamp(self.expires_at, dt.timezone.utc)
        current_timestamp = dt.datetime.now(dt.timezone.utc)
        return (expires_at - current_timestamp).total_seconds()

    def as_dict(self) -> Mapping[str, Any]:
        return {
            "access_token": self.access_token,
            "expires_at": self.expires_at,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "scope": self.scope,
            "token_type": self.token_type,
        }
