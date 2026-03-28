from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schema.transfer_money_schemas import (
    TransferMoneyRequest,
    TransferMoneyResponse,
)

from service.transfer_money_service import TransferService

from exceptions.idempodent_exceptions import (
    IdempotencyAlreadyProcessed,
    IdempotencyConflictException,
)
from exceptions.transaction_exception import (
    TransactionUnableToChangeState,
)

from core.database import get_db
from core.dependencies import get_transfer_service


router = APIRouter(prefix="/transfers", tags=["Transfers"])


@router.post(
    "/",
    response_model=TransferMoneyResponse,
    status_code=status.HTTP_201_CREATED,
)
async def transfer_money(
    request: TransferMoneyRequest,
    user_id: UUID,  # Normally from auth middleware
    session: AsyncSession = Depends(get_db),
    transfer_service: TransferService = Depends(get_transfer_service),
) -> TransferMoneyResponse:

    try:
        return await transfer_service.transfer(
            request=request,
            user_id=user_id,
            session=session,
        )

    except IdempotencyAlreadyProcessed as e:
        return TransferMoneyResponse.model_validate(e.response)

    except IdempotencyConflictException:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Request already processing",
        )

    except TransactionUnableToChangeState:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid transaction state transition",
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )