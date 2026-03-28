import uuid
from dataclasses import asdict 

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from repository.base_repo import BaseRepo
from model.account import Account
from exceptions.account_exceptions import AccountNotFound
from utils.model_utils import map_to_dataclass

class AccountRepo(BaseRepo):
    table = "accounts"
    currency_serial_table = "currency_serial"
    
    async def getCurrencySerial(self, currency: str, conn: AsyncSession) -> int: 
        if not currency:
            raise ValueError("Currency Not Provided")
        
        query = text(f"""
            UPDATE {self.currency_serial_table}
            SET id = id + 1 
            WHERE currency = :currency
            RETURNING id;
        """)

        result = await conn.execute(query, params={
            'currency' : currency
        })
        new_id = result.scalar_one_or_none()

        if new_id is None:
            raise ValueError(f"Currency {currency} not initialized")
        return new_id
    
    async def addAccount(self, account: Account, conn : AsyncSession) -> None:
        if not account:
            raise ValueError("Account details not Provided")
        data = asdict(account)
        data = {k: v for k, v in data.items() if v is not None}
        data['status'] = data['status'].value
        if not data: 
            raise ValueError("Account details not Provided")
        columns = ", ".join(list(data.keys()))
        placeholder = ", ".join(f" :{k}" for k in data.keys())
        query = text(f"""
            INSERT INTO {self.table} ({columns})
            VALUES({placeholder})
        """)
        
        await conn.execute(query, data)
        
    async def getAccountByAccountName(self, account_name: str, user_id: uuid.UUID, conn: AsyncSession) -> Account:
        if not account_name or not user_id:
            raise ValueError("Invalid Paramters") 
        
        query = text(f"""
                SELECT * 
                FROM {self.table}
                WHERE account_number = :account_name 
                AND user_id = :user_id
            """)
        result = await conn.execute(query, params={
                'user_id' : user_id,
                'account_name': account_name
            })
        
        row = result.mappings().one_or_none()
        if not row:
            raise AccountNotFound()
        
        account = map_to_dataclass(Account, row)
        return account
    
    async def getAccountByAccountId(self, account_id: uuid.UUID, user_id: uuid.UUID, conn: AsyncSession) -> Account:
        if not account_id or not user_id:
            raise ValueError("Invalid Paramters") 
        
        query = text(f"""
                SELECT * 
                FROM {self.table}
                WHERE account_id = :account_id 
                AND user_id = :user_id
            """)
        result = await conn.execute(query, params={
                'user_id' : user_id,
                'account_id': account_id
            })
        
        row = result.mappings().one_or_none()
        if not row:
            raise AccountNotFound()
        
        account = map_to_dataclass(Account, row)
        return account
        
