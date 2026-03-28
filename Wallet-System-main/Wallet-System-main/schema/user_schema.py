from typing import Optional
from uuid import UUID
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

class AddUserRequest(BaseModel):
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=8)
    email: EmailStr 
    first_name: str = Field(...,  min_length=1)
    last_name: str = Field(...,  min_length=1)
    address: Optional[str] = None

class AddUserResponse(BaseModel):
    user_id : UUID 
    username: str 
    email: EmailStr 
    created_at: datetime
    message: str = "User Created"
    
    model_config = {
        "from_attributes": True,
        "extra": "ignore",
    }
    
    
class RemoveUserRequest(BaseModel):
    user_id: UUID
    
class RemoveUserResponse(BaseModel):
    user_id: UUID
    message: str = "User Deleted"