from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from decimal import Decimal
from enum import Enum
from uuid import UUID

from utils.datetime_util import utc_now

class TransferType(Enum): 
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"

@dataclass
class Ledger:
    ledger_id: UUID
    account_id: UUID
    transaction_id: UUID
    amount: int  # stored in smallest currency unit (e.g. paisa, cents)
    type: TransferType
    balance_after: int  # stored in smallest currency unit (e.g. paisa, cents)
    created_at: datetime = field(default_factory=utc_now)

    def __post_init__(self):
        if isinstance(self.type, str) : 
            try:
                self.type = TransferType(self.type)
            except:
                raise ValueError("Wrong Transfer Type Passed") 
        if not isinstance(self.type, TransferType):
            raise ValueError("type of transfer should be from TransferType enum")