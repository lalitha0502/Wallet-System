from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from uuid import UUID
from datetime import datetime

from utils.datetime_util import utc_now

class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"

@dataclass
class Account:
    user_id: UUID
    account_id: UUID
    account_number: str
    currency: str
    status: AccountStatus = AccountStatus.ACTIVE
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)

    def __post_init__(self) : 
        if isinstance(self.status, str): 
            try:
                self.status = AccountStatus(self.status)
            except:
                raise ValueError(f"Invalid Account Status Passed: {self.status}") 
        
        if not isinstance(self.status, AccountStatus) :
            raise ValueError(f"status must be enum from AccountStatus")  