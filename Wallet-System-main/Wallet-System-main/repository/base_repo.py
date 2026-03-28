import logging
from abc import ABC
from typing import Tuple, AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_connection

class BaseRepo(ABC):
    def __init__(self, conn: AsyncSession | None = None) -> None:
        self.conn = conn
        self.logger = logging.getLogger(self.__class__.__name__)
    