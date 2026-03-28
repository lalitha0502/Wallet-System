from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict
from enum import Enum
from uuid import UUID


from utils.datetime_util import utc_now

class ProcessState(Enum):
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"

@dataclass
class Transaction:
    idempotency_key: str
    user_id: UUID
    sender_account_id: UUID
    receiver_account_id: UUID
    transaction_id: UUID
    amount: int # least unit of curreny like paisa or cent
    currency: str
    reference_type: str
    reference_id: str
    state: ProcessState = ProcessState.CREATED
    metadata: Optional[Dict] = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self):
        if self.amount <= Decimal("0"):
            raise ValueError("Amount must be positive")
