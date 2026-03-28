from abc import ABC

from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager 

from repository.base_repo import BaseRepo

class BaseService(ABC):        
    @asynccontextmanager
    async def transaction_scope(self, conn: AsyncSession):
        async with conn.begin():
            yield conn
                