from uuid import UUID

from dataclasses import dataclass

@dataclass
class Balance:
    balance_id: UUID
    account_id: UUID
    version: int 
    amount: int
