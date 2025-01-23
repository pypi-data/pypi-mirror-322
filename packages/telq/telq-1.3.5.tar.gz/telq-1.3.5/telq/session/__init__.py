from dataclasses import asdict
from telq.endpoints import SessionItemURL, SessionURL
from telq.endpoints import SessionPageURL
from telq.session.session_data import SessionData
from telq.util.rest import TelQRest


class Session(TelQRest):
    """
    Manage SMPP Sessions. You can create, update, delete and retrieve the list of all your existing sessions.
    For details, please refer to the corresponding chapters of this section.

    Parameters
    -------
    authentication: authentication.Authentication
        The authentication class after you have been authenticated

    Raises
    ------
    Exception
        The Exception will display the error code and the message.
        This will happen If there is an error with your request
    """ ""

    def create(self, session: SessionData):
        """Create SMPP session

        Parameters
        --------
        session: SessionData
            Session object data

        Returns
        --------
            dict: A dictionary containing smppSessionId key
        """
        url = SessionURL(self._authentication.base_url, self._authentication.api_version).url()
        method = "POST"
        return self.request(url, method, data=asdict(session))

    def update(self, session: SessionData):
        """Update SMPP session"""
        url = SessionURL(self._authentication.base_url, self._authentication.api_version).url()
        method = "PUT"

        if not session.smppSessionId:
            raise ValueError("smpp_session_id in session required to update")

        self.request(url, method, data=asdict(session))

    def get(self, id: int):
        """Retrieve individual SMPP session

            Returns:
                dict: A dictionary containing the following keys:
                    - 'smppSessionId' (int): Unique identifier of the SMPP session.
                    - 'hostIp' (str): SMPP session domain or IP address.
                    - 'hostPort' (int): SMPP session port.
                    - 'systemId' (str): SMPP session system_id.
                    - 'systemType' (str): SMPP session system_type.
                    - 'throughput' (int): SMPP throughput in SMS per second.
                    - 'destinationTon' (int): SMPP destination TON. Allowed values: [0, 1, 5].
                    - 'destinationNpi' (int): SMPP destination NPI. Allowed values: [0, 1].
                    - 'enabled' (bool): True if the session is currently enabled.
                    - 'userId' (int): Unique identifier of the user that created this session.
                    - 'userName' (str): Username of the user that created this session.
                    - 'online' (bool): True if the session is currently online.
                    - 'lastError' (str): Returns the last error associated with this session.
                    - 'windowSize' (int): Window size. Allowed values: [1-20].
                    - 'useSSL' (bool): True if the session is using SSL protocol.
                    - 'windowWaitTimeout' (int): Window wait timeout in milliseconds.
                    - 'supplierCount' (int): Total number of suppliers assigned to this session object.
        """
        url = SessionItemURL(self._authentication.base_url, self._authentication.api_version).url(id)
        method = "GET"
        return self.request(url, method)

    def delete(self, id: int):
        """Delete individual SMPP session"""
        url = SessionItemURL(self._authentication.base_url, self._authentication.api_version).url(id)
        method = "DELETE"
        return self.request(url, method)

    def list(self, page: int = 1, size: int = 20, order: str = "asc") -> dict:
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
        url = SessionPageURL(self._authentication.base_url, self._authentication.api_version).url(page, size, order)
        method = "GET"
        headers = {
            "accept": "application/json",
            "Authorization": self._authentication._bearer_token,
        }
        return self.request(url, method)
