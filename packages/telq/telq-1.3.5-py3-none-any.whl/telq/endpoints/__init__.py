from abc import ABC, abstractmethod
from typing import Optional
from urllib.parse import urljoin
from urllib.parse import urlencode


class TelQURL(ABC):
    """Base class for generating TelQ URLs for the endpoints. This class sets the stage for each endpoint URL

    Attributes
    ----------
    schemes : str
        https
    host : str
        api.telqtele.com

    Parameters
    ----------
    api_version : str
        API version, for example: 'v1.5', defaults to 'v3'
    """ ""

    schemes = "https"
    host = "api.telqtele.com"
    base_url = "https://api.telqtele.com"

    def __init__(self, base_url: str = "https://api.telqtele.com", api_version: str = "v3"):
        self.base_url = base_url
        self.base_path = f"/{api_version}/client"

    def create_base_url(self):
        return self.base_url + self.base_path

    @abstractmethod
    def path(self, **kwargs) -> str:
        raise NotImplementedError

    def url(self, **kwargs):
        return self.create_base_url() + self.path(**kwargs)


class TokenURL(TelQURL):
    """Endpoint for Token authentication"""

    def path(self) -> str:
        return "/token"


class NetworksURL(TelQURL):
    """Endpoint for networks"""

    def path(self) -> str:
        return "/networks"


class TestsURL(TelQURL):
    """Endpoint for tests"""

    def path(self) -> str:
        return "/tests"


class TestsBatchURL(TelQURL):
    """Endpoint for tests"""

    def path(self) -> str:
        return "/lnt/tests"


class ResultsURL(TelQURL):
    """Endpoint for results"""

    def path(self, test_id) -> str:
        return f"/tests/{test_id}"


class BatchResultsURL(TelQURL):
    """Endpoint for batch results"""
    def url(self, date_from: Optional[str], date_to: Optional[str], page: int = 1, size: int = 100, order: str = "asc") -> str:
        query_params = {
            "page": page,
            "size": size,
            "order": order
        }
        if date_from is not None:
            query_params["from"] = date_from
        if date_to is not None:
            query_params["to"] = date_to
        return urljoin(self.create_base_url() + self.path(), "?" + urlencode(query_params))

    def path(self) -> str:
        return f"/lnt/tests"

class SessionURL(TelQURL):
    """Endpoint for session"""
    def path(self) -> str:
        return "/sessions"

class SessionItemURL(TelQURL):
    """Endpoint for session"""
    def url(self, id: Optional[int] = None) -> str:
        return self.create_base_url() + self.path(id)

    def path(self, id: Optional[int] = None) -> str:
        return "/sessions" + f"/{id}" if id else ""

class SessionPageURL(TelQURL):
    """Endpoint for session page result"""
    def url(self, page: int = 1, size: int = 20, order: str = "asc"):
        query_params = {
            "page": page,
            "size": size,
            "order": order
        }
        return urljoin(self.create_base_url() + self.path(), "?" + urlencode(query_params))

    def path(self) -> str:
        return "/sessions"

class SupplierURL(TelQURL):
    """Endpoint for session"""

    def path(self) -> str:
        return "/suppliers"

class SupplierItemURL(TelQURL):
    """Endpoint for session"""

    def url(self, id: Optional[int] = None) -> str:
        return self.create_base_url() + self.path(id)

    def path(self, id: Optional[int] = None) -> str:
        return "/suppliers" + f"/{id}" if id else ""

class SupplierCustomURL(TelQURL):
    """Endpoint for session"""
    def url(self, extra_url: str) -> str:
        return self.create_base_url() + self.path() + extra_url
    def path(self) -> str:
        return "/suppliers"

class SupplierPageURL(TelQURL):
    """Endpoint for session page result"""
    def url(self, page: int = 1, size: int = 20, order: str = "asc"):
        query_params = {
            "page": page,
            "size": size,
            "order": order
        }
        return urljoin(self.create_base_url() + self.path(), "?" + urlencode(query_params))

    def path(self) -> str:
        return "/suppliers"

class SupplierStatusPageURL(TelQURL):
    """Endpoint for session page result"""
    def url(self, page: int = 1, size: int = 20, order: str = "asc"):
        query_params = {
            "page": page,
            "size": size,
            "order": order
        }
        return urljoin(self.create_base_url() + self.path(), "?" + urlencode(query_params))

    def path(self) -> str:
        return "/sessions-suppliers"
