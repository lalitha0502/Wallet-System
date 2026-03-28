from uuid import UUID

from dataclasses import asdict
from sqlalchemy import text, bindparam
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.asyncio import AsyncSession
from model.idempodent import IdempotencyKey

def uuids_to_str(obj):
    """
    Recursively converts UUIDs in dicts/lists to strings
    """
    if isinstance(obj, dict):
        return {k: uuids_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [uuids_to_str(v) for v in obj]
    elif isinstance(obj, UUID):
        return str(obj)
    else:
        return obj
    
class IdempotencyRepository:

    table = "idempotency_keys"

    async def get_by_key(
        self,
        idempotency_key: str,
        user_id: int,
        conn: AsyncSession
    ) -> IdempotencyKey | None:

        query = text(f"""
            SELECT *
            FROM {self.table}
            WHERE idempotency_key = :key
              AND user_id = :user_id
        """)

        result = await conn.execute(
            query,
            {"key": idempotency_key, "user_id": user_id}
        )

        row = result.fetchone()
        if not row:
            return None

        return IdempotencyKey(**row._mapping)

    async def insert(
        self,
        key: IdempotencyKey,
        conn: AsyncSession
    ) -> None:

        data = asdict(key)
        data['status'] = data['status'].value
        columns = ", ".join(data.keys())
        placeholders = ", ".join(f":{k}" for k in data.keys())

        query = text(f"""
            INSERT INTO {self.table} ({columns})
            VALUES ({placeholders})
        """)

        await conn.execute(query, data)

    async def update_status(
        self,
        idempotency_key: str,
        user_id: int,
        status: str,
        transaction_id: int | None,
        response: str | None,
        conn: AsyncSession
    ) -> None:
        response_serializable = uuids_to_str(response) if response else None

        query = text(f"""
            UPDATE {self.table}
            SET status = :status,
                transaction_id = :transaction_id,
                response = :response,
                updated_at = NOW()
            WHERE idempotency_key = :key
            AND user_id = :user_id
        """).bindparams(
            bindparam("response", type_=JSONB)  # tell SQLAlchemy this is JSON
        )

        await conn.execute(
            query,
            {
                "status": status,
                "transaction_id": transaction_id,
                "response": response_serializable, 
                "key": idempotency_key,
                "user_id": user_id
            }
        )