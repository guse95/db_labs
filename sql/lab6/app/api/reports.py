from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db import get_db

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)

@router.get("/tickets-by-status")
async def tickets_by_status(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(text("""
        SELECT status, COUNT(*) as total
        FROM tickets
        GROUP BY status
    """))

    return result.mappings().all()


@router.get("/top-clients")
async def top_clients(
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(text("""
        SELECT c.client_name, COUNT(t.id) as tickets_count
        FROM clients c
        JOIN tickets t ON c.id = t.client_id
        GROUP BY c.client_name
        ORDER BY tickets_count DESC
        LIMIT 10
    """))

    return result.mappings().all()