from dataclasses import dataclass
from typing import Optional

@dataclass
class AccountNumber: 
    currency: str 
    id: Optional[int] = None