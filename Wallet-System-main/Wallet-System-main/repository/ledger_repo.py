from dataclasses import asdict

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from repository.base_repo import BaseRepo
from model.ledger import Ledger

class LedgerRepository(BaseRepo):
    table = "ledger"
    
    async def addLedger(self, ledger: Ledger, conn: AsyncSession) -> None: 
        if not ledger:
            raise ValueError("Ledger Not Defined")
        
        data = asdict(ledger)
        data['type'] = data['type'].value
        data = {k: v for k, v in data.items() if v is not None}
        if not data:
            raise ValueError("Ledger Not Defined")
        
        columns = ", ".join(list(data.keys()))
        placeholder = ", ".join(f" :{k}" for k in data.keys())
        
        query = text(f"""
                INSERT INTO {self.table} ({columns})
                VALUES ({placeholder})
        """)
        await conn.execute(query, params=data)
        