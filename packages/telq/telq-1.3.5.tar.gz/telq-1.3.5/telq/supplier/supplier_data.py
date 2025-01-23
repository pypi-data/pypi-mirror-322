from dataclasses import dataclass
from typing import Optional, List


@dataclass
class SupplierData:
    """
    Represents a supplier assignment.

    Attributes:
        smppSessionId (int): Id of the session to which the new supplier will be assigned.
        supplierName (str): Name of the supplier, max. 30 chars.
        routeType (str): Route type of the supplier, max. 30 chars.
        attributeList (List[str], optional): Attributes of the supplier. Allowed values: ['DOMESTIC', 'INTERNATIONAL', 'TRANSACTIONAL', 'PROMOTIONAL', 'PRE_REGISTRATION', 'SHORT_CODE', 'LONG_CODE', 'TWO_WAY', 'P2P', 'SMSC', 'DLR', 'SPAM']. Default is None.
        comment (str, optional): Custom comment associated with the supplier, max. 100 chars. Default is None.
        serviceType (str, optional): Service type of the supplier, max. 5 chars. Default is None.
        tlv (List[dict], optional): An array of TLV values defined in HEX format for the supplier as: tagHex and valueHex. Default is None.
        udh (List[dict], optional): An array of UDH values defined in HEX format for the supplier as: tagHex and valueHex. Default is None.
        supplierId (int, optional): Optional supplier id to be used for update
    """
    smppSessionId: int
    supplierName: str
    routeType: str
    attributeList: Optional[List[str]] = None
    comment: Optional[str] = None
    serviceType: Optional[str] = None
    tlv: Optional[List[dict]] = None
    udh: Optional[List[dict]] = None
    supplierId: Optional[int] = None
