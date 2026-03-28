from model.idempodent import (
    IdempotencyKey,
    IdempodentStatus
)
from repository.idempodent_repo import IdempotencyRepository
from sqlalchemy.ext.asyncio import AsyncSession

from exceptions.idempodent_exceptions import IdempotencyAlreadyProcessed, IdempotencyConflictException


class IdempotencyService:

    def __init__(self, repo: IdempotencyRepository):
        self.repo = repo

    async def start_request(
        self,
        idempotency_key: str,
        user_id: int,
        request_hash: str,
        conn: AsyncSession
    ) -> IdempotencyKey:

        existing = await self.repo.get_by_key(
            idempotency_key,
            user_id,
            conn
        )

        # First time request
        if not existing:
            new_key = IdempotencyKey(
                idempotency_key=idempotency_key,
                user_id=user_id,
                request_hash=request_hash,
                status=IdempodentStatus.CREATED
            )

            await self.repo.insert(new_key, conn)

            return new_key

        # If request body changed → reject
        if existing.request_hash != request_hash:
            raise IdempotencyConflictException(
                "Request payload does not match original"
            )

        # Already success → return stored response
        if existing.status == IdempodentStatus.SUCCESS.value:
            raise IdempotencyAlreadyProcessed(existing.response)

        # Already processing → reject
        if existing.status == IdempodentStatus.PROCESSING:
            raise IdempotencyConflictException("Request still processing")

        print(existing)
        # FAILED → allow retry (optional design choice)
        return existing

    async def mark_processing(
        self,
        idempotency_key: str,
        user_id: int,
        conn: AsyncSession
    ) -> None:

        await self.repo.update_status(
            idempotency_key,
            user_id,
            IdempodentStatus.PROCESSING.value,
            None,
            None,
            conn
        )

    async def mark_success(
        self,
        idempotency_key: str,
        user_id: int,
        transaction_id: int,
        response: str,
        conn: AsyncSession
    ) -> None:

        await self.repo.update_status(
            idempotency_key,
            user_id,
            IdempodentStatus.SUCCESS.value,
            transaction_id,
            response,
            conn
        )

    async def mark_failed(
        self,
        idempotency_key: str,
        user_id: int,
        conn: AsyncSession
    ) -> None:

        await self.repo.update_status(
            idempotency_key,
            user_id,
            IdempodentStatus.FAILED.value,
            None,
            None,
            conn
        )