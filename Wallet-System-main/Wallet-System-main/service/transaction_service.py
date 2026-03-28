from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from service.base_service import BaseService
from model.transaction import Transaction, ProcessState
from repository.transaction_repo import TransactionRepo

from exceptions.transaction_exception import (
    TransactionUnableToChangeState,
    TransactionNotFound,
)


class TransactionService(BaseService):

    def __init__(self, repo: TransactionRepo) -> None:
        self.repo: TransactionRepo = repo


    async def create(
        self,
        transaction: Transaction,
        conn: AsyncSession,
    ) -> None:

        if transaction is None:
            raise ValueError("Transaction required")

        await self.repo.addTransaction(transaction, conn)


    async def get_by_idempotency(
        self,
        user_id: UUID,
        idempotency_key: str,
        conn: AsyncSession,
    ) -> Optional[Transaction]:

        return await self.repo.getTransaction(
            user_id=user_id,
            idempotency_key=idempotency_key,
            conn=conn,
        )


    async def update_state(
        self,
        transaction: Transaction,
        new_state: ProcessState,
        conn: AsyncSession,
    ) -> Transaction:

        if transaction is None:
            raise TransactionNotFound()

        if not self._is_valid_transition(transaction.state, new_state):
            raise TransactionUnableToChangeState(
                f"Invalid transition {transaction.state} → {new_state}"
            )

        updated = await self.repo.updateState(
            transaction,
            new_state,
            conn,
        )

        if not updated:
            raise TransactionUnableToChangeState()

        return updated

    def _is_valid_transition(
        self,
        current: ProcessState,
        new: ProcessState,
    ) -> bool:

        valid_transitions = {
            ProcessState.PROCESSING: {
                ProcessState.SUCCESS,
                ProcessState.FAILED,
            },
        }

        return new in valid_transitions.get(current, set())