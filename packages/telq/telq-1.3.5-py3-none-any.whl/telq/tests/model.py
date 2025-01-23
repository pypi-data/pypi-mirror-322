from dataclasses import dataclass
from typing import Optional


@dataclass
class Test:
    sender: str
    text: str
    testIdTextType: str
    testIdTextCase: str
    testIdTextLength: int
    supplierId: int
    mcc: str
    mnc: str
    portedFromMnc: Optional[str] = None
