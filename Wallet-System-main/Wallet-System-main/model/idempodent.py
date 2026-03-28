from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from utils.datetime_util import utc_now
from model.transaction import ProcessState

class IdempodentStatus(Enum): 
    CREATED = "CREATED"
    PROCESSING = "PROCESSING"
    FAILED  = "FAILED"
    SUCCESS = "SUCCESS"
    
@dataclass
class IdempotencyKey:
    idempotency_key: str
    user_id: int
    request_hash: str
    status: ProcessState
    transaction_id: Optional[int] = None
    response: Optional[str] = None
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
