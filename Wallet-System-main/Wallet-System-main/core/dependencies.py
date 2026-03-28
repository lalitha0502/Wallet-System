from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Repositories
from repository.user_repo import UserRepo
from repository.account_repo import AccountRepo
from repository.balance_repo import BalanceRepo
from repository.ledger_repo import LedgerRepository
from repository.idempodent_repo import IdempotencyRepository
from repository.transaction_repo import TransactionRepo

# Services
from service.user_service import UserService
from service.account_service import AccountService
from service.balance_service import BalanceService
from service.ledger_service import LedgerService
from service.idempodent_service import IdempotencyService
from service.transaction_service import TransactionService
from service.transfer_money_service import TransferService

# Utils 
from utils.password_manager import PasswordManager

def get_user_repo() -> UserRepo:
    return UserRepo()


def get_password_manager() -> PasswordManager:
    return PasswordManager()


def get_user_service(
    user_repo: UserRepo = Depends(get_user_repo),
    password_manager: PasswordManager = Depends(get_password_manager),
) -> UserService:
    return UserService(
        user_repo=user_repo,
        password_manager=password_manager,
    )
    

def get_account_repo() -> AccountRepo:
    return AccountRepo()


def get_balance_repo() -> BalanceRepo:
    return BalanceRepo()

def get_account_service(
    repo: AccountRepo = Depends(get_account_repo),
    balance_repo: BalanceRepo = Depends(get_balance_repo)
) -> AccountService:
    return AccountService(repo, balance_repo)


def get_ledger_repo() -> LedgerRepository:
    return LedgerRepository()


def get_idempotency_repo() -> IdempotencyRepository:
    return IdempotencyRepository()


def get_transaction_repo() -> TransactionRepo:
    return TransactionRepo()

def get_balance_service(
    repo: BalanceRepo = Depends(get_balance_repo),
) -> BalanceService:
    return BalanceService(repo)


def get_ledger_service(
    repo: LedgerRepository = Depends(get_ledger_repo),
) -> LedgerService:
    return LedgerService(repo)


def get_idempotency_service(
    repo: IdempotencyRepository = Depends(get_idempotency_repo),
) -> IdempotencyService:
    return IdempotencyService(repo)


def get_transaction_service(
    repo: TransactionRepo = Depends(get_transaction_repo),
) -> TransactionService:
    return TransactionService(repo)

def get_transfer_service(
    balance_service: BalanceService = Depends(get_balance_service),
    ledger_service: LedgerService = Depends(get_ledger_service),
    idempotency_service: IdempotencyService = Depends(get_idempotency_service),
    transaction_service: TransactionService = Depends(get_transaction_service),
) -> TransferService:

    return TransferService(
        balance_service=balance_service,
        ledger_service=ledger_service,
        idempotency_service=idempotency_service,
        transaction_service=transaction_service,
    )
    
