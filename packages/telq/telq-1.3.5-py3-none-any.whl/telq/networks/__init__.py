import requests
import telq.authentication as authentication
from telq.endpoints import NetworksURL


class Networks:
    """Retrieves a list with all our currently available Networks. 
    Please note that the list of available networks updates frequently 
    and we recommend to retrieve the list every minute. 
    
    The returned values (mcc, mnc, portedFromMnc) will be used in the /tests endpoint to request test numbers. 
    
    - mcc is the Mobile Country Code, as defined by The ITU-T Recommendation E.212. 
    This value will always contain 3 digits.
    - mnc is the Mobile Network Code, as defined by The ITU-T Recommendation E.212. 
    This value can be 2 to 3 digits long.
    - portedFromMnc indicates from which mnc the phone number has been ported. 
    If this param is not present, the test number has not been ported and belongs to the original network.

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

    def __init__(self, authentication: authentication.Authentication):
        self._authentication = authentication

    def get_networks(self):
        """Retrieves a list with all our currently available Networks"""
        url = NetworksURL(self._authentication.base_url, self._authentication.api_version).url()
        method = "GET"
        headers = {
            "accept": "application/json",
            "Authorization": self._authentication._bearer_token,
        }
        response = requests.request(method, url, headers=headers)
        res = response.json()
        try:
            if 'error' in res:
                raise ValueError(res['message'])
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            raise (e)
        return res
