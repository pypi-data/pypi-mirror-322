from dataclasses import dataclass
from typing import Optional

@dataclass
class SessionData:
    """
       A class to represent an SMPP session.

       Attributes:
           hostIp (str): SMPP session domain or IP address.
           hostPort (int): SMPP session port.
           systemId (str): SMPP session system_id, 1-16 characters, cannot contain space.
           password (str): SMPP session password, 1-9 characters, only latin characters and numbers are allowed.
           systemType (str): SMPP session system_type, max. 13 chars. (default: None)
           throughput (int): SMPP throughput in SMS per second, allowed values [5-50]. (default: 5)
           destinationTon (int): SMPP destination TON, allowed values [0, 1, 5]. (default: 1)
           destinationNpi (int): SMPP destination NPI, allowed values [0, 1]. (default: 1)
           enabled (bool): Specifies whether the session will be enabled upon creation, true or false. (default: True)
           windowSize (int): SMPP window size, allowed values [1-20]. (default: 1)
           useSsl (bool): Specifies whether the session will use SSL, true or false. (default: False)
           windowWaitTimeout (int): Window wait timeout in ms, min. 10000, max. 300000. (default: 60000)
           smppSessionId (int): Optional parameter to be used for updating session
       """
    hostIp: str
    hostPort: int
    systemId: str
    password: str
    systemType: Optional[str] = None
    throughput: int = 5
    destinationTon: int = 1
    destinationNpi: int = 1
    enabled: bool = True
    windowSize: int = 1
    useSSL: bool = False
    windowWaitTimeout: int = 60000
    smppSessionId: Optional[int] = None
