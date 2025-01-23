from typing import Dict, List, Optional, Union

from telq.endpoints import BatchResultsURL, TestsBatchURL
from telq.tests.model import Test
from telq.util.rest import TelQRest


class LNT(TelQRest):
    """ Launch batch tests with LNT API

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

    def initiate_new_tests(
        self,
        tests: List[Test],
        smppValidityPeriod: Optional[int] = None,
        dataCoding: Optional[str] = None,
        sourceTon: Optional[str] = None,
        sourceNpi: Optional[str] = None,
        resultsCallbackUrl: Union[str, None] = None,
        resultsCallbackToken: Optional[str] = None,
        maxCallbackRetries: int = 3,
        testTimeToLiveInSeconds: int = 3600,
        scheduledDeliveryTime: Optional[str] = None,
        replaceIfPresentFlag: bool = False,
        priorityFlag: int = 1,
        sendTextAsMessagePayloadTlv: bool = False,
        commentText: Optional[str] = None,
        tlv: Optional[List[Dict[str, str]]] = None,
        udh: Optional[List[Dict[str, str]]] = None,
    ):
        """Initiate a new lnt batch tests

        Parameters
        ----------
        tests : List[Test]
            List of tests in a batch. Test should be represented with Test class
        resultsCallbackUrl : Union[str, None], optional
            The callback URL where you would like to receive TestResult updates
            anytime your tests status changes, by default None
        resultsCallbackToken : str, optional
            If you would like to authenticate our Test Results Callbacks, you can send an authentication
            token in this parameter. It will be included as the Authorization bearer token of the callbacks
            we make to your server.
        maxCallbackRetries : int, optional
            The maximum number of attempts you want us to try when calling your "callback url" with updates, min. 0 and max. 5. Default is 3.
        dataCoding : str, optional
            SMPP data_coding parameter
            The allowed values are: [00, 01, 03, 08, F0]
            If not specified, our system will determine the appropriate setting based on the sender and text parameters.
        sourceTon : str, optional
            SMPP source_addr_ton parameter
            The allowed values are: [00, 01, 02, 03, 04, 05, 06]
            If not specified, our system will determine the appropriate setting based on the sender parameter.
        sourceNpi : int
            SMPP source_addr_npi parameter
            The allowed values are: [00, 01, 03, 04, 06, 08, 09, 0A, 0E, 12]
            If not specified, our system will determine the appropriate setting based on the sender parameter, optional
        testTimeToLiveInSeconds : int, optional
            The time to live (TTL) for the test, in seconds,
            min. 60(1 min) and max. 10800(3h). Default is 3600(1h)
        smppValidityPeriod : int, optional
            SMPP validity_period parameter in s,
            min. 60(1 min) and max. 86400(1 day)
        scheduledDeliveryTime : str, optional
            SMPP schedule_delivery_time parameter
        replaceIfPresentFlag : int, optional
            SMPP replace_if_present_flag parameter
        priorityFlag : int, optional
            SMPP priority_flag parameter
        sendTextAsMessagePayloadTlv : int, optional
        	Send text as message payload TLV
        commentText : str, optional
            Custom comment associated with the test
        tlv : List[Dict[str, str], optional
            An array of TLV values defined in HEX format for the supplier as: tagHex and valueHex
        udh : List[Dict[str, str], optional
            Udh value for the tests. The datatype for this type is List[Dict]. Dict should
            contain tagHex and valueHex values.

        Returns
        -------
        JSON Response
            The Response consists of an array of Test objects, containing each a destinationNetwork
            and details about the test request. Here is a description of each of the keys contained by a Test object:

        Raises
        ------
        Exception
            When an error occurs, the associated error is returned
        """ ""
        url = TestsBatchURL(self._authentication.base_url, self._authentication.api_version).url()
        method = "POST"
        extra_headers = {}

        if resultsCallbackToken:
            extra_headers["results-callback-token"] = resultsCallbackToken

        data = self._validate_parse_data(
            tests,
            smppValidityPeriod,
            dataCoding,
            sourceTon,
            sourceNpi,
            resultsCallbackUrl,
            maxCallbackRetries,
            testTimeToLiveInSeconds,
            scheduledDeliveryTime,
            replaceIfPresentFlag,
            priorityFlag,
            sendTextAsMessagePayloadTlv,
            commentText,
            tlv,
            udh
        )
        return self.request(url, method, data, extra_headers=extra_headers)


    def get_test_results(self, date_from: Optional[str] = None, date_to: Optional[str] = None, page: int = 1, size: int = 100, order: str = "asc"):
        url = (BatchResultsURL(self._authentication.base_url, self._authentication.api_version)
               .url(date_from, date_to, page, size, order))
        method = "GET"
        return self.request(url, method)


    def _validate_parse_data(
        self,
        tests: List[Test],
        smppValidityPeriod: Optional[int] = None,
        dataCoding: Optional[str] = None,
        sourceTon: Optional[str] = None,
        sourceNpi: Optional[str] = None,
        resultsCallbackUrl: Union[str, None] = None,
        maxCallbackRetries: int = 3,
        testTimeToLiveInSeconds: int = 3600,
        scheduledDeliveryTime: Optional[str] = None,
        replaceIfPresentFlag: bool = False,
        priorityFlag: int = 1,
        sendTextAsMessagePayloadTlv: bool = False,
        commentText: Optional[str] = None,
        tlv: Optional[List[Dict[str, str]]] = None,
        udh: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, str]:
        if len(tests) == 0:
            raise KeyError(
                "at least one test should be supplied in the tests parameter"
            )

        for test in tests:
            if not isinstance(test, Test):
                raise KeyError(
                    "test should be instance of Test class"
                )

        data = {
            "tests": [test.__dict__ for test in tests],
            "resultsCallbackUrl": resultsCallbackUrl,
            "maxCallbackRetries": maxCallbackRetries,
            "dataCoding": dataCoding,
            "sourceTon": sourceTon,
            "sourceNpi": sourceNpi,
            "testTimeToLiveInSeconds": testTimeToLiveInSeconds,
            "smppValidityPeriod": smppValidityPeriod,
            "scheduledDeliveryTime": scheduledDeliveryTime,
            "replaceIfPresentFlag": replaceIfPresentFlag,
            "priorityFlag": priorityFlag,
            "sendTextAsMessagePayloadTlv": sendTextAsMessagePayloadTlv,
            "commentText": commentText,
            "tlv": tlv,
            "udh": udh
        }
        return data
