from typing import List
from dataclasses import asdict
from telq.endpoints import SupplierItemURL, SupplierStatusPageURL, SupplierURL
from telq.endpoints import SupplierPageURL
from telq.endpoints import SupplierCustomURL
from telq.supplier.supplier_data import SupplierData
from telq.util.rest import TelQRest


class Supplier(TelQRest):
    """
    Manage suppliers. You can create, update, delete and retrieve the list of all your existing sessions.

    Parameters
    -------
    authentication: authentication.Authentication
        The authentication class after you have been authenticated

    Raises
    ------
    Exception
        The Exception will display the error code and the message.
        This will happen If there is an error with your request
    """

    def create(self, supplier: SupplierData):
        """Create SMPP session"""
        url = SupplierURL(self._authentication.base_url, self._authentication.api_version).url()
        method = "POST"
        return self.request(url, method, data=asdict(supplier))

    def update(self, supplier: SupplierData):
        """Update supplier"""
        url = SupplierURL(self._authentication.base_url, self._authentication.api_version).url()
        method = "PUT"

        if not supplier.supplierId:
            raise ValueError("supplierId in supplier required to update")

        return self.request(url, method, data=asdict(supplier))

    def get(self, id: int):
        """Retrieve individual supplier

            Returns:
                dict: A dictionary containing the following keys:
                    supplier_id (int): Unique identifier of the supplier.
                    smpp_session_id (int): Unique identifier of the SMPP session to which the supplier is assigned.
                    supplier_name (str): Name of the supplier.
                    route_type (str): Route type of the supplier.
                    attribute_list (List[str]): Attributes of the supplier. Allowed values: ['DOMESTIC', 'INTERNATIONAL', 'TRANSACTIONAL', 'PROMOTIONAL', 'PRE_REGISTRATION', 'SHORT_CODE', 'LONG_CODE', 'TWO_WAY', 'P2P', 'SMSC', 'DLR', 'SPAM'].
                    comment (str): Custom comment associated with the supplier.
                    user_id (int): Unique identifier of the user that created this supplier.
                    service_type (str): Service type of the supplier.
                    tlv (List[dict]): An array of TLV values defined in HEX format for the supplier as: tagHex and valueHex.
                    udh (List[dict]): An array of UDH values defined in HEX format for the supplier as: tagHex and valueHex.
        """
        url = SupplierItemURL(self._authentication.base_url, self._authentication.api_version).url(id)
        method = "GET"
        return self.request(url, method)

    def delete(self, id: int):
        """Delete individual supplier"""
        url = SupplierItemURL(self._authentication.base_url, self._authentication.api_version).url(id)
        method = "DELETE"
        return self.request(url, method)

    def list(self, page: int = 1, size: int = 20, order: str = "asc"):
        """Get sessions list with pagination.

           Returns:
               dict: A dictionary containing the following keys:
                   - 'content' (list): Contains the list of corresponding session objects. The size of the list is determined by the size request parameter.
                   - 'pageable' (dict): Contains information about the corresponding paginated result such as: page number, sorting info, page size, etc.
                   - 'totalPages' (int): Total number of pages for the selected size of paginated response.
                   - 'last' (bool): True if the corresponding page is the last one.
                   - 'totalElements' (int): Total number of existing sessions.
                   - 'sort' (dict): Returns the sorting configuration of the page.
                   - 'size' (int): Amount of elements per page.
                   - 'number' (int): Current page number.
                   - 'first' (bool): True if the current page is the first.
                   - 'empty' (bool): True if there are no existing sessions.
           """
        url = SupplierPageURL(self._authentication.base_url, self._authentication.api_version).url(page, size, order)
        method = "GET"
        return self.request(url, method)

    def list_status(self, page: int = 1, size: int = 20, order: str = "asc"):
        """This allows you to retrieve live information about your suppliers and their corresponding sessions to check their current availability.

           Returns:
               dict: A dictionary containing the following keys:
                   - 'content' (list): Contains the list of corresponding session-supplier objects (described below). The size of the list is determined by the size request parameter
                   - 'pageable' (dict): Contains information about the corresponding paginated result such as: page number, sorting info, page size, etc.
                   - 'totalPages' (int): Total number of pages for the selected size of paginated response.
                   - 'last' (bool): True if the corresponding page is the last one.
                   - 'totalElements' (int): Total number of existing sessions.
                   - 'sort' (dict): Returns the sorting configuration of the page.
                   - 'size' (int): Amount of elements per page.
                   - 'number' (int): Current page number.
                   - 'first' (bool): True if the current page is the first.
                   - 'empty' (bool): True if there are no existing sessions.
           """
        url = SupplierStatusPageURL(self._authentication.base_url, self._authentication.api_version).url(page, size, order)
        method = "GET"
        return self.request(url, method)

    def assign(self, smpp_session_id: int, supplier_id_list: List[str]):
        """This is a bulk operation that allows our users to re-assign a list of existing suppliers to another SMPP session."""
        url = SupplierCustomURL(self._authentication.base_url, self._authentication.api_version).url("/assign")
        method = "POST"
        data = {
            "smppSessionId": smpp_session_id,
            "supplierIds": supplier_id_list
        }
        return self.request(url, method, data=data)
