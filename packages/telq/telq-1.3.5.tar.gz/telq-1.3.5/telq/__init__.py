import datetime as dt
from typing import Dict, List, Union

import telq.authentication as authentication
from telq.session.session_data import SessionData
from telq.supplier.supplier_data import SupplierData
from telq.networks import Networks
from telq.tests import Test
from telq.tests import MT
from telq.tests import LNT
from telq.supplier import Supplier
from telq.session import Session


class TelQTelecomAPI:
    """Connects to the TelQ Telecom API to perform operations such as obtaining
    a list with our available networks, send tests and consult test results.

    By default the TelQTelecomAPI uses the API Version 3.0 which can be changed
    with the API version parameter.

    NOTES
    ----------
    Please kindly be informed that this Python SDK supports API version version from 2.1 only

    Parameters
    ----------
    api_version : str, default 'v3'
        API version to use, defaults to version 'v2.2'
        Versions 1.0, 1.1, 1.2, 1.3 and 1.4 have been deprecated. This means no new development or bug fixes
        will occur on those versions, but they will continue to be supported
        by our app through 2021. We may stop supporting them at some point in the future
        but we will give ample warning to all our customers about it.

    Examples
    --------
    Initialise the TelQTelecomAPI class
    >>> telq_api = TelQTelecomAPI(base_url="https://api.telqtele.com")

    Authenticate the TelQ API by simply passing your App Id and App Key.
    If there are no errors, it means you have been authenticated.

    >>> telq_api.authenticate(api_id="<yourAppKey>", api_key="<yourAppId>")

    After authentication, you can get the list of available networks

    >>> telq_api.get_networks()
    [{'mcc': '350',
      'countryName': 'Bermuda',
      'mnc': '01',
      'providerName': 'Digicel',
      'portedFromMnc': None,
      'portedFromProviderName': None},
      {'mcc': '310',
      'countryName': 'United States of America',
      'mnc': '012',
      'providerName': 'Verizon',
      'portedFromMnc': '260',
      'portedFromProviderName': 'T-Mobile'},
      ...
      'mnc': '03',
      'providerName': 'Claro',
      'portedFromMnc': None,
      'portedFromProviderName': None},
      ...]

    Request New Tests

    >>> telq_api.initiate_new_tests(destinationNetworks= [{'mcc': '310',
    ...                                                   'countryName': 'United States of America',
    ...                                                   'mnc': '012',
    ...                                                   'providerName': 'Verizon',
    ...                                                   'portedFromMnc': '260',
    ...                                                   'portedFromProviderName': 'T-Mobile'}
    ...                                                 ])
    [{'id': 13754642,
      'testIdText': 'woOMJtrQAy',
      'phoneNumber': '14045183990',
      'errorMessage': None,
      'destinationNetwork': {'mcc': '310', 'mnc': '012', 'portedFromMnc': '260'},
      'testIdTextType': 'ALPHA',
      'testIdTextCase': 'MIXED',
      'testIdTextLength': 10}]

    Test Results

    >>> telq_api.get_test_results(test_id=13754642)
    {'id': 13754642,
     'testIdText': 'woOMJtrQAy',
     'senderDelivered': None,
     'textDelivered': None,
     'testCreatedAt': '2022-05-13T19:46:38.011254Z',
     'smsReceivedAt': None,
     'receiptDelay': None,
     'testStatus': 'WAIT',
     'destinationNetworkDetails': {'mcc': '310',
      'mnc': '012',
      'portedFromMnc': '260',
      'countryName': 'United States of America',
      'providerName': 'Verizon',
      'portedFromProviderName': 'T-Mobile'},
     'smscInfo': None,
     'pdusDelivered': []}
    """

    _last_time_authenticated = None
    _authenticated: authentication.Authentication
    supplier: Supplier
    session: Session
    mt: MT
    lnt: LNT
    network: Networks

    def __init__(self, base_url: str = "https://api.telqtele.com", api_version: str = "v3") -> None:
        self.api_version = api_version
        self.base_url = base_url

    def __init_clients(self):
        try:
            self.session = Session(self._authenticated)
            self.supplier = Supplier(self._authenticated)
            self.mt = MT(self._authenticated)
            self.lnt = LNT(self._authenticated)
            self.network = Networks(self._authenticated)

        except AttributeError:
            raise RuntimeError(
                "You must be authenticated first - call the authenticate method passing your App Id and Key "
            )

    def authenticate(self, api_id: str, api_key: str):
        """Authenticates the App Id and Key.

        NOTE
        ----------
        Please note that each authentication lasts for only 24 hours, you will be required to
        authenticate every 24 hours

        Parameters
        ----------
        api_id : str
            TelQ uses API key pairs (appId, appKey) to allow access to the API.
            You can find your AppId and generate your AppKey on the API Menu of the TelQ App.
        api_key : str
            Your AppKey gotten from the API Menu of the TelQ App
        """ ""
        if not api_id or not api_key:
            raise ValueError("API credentials are not set")
        try:
            # if the user has been authenticated before
            # and its within 24 hours since the last time the user was authenticated
            if self._last_time_authenticated and (
                    dt.datetime.utcnow() -
                    self._last_time_authenticated) < dt.timedelta(days=1):
                print("Already authenticated")
            # if 24 hours has elapased
            else:
                self._authenticated = authentication.Authentication(
                    api_id=api_id, api_key=api_key, api_version=self.api_version, base_url=self.base_url
                )
                self._last_time_authenticated = dt.datetime.now()
        except AttributeError:
            # if the user has never been authenticated
            self._authenticated = authentication.Authentication(
                api_id=api_id, api_key=api_key, api_version=self.api_version, base_url=self.base_url
            )
            self._last_time_authenticated = dt.datetime.now()
        self.__init_clients()
