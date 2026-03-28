import uuid
from pydantic import BaseModel
from typing import Optional

from model.account import AccountStatus

class AddAccountRequest(BaseModel):
    currency: str 
    initial_amount: int
    
class AddAccountResponse(BaseModel):
    account_number: str 
    currency: str 
    status: str 
    message: Optional[str] = "Account Created"
    
    model_config = {
        "from_attributes": True,
        "extra": "ignore",
    }
    
class GetAccountByAccountNameRequest(BaseModel): 
    account_number: str 
    
class GetAccountByAccountIdequest(BaseModel): 
    account_id: uuid.UUID 
    
class GetAccountResponse(BaseModel):
    account_id: uuid.UUID 
    account_number: str 
    currency: str 
    status: AccountStatus
    
    model_config = {
        "from_attributes": True,
        "extra": "ignore",
    }