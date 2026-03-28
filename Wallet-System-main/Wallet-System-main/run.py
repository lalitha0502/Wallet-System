from fastapi import FastAPI

from controller.user_controller import router as user_router
from controller.account_controller import router as account_router
from controller.transfer_controller import router as transfer_router


app = FastAPI(
    title="Wallet Backend",
    version="1.0.0",
    description="Idempotent wallet & transfer engine",
)


# Include Routers
app.include_router(user_router)
app.include_router(account_router)
app.include_router(transfer_router)