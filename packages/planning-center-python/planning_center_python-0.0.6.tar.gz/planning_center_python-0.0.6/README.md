<!-- README.md -->
[![Build Status](https://github.com/andy-goellner/pco-python-sdk/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/andy-goellner/pco-python-sdk/actions?query=branch%main)
[![Coverage Status](https://coveralls.io/repos/github/andy-goellner/pco-python-sdk/badge.svg?branch=main)](https://coveralls.io/github/andy-goellner/pco-python-sdk?branch=main)
![PyPI - Version](https://img.shields.io/pypi/v/planning-center-python)

# pco-python-sdk
A Python SDK for simplifying interactions with the Planning Center API.


## NOTE: WIP. This library is not stable and is under active development. I will release a 1.x.x version when the library has reached a stable state.

## Currently only supporting the latest version of all the APIs. Will come up with a better versioning strategy after 1.0

## Need to install
poetry
python
ruff
pre-commit

## NOTE: Not currently supporting the json fields in the attribute payloads

# Getting Started

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install planning_center_python
```

## Contributing

This project is under active development. Feel free to contribute and submit a pull request. The project is managed with poetry and tests use pytest.

# Docs

## Webhooks

You can validate a webhook using the `WebhookSignature` class. Pass the request headers, the body of the request, and the secret to `.verify` which will return `True/False` depending if the signature is verified. A `SignatureVerificationError` will be raise for any exceptions.


## Auth and Client Setup

There is a class called `PCOToken` that wraps the token dict returned from `https://api.planningcenteronline.com/oauth/token`. NOTE: The inital auth => redirect token fetch is not yet supported.

Once you have a token instance you need to initialize a set of credentials (`Credentials`). `Credentials` takes a `client_id`, `client_secret`, a `pco_token`, and a `token_updater`. `token_updater` is a callable function that takes one argument `token` and is used to store a new token whenever a token refresh is triggered.

Create an instance of a `PCOClient` using the `Credentials` and you are off and running. You can access api resources from the client.

```python
from planning_center_python.api import PCOClient, Credentials, PCOToken

def token_saver(token):
    print(token)

client_id = "myclientid"
secret = "mysecretkey"
token = {
    "access_token": "pco_tok_abc",
    "token_type": "Bearer",
    "expires_in": 7199,
    "refresh_token": "abcdefg",
    "scope": ["people", "services"],
    "created_at": 1737307589,
    "expires_at": 1737314788.50569,
}
pco_token = PCOToken(token)
credentials = Credentials(
    client_id=client_id,
    client_secret=secret,
    pco_token=pco_token,
    token_updater=token_saver,
)
client = PCOClient(credentials=credentials)
person = client.person.get("personid")
```

NOTE: The client is a singleton. You only need to initialize it once with an `http_client` or `credentials` from then on you can call `PCOClient()` to return the already configured client.
