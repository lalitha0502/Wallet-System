from dataclasses import asdict
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from model.balance import Balance


class BalanceRepo:
    async def addBalance(self, balance: Balance, conn: AsyncSession) -> None:
        query = text("""
            INSERT INTO balances (
                balance_id,
                account_id,
                version,
                amount
            )
            VALUES (
                :balance_id,
                :account_id,
                :version,
                :amount
            )
        """)

        await conn.execute(query, asdict(balance))
    
    async def get_balance(
        self,
        account_id: UUID,
        conn: AsyncSession
    ) -> Balance | None:

        query = text("""
            SELECT balance_id, account_id, version, amount
            FROM balances
            WHERE account_id = :account_id
        """)

        result = await conn.execute(query, {"account_id": account_id})
        row = result.fetchone()

        if not row:
            return None

        return Balance(
            balance_id=row.balance_id,
            account_id=row.account_id,
            version=row.version,
            amount=row.amount
        )

    async def update_balance(
        self,
        account_id: UUID,
        old_version: int,
        new_amount: int,
        conn: AsyncSession
    ) -> bool:

        query = text("""
            UPDATE balances
            SET amount = :new_amount,
                version = version + 1
            WHERE account_id = :account_id
              AND version = :old_version
        """)

        result = await conn.execute(
            query,
            {
                "account_id": account_id,
                "old_version": old_version,
                "new_amount": new_amount
            }
        )

        return result.rowcount == 1