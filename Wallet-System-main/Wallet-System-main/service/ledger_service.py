from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from repository.ledger_repo import LedgerRepository
from model.ledger import Ledger, TransferType


class LedgerService:
    def __init__(self, repo: LedgerRepository):
        self.repo = repo

    async def create_ledger_entry(
        self,
        ledger_id: UUID,
        account_id: UUID,
        transaction_id: UUID,
        amount: int,
        transfer_type: TransferType,
        balance_after: int,
        conn: AsyncSession
    ) -> None:

        if amount <= 0:
            raise ValueError("Ledger amount must be positive")

        ledger = Ledger(
            ledger_id=ledger_id,
            account_id=account_id,
            transaction_id=transaction_id,
            amount=amount,
            type=transfer_type,
            balance_after=balance_after
        )

        await self.repo.addLedger(ledger, conn)