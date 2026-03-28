from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from repository.balance_repo import BalanceRepo
from exceptions.balance_exceptions import (
    ConcurrencyException,
    InsufficientBalanceException
)

class BalanceService:

    MAX_RETRIES = 3

    def __init__(self, repo: BalanceRepo):
        self.repo = repo

    async def update_balance(
        self,
        account_id: UUID,
        delta: int,
        conn: AsyncSession
    ) -> int:

        for attempt in range(self.MAX_RETRIES):

            balance = await self.repo.get_balance(account_id, conn)

            if not balance:
                raise ValueError("Balance not found")

            new_amount = balance.amount + delta
            if new_amount < 0:
                raise InsufficientBalanceException()

            success = await self.repo.update_balance(
                account_id=account_id,
                old_version=balance.version,
                new_amount=new_amount,
                conn=conn
            )

            if success:
                return new_amount

        # Only reaches here if all retries failed due to version mismatch
        raise ConcurrencyException("Too much contention")