import uuid

from repository.user_repo import UserRepo
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError


from schema.user_schema import (
    AddUserRequest, AddUserResponse,
    RemoveUserRequest, RemoveUserResponse
)
from utils.password_manager import PasswordManager
from exceptions.user_exceptions import UsernameAlreadyExists, EmailAlreadyExists, UserNotFound
from model.user import User
from service.base_service import BaseService

class UserService(BaseService): 
    def __init__(self, user_repo: UserRepo, password_manager: PasswordManager):
        self.user_repo = user_repo
        self.password_manager = password_manager
        
    async def addUser(self, user_details : AddUserRequest, conn: AsyncSession) -> AddUserResponse:        
        try:
            async with self.transaction_scope(conn):
                password_hash = self.password_manager.hash(user_details.password)
                user = User(
                    user_id=uuid.uuid4(),
                    password_hash=password_hash,
                    email=user_details.email,
                    username=user_details.username, 
                    first_name=user_details.first_name,
                    last_name=user_details.last_name,
                    address=user_details.address
                )

                await self.user_repo.add_user(user, conn)

        except IntegrityError as e:
            constraint = getattr(e.orig.diag, "constraint_name", None)

            if constraint == "users_username_key":
                raise UsernameAlreadyExists()
            elif constraint == "users_email_key":
                raise EmailAlreadyExists()
            else:
                raise
        return AddUserResponse.model_validate(user)


    async def deleteUser(self, user_details: RemoveUserRequest, conn: AsyncSession) -> RemoveUserResponse:
        try: 
            async with self.transaction_scope(conn) as db:
                await self.user_repo.delete_user(
                    user_id=user_details.user_id, 
                    conn=db
                )
        except UserNotFound as e:
            raise e
        
        return RemoveUserResponse(user_id=user_details.user_id)
    
