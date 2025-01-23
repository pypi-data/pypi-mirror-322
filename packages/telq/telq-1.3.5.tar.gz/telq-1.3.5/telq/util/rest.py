from typing import Optional
from abc import ABC

import requests
from requests.exceptions import JSONDecodeError

from telq.authentication import Authentication
from telq.util.version import SDK_VERSION

class TelQRest(ABC):
    def __init__(self, authentcation: Optional[Authentication] = None):
        self._authentication = authentcation


    def request(self, url: str, method: str, data: Optional[dict] = None, extra_headers: Optional[dict] = None) -> dict:
        headers = {
            "accept": "*/*",
            "Content-Type": "application/json",
            "User-Agent": f"python-sdk/{SDK_VERSION}"
        }
        if self._authentication:
            headers["Authorization"] = self._authentication._bearer_token
        if extra_headers:
            headers.update(extra_headers)

        response = requests.request(method, url, headers=headers, json=data)

        try:
            res = response.json()
        except JSONDecodeError:
            res = response.text

        try:
            if isinstance(res, dict) and res.get('error') != None:
                raise ValueError(f"Server returned {url} HTTP {response.status_code}: {res}")
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise (e)

        return res if isinstance(res, dict) else {"response": res}
