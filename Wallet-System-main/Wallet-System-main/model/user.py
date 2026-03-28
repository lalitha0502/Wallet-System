from typing import Optional
from dataclasses import dataclass, field
from uuid import UUID
from datetime import datetime

from utils.datetime_util import utc_now

@dataclass
class User:
    user_id: UUID
    username: str 
    password_hash: str 
    email: str 
    first_name: str
    last_name: str
    created_at: datetime = field(default_factory=utc_now)
    updated_at: datetime = field(default_factory=utc_now)
    address: Optional[str] = None