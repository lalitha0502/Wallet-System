from uuid import UUID, uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from model.transaction import Transaction, ProcessState
from model.ledger import TransferType
from schema.transfer_money_schemas import (
    TransferMoneyRequest,
    TransferMoneyResponse,
)

from service.base_service import BaseService
from service.balance_service import BalanceService
from service.ledger_service import LedgerService
from service.idempodent_service import IdempotencyService
from service.transaction_service import TransactionService

from exceptions.idempodent_exceptions import (
    IdempotencyAlreadyProcessed,
    IdempotencyConflictException,
)


class TransferService(BaseService):

    def __init__(
        self,
        balance_service: BalanceService,
        ledger_service: LedgerService,
        idempotency_service: IdempotencyService,
        transaction_service: TransactionService,
    ) -> None:
        self.balance_service = balance_service
        self.ledger_service = ledger_service
        self.idempotency_service = idempotency_service
        self.transaction_service = transaction_service

    async def transfer(
        self,
        request: TransferMoneyRequest,
        user_id: UUID,
        session: AsyncSession,
    ) -> TransferMoneyResponse:

        async with self.transaction_scope(session) as conn:
            try:
                await self.idempotency_service.start_request(
                    idempotency_key=request.idempotency_key,
                    user_id=user_id,
                    request_hash=str(request.model_dump()),
                    conn=conn,
                )

            except IdempotencyAlreadyProcessed as e:
                return TransferMoneyResponse.model_validate(e.response)

            except IdempotencyConflictException:
                return TransferMoneyResponse(
                    transaction_id=None,
                    user_id=user_id,
                    sender_account_id=request.sender_account_id,
                    receiver_account_id=request.receiver_account_id,
                    message="Transaction PROCESSING",
                )
            
            transaction_id: UUID = uuid4()
            transaction = Transaction(
                transaction_id=transaction_id,
                user_id=user_id,
                idempotency_key=request.idempotency_key,
                sender_account_id=request.sender_account_id,
                receiver_account_id=request.receiver_account_id,
                amount=request.amount,
                currency=request.currency,
                state=ProcessState.PROCESSING,
                reference_id=request.reference_id,
                reference_type=request.reference_type
            )
            await self.transaction_service.create(transaction, conn)
            try:
                sender_balance: int = await self.balance_service.update_balance(
                    account_id=request.sender_account_id,
                    delta=-request.amount,
                    conn=conn,
                )

                receiver_balance: int = await self.balance_service.update_balance(
                    account_id=request.receiver_account_id,
                    delta=request.amount,
                    conn=conn,
                )
                
                print()
                await self.ledger_service.create_ledger_entry(
                    ledger_id=uuid4(),
                    account_id=request.sender_account_id,
                    transaction_id=transaction_id,
                    amount=request.amount,
                    transfer_type=TransferType.DEBIT,
                    balance_after=sender_balance,
                    conn=conn,
                )

                await self.ledger_service.create_ledger_entry(
                    ledger_id=uuid4(),
                    account_id=request.receiver_account_id,
                    transaction_id=transaction_id,
                    amount=request.amount,
                    transfer_type=TransferType.CREDIT,
                    balance_after=receiver_balance,
                    conn=conn,
                )
                await self.transaction_service.update_state(
                    transaction,
                    ProcessState.SUCCESS,
                    conn,
                )

                response = TransferMoneyResponse(
                    transaction_id=transaction_id,
                    user_id=user_id,
                    sender_account_id=request.sender_account_id,
                    receiver_account_id=request.receiver_account_id,
                    message="Transaction Completed",
                )

                await self.idempotency_service.mark_success(
                    idempotency_key=request.idempotency_key,
                    user_id=user_id,
                    transaction_id=transaction_id,
                    response=response.model_dump(),
                    conn=conn,
                )

                return response

            except Exception as e:
                print(e)
                raise 