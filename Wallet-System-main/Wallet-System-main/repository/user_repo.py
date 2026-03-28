from dataclasses import asdict
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from model.user import User 
from repository.base_repo import BaseRepo
from utils.model_utils import map_to_dataclass
from exceptions.user_exceptions import UserNotFound


class UserRepo(BaseRepo):
    # Table associated with this repo layer 
    table = 'users'
    USER_FIELDS = {"user_id", "username", "email", "first_name", "last_name"}

    # Func to add the user in the table
    async def add_user(self, user : User, conn: AsyncSession) -> User:
        if not user:
            raise ValueError("No User Object Found") 
        data = asdict(user)
        data = {k: v for k, v in data.items() if v is not None}
        if not data: 
            raise ValueError("No User to Add")
        columns = ', '.join(list(data.keys()))
        placeholder = ', '.join(f':{k}' for k in data.keys())

        query = text(f"""
            INSERT INTO {self.table} ({columns})
            VALUES ({placeholder})
        """)

        result = await conn.execute(query, data)        
        return user     
            
    # Func to delete the user in the table
    async def delete_user(self, user_id: UUID, conn: AsyncSession) -> None:
        if not user_id:
            raise ValueError("Invalid User ID") 
        
        query = text(f"""
            DELETE FROM {self.table}
            WHERE user_id = :user_id
        """)
        
        result = await conn.execute(query, {
                "user_id" : user_id
            })
        if result.rowcount == 0:
            raise UserNotFound()
            
    # Func to Update the User   
    async def update_user(self, user_id: UUID, user: User, conn : AsyncSession) -> None:
        if not user:
            raise ValueError("No User Object Found") 
        data = asdict(user)
        data = {k: v for k, v in data.items() if v is not None}
        if not data: 
            raise ValueError("No fields to update")
        data.pop('user_id', None)      

        placeholder = ', '.join(f'{k}= :{k}' for k in data.keys())
        
        query = text(f"""
            UPDATE {self.table}
            SET {placeholder}
            WHERE user_id = :user_id
        """)
        
        data['user_id'] = user_id
        result = await conn.execute(query, data)
        if result.rowcount == 0:
            raise ValueError("User not found")
    
    # generic function to get user based on field             
    async def get_user(self, field_name: str, field_value: str | UUID | None = None, conn: AsyncSession | None = None) -> User:
        if field_name not in self.USER_FIELDS:
            raise ValueError(f"Invalid field name: {field_name}")
        query = text(f"""
            SELECT * 
            FROM {self.table} 
            WHERE {field_name} = :value            
        """)
        
        result = await conn.execute(query, {
            'value' : field_value
        })
        row = result.mappings().one_or_none()
        if not row : 
            return None
        user = map_to_dataclass(User, row)
        
        return user
    
    # function to get user based on id 
    async def get_user_using_id(self, user_id: UUID, conn: AsyncSession) -> User:
        if not user_id:
            raise ValueError("User ID not Provided")
        user=  await self.get_user('user_id', user_id, conn)
        if not user:
            raise UserNotFound()
        return None
        
    # function to get user based on username 
    async def get_user_using_username(self, username:str , conn: AsyncSession) -> User:
        if not username:
            raise ValueError("Username Not Provided")
        user =  await self.get_user('username', username, conn)
        if not user:
            raise UserNotFound()
        return user
    
    # function to get user based on email 
    async def get_user_using_email(self, email: str, conn: AsyncSession) -> User:
        if not email:
            raise ValueError("Email Not Provided")
        user = await self.get_user('email', email, conn)
        if not user:
            raise UserNotFound()
        return user
    
    # function to find user based on id if exists user else return None 
    async def find_user_using_id(self, user_id: UUID, conn: AsyncSession) -> User:
        if not user_id:
            raise ValueError("User ID not Provided")
        user=  await self.get_user('user_id', user_id, conn)
        if not user:
            raise ValueError("User Not Found")
        return None
        
    # function to find user based on username if exists user else return None 
    async def find_user_using_username(self, username:str , conn: AsyncSession) -> User:
        if not username:
            raise ValueError("Username Not Provided")
        return await self.get_user('username', username, conn)
    
    # function to find user based on email if exists user else return None 
    async def find_user_using_email(self, email: str, conn: AsyncSession) -> User:
        if not email:
            raise ValueError("Email Not Provided")
        return await self.get_user('email', email, conn)
    
