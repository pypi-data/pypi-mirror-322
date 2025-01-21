from requests_oauthlib import OAuth2Session

from planning_center_python.api.credentials import Credentials
from planning_center_python.errors import InvalidCredentialsError

TOKEN_URL = "https://api.planningcenteronline.com/oauth/token"
SCOPES = "people check_ins groups"


class Session(OAuth2Session):
    def __init__(self, credentials: Credentials) -> None:
        self.credentials = credentials

        if not credentials.pco_token and not credentials.access_code:
            raise InvalidCredentialsError(
                "Either PCO Token or Access Code must be provided"
            )

        pco_client_id = self.credentials.client_id
        pco_client_secret = self.credentials.client_secret
        auto_refresh_kwargs = {
            "client_id": pco_client_id,
            "client_secret": pco_client_secret,
        }
        token_updater = self.credentials.token_updater

        if credentials.pco_token:
            super().__init__(  # type: ignore
                pco_client_id,
                auto_refresh_url=TOKEN_URL,
                token=credentials.pco_token.as_dict(),
                auto_refresh_kwargs=auto_refresh_kwargs,
                token_updater=token_updater,
            )
            return

        if credentials.access_code:
            pass
            # TODO: implement the initial token fetch code
