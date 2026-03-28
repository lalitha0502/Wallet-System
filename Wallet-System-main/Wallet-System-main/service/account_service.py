import uuid
import logging

from sqlalchemy.ext.asyncio import AsyncSession

from model.account import Account, AccountStatus
from model.balance import Balance
from service.base_service import BaseService
from repository.account_repo import AccountRepo
from repository.balance_repo import BalanceRepo
from schema.account_schema import (
    AddAccountRequest, AddAccountResponse,
    GetAccountByAccountIdequest,GetAccountByAccountNameRequest, GetAccountResponse
)
from exceptions.account_exceptions import AccountNotFound

class AccountService(BaseService):
    def __init__(self, repo: AccountRepo, balance_repo: BalanceRepo) -> None:
        self.acc_repo = repo
        self.logger = logging.getLogger(self.__class__.__name__)
        self.balance_repo = balance_repo
        
    async def addAccount(self, account_details: AddAccountRequest, user_id: uuid.UUID, conn: AsyncSession):
        try:
            async with self.transaction_scope(conn) as db:

                serial_id = await self.acc_repo.getCurrencySerial(account_details.currency, db)
                account_number = f"{account_details.currency}_{serial_id}"

                account = Account(
                    user_id=user_id,
                    account_id=uuid.uuid4(),
                    account_number=account_number,
                    currency=account_details.currency
                )

                await self.acc_repo.addAccount(account, db)

                balance = Balance(
                    balance_id=uuid.uuid4(),
                    account_id=account.account_id,
                    version=0,
                    amount=account_details.initial_amount or 0
                )

                await self.balance_repo.addBalance(balance, db)

        except Exception as e:
            self.logger.critical(f"Exception Raised: {e}")
            raise

        return AddAccountResponse.model_validate(account)
    
    async def getAccountByAccountName(self, account_details: GetAccountByAccountNameRequest, user_id: uuid.UUID, conn: AsyncSession) -> GetAccountResponse:
        try:
            async with self.transaction_scope(conn) as db:
                account_name = account_details.account_number
                account = await self.acc_repo.getAccountByAccountName(account_name=account_name, user_id=user_id, conn=db)
        except AccountNotFound as e : 
            self.logger.critical(f"Account Not Found")
            raise
        except Exception as e:
            self.logger.critical(f"Exception Raised : {e}")
            raise 
                
        return GetAccountResponse.model_validate(account)
    
    async def getAccountByAccountId(self, account_details: GetAccountByAccountIdequest, user_id: uuid.UUID, conn: AsyncSession) -> GetAccountResponse:
        try:
            async with self.transaction_scope(conn) as db:
                account_id = account_details.account_id
                account = await self.acc_repo.getAccountByAccountId(account_id=account_id, user_id=user_id, conn=db)
        except AccountNotFound as e : 
            self.logger.critical(f"Account Not Found")
            raise 
        except Exception as e:
            self.logger.critical(f"Exception Raised : {e}")
            raise 
        return GetAccountResponse.model_validate(account)

    