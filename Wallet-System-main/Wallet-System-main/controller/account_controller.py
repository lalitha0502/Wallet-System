from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schema.account_schema import (
    AddAccountRequest,
    AddAccountResponse,
    GetAccountByAccountIdequest,
    GetAccountByAccountNameRequest,
    GetAccountResponse,
)

from service.account_service import AccountService
from core.dependencies import get_account_service
from core.database import get_db

from exceptions.account_exceptions import AccountNotFound


router = APIRouter(prefix="/accounts", tags=["Accounts"])


# CREATE ACCOUNT
@router.post(
    "/",
    response_model=AddAccountResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_account(
    request: AddAccountRequest,
    user_id: UUID,  # Replace with Depends(get_current_user) later
    session: AsyncSession = Depends(get_db),
    account_service: AccountService = Depends(get_account_service),
) -> AddAccountResponse:

    try:
        return await account_service.addAccount(
            account_details=request,
            user_id=user_id,
            conn=session,
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create account",
        )


# GET ACCOUNT BY ACCOUNT NUMBER
@router.post(
    "/by-number",
    response_model=GetAccountResponse,
    status_code=status.HTTP_200_OK,
)
async def get_account_by_number(
    request: GetAccountByAccountNameRequest,
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    account_service: AccountService = Depends(get_account_service),
) -> GetAccountResponse:

    try:
        return await account_service.getAccountByAccountName(
            account_details=request,
            user_id=user_id,
            conn=session,
        )

    except AccountNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


# GET ACCOUNT BY ACCOUNT ID
@router.post(
    "/by-id",
    response_model=GetAccountResponse,
    status_code=status.HTTP_200_OK,
)
async def get_account_by_id(
    request: GetAccountByAccountIdequest,
    user_id: UUID,
    session: AsyncSession = Depends(get_db),
    account_service: AccountService = Depends(get_account_service),
) -> GetAccountResponse:

    try:
        return await account_service.getAccountByAccountId(
            account_details=request,
            user_id=user_id,
            conn=session,
        )

    except AccountNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )