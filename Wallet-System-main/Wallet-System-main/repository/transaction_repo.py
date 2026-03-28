import uuid
from dataclasses import asdict
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from repository.base_repo import BaseRepo
from model.transaction import Transaction, ProcessState
from utils.model_utils import map_to_dataclass

class TransactionRepo(BaseRepo):
    table = "transactions"
    ALLOWED_TRANSITIONS = {
        ProcessState.CREATED: {ProcessState.PROCESSING},
        ProcessState.PROCESSING: {ProcessState.SUCCESS, ProcessState.FAILED},
        ProcessState.SUCCESS: set(),
        ProcessState.FAILED: set(),
    }
    async def addTransaction(self, transaction: Transaction, conn: AsyncSession) -> None: 
        if not transaction:
            raise ValueError("Transaction Not Defined")
        
        data = asdict(transaction)
        data['state'] = data['state'].value
        data = {k: v for k, v in data.items() if v is not None}
        if not data:
            raise ValueError("Transaction Not Defined")
        
        columns = ", ".join(list(data.keys()))
        placeholder = ", ".join(f" :{k}" for k in data.keys())
        
        query = text(f"""
                INSERT INTO {self.table} ({columns})
                VALUES ({placeholder})
        """)
        await conn.execute(query, params=data)
        
    async def getTransaction(self, user_id: uuid.UUID, idempotency_key: str, conn: AsyncSession) -> Optional[Transaction]:
        if not user_id or not idempotency_key:
            raise ValueError("Invalid Argument passed")
        
        query = text (f"""
                    SELECT  * 
                    FROM {self.table}
                    WHERE user_id = :user_id 
                    AND idempotency_key = :idempotency_key 
            """)
        
        result = await conn.execute(query, params={
                'user_id': user_id, 
                'idempotency_key': idempotency_key,
            })
        
        new_row = result.mappings().one_or_none
        if not new_row:
            return None
        
        transaction = map_to_dataclass(Transaction, new_row)
        return transaction      
    
    async def updateState(self, transaction: Transaction, new_state: ProcessState, conn: AsyncSession) -> Optional[Transaction]:
        if not transaction:
            raise ValueError("Invalid Argument Passed")

        old_state = transaction.state
        if not new_state in self.ALLOWED_TRANSITIONS.get(old_state):
            return None

        query = text(f"""
            UPDATE {self.table}
            SET state = :state
            WHERE transaction_id = :transaction_id
            AND state = :old_state
        """)

        result = await conn.execute(
            query,
            params={
                "state": new_state.value,
                "transaction_id": transaction.transaction_id,
                "old_state": old_state.value,
            }
        )

        if result.rowcount == 0:
            return None

        transaction.state = new_state
        return transaction