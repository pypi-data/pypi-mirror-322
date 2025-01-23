import os
from dataclasses import dataclass
import warnings
import toml
import requests
import telq.endpoints as endpoints
from telq.util.version import SDK_VERSION


@dataclass
class Authentication:
    """Performs authentication with the App Id and App Key
    The App Id and App Key is validated with the token endpoint

    Parameters
    ----------
    api_id : str
        TelQ uses API keypairs (appId, appKey) to allow access to the API.
        You can find your AppId and generate your AppKey on the API Menu of the TelQ App.
    api_key : str
        Your AppKey gotten from the API Menu of the TelQ App
    api_version : str, default 'v3'
        API version to use, defaults to version 'v3'
        Versions 1.0, 1.1, 1.2, 1.3 and 1.4 have been deprecated. This means no new development or bug fixes
        will occur on those versions, but they will continue to be supported
        by our app through 2021. We may stop supporting them at some point in the future
        but we will give ample warning to all our customers about it.
    base_url : str, default 'https://api.telqtele.com'
        Base URL for TelQ App

    Raises
    ------
    ValueError
        if you pass an API version not supported
    """ ""

    api_id: str
    api_key: str
    base_url: str
    api_version: str = "v3"

    def __post_init__(self) -> None:
        self.headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
            "User-Agent": f"python-sdk/{SDK_VERSION}"
        }
        self.data = {"appId": self.api_id, "appKey": self.api_key, "baseUrl": self.base_url}
        self._validate_api_version()
        self._authenticate_user()

    def _validate_api_version(self) -> None:
        _deprecated_versions = ["v1.0", "v1.1", "v1.2", "v1.3", "v1.4"]
        _currently_supported_versions = ["v1.5", "v2.1", "v3"]

        if self.api_version in _deprecated_versions:
            warnings.warn(
                "Versions 1.0 through 1.4 are deprecated and will not longer be supported in the future",
                DeprecationWarning,
            )
        elif self.api_version in _currently_supported_versions:
            pass
        else:
            raise ValueError(
                "Invalid TelQ API selected - choose a version like 'v2.2' or 'v1.5' and so on - see our documentation for more information"
            )

    def _authenticate_user(self) -> None:
        # pass App Id and App Key to the token endpoint to authenticate user
        url = endpoints.TokenURL(self.base_url, self.api_version).url()
        method = "POST"
        response = requests.request(method, url, headers=self.headers, json=self.data)

        try:
            res = response.json()
            if 'error' in res:
                raise ValueError(res['message'])
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise Exception(e)

        json_obj = response.json()
        self._bearer_token = json_obj["value"]
