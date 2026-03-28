from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from schema.user_schema import (
    AddUserRequest,
    AddUserResponse,
    RemoveUserRequest,
    RemoveUserResponse,
)

from service.user_service import UserService
from core.dependencies import get_user_service
from core.database import get_db

from exceptions.user_exceptions import (
    UsernameAlreadyExists,
    EmailAlreadyExists,
    UserNotFound,
)

router = APIRouter(prefix="/users", tags=["Users"])


# CREATE USER
@router.post(
    "/",
    response_model=AddUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    request: AddUserRequest,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
) -> AddUserResponse:

    try:
        return await user_service.addUser(
            user_details=request,
            conn=session,
        )

    except UsernameAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username already exists",
        )

    except EmailAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

# delete user
@router.delete(
    "/",
    response_model=RemoveUserResponse,
    status_code=status.HTTP_200_OK,
)
async def delete_user(
    request: RemoveUserRequest,
    session: AsyncSession = Depends(get_db),
    user_service: UserService = Depends(get_user_service),
) -> RemoveUserResponse:

    try:
        return await user_service.deleteUser(
            user_details=request,
            conn=session,
        )

    except UserNotFound:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )