from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class TransferMoneyRequest(BaseModel):
    idempotency_key: str = Field(min_length=10)

    sender_account_id: UUID
    receiver_account_id: UUID

    currency: str = Field(min_length=3, max_length=3)

    amount: int = Field(gt=0)

    reference_type: Optional[str] = None
    reference_id: Optional[str] = None

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v: str):
        return v.upper()

    @field_validator("receiver_account_id")
    @classmethod
    def validate_accounts_different(cls, v, info):
        sender = info.data.get("sender_account_id")
        if sender and sender == v:
            raise ValueError("Sender and receiver cannot be same")
        return v
    
class TransferMoneyResponse(BaseModel):
    transaction_id: UUID
    user_id: UUID
    sender_account_id: UUID
    receiver_account_id: UUID 
    message: str = "Transaction Completed"
    
    model_config = {
        "from_attributes": True,
        "extra": "ignore",
    }
    
    