from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db import get_db

router = APIRouter(
    prefix="/views",
    tags=["Views"]
)

@router.get("/ticket-info")
async def ticket_info(
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        text(f"""
            SELECT *
            FROM ticket_info
            ORDER BY client_age
            LIMIT {limit}
        """)
    )

    return result.mappings().all()


@router.get("/ticket-info/solved")
async def solved_ticket_info(
        page: int = 1,
        limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        text(f"""
            SELECT *
            FROM ticket_info
            WHERE status = 'решен'
            ORDER BY client_age
            LIMIT {limit}
        """)
    )

    return result.mappings().all()


@router.get("/agent-stats")
async def agent_stats(
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        text(f"""
            SELECT *
            FROM agent_ticket_stats
            ORDER BY ticket_count DESC
            LIMIT {limit}
        """)
    )

    return result.mappings().all()


@router.get("/unassigned-tickets")
async def unassigned_tickets(
    page: int = 1,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        text(f"""
            SELECT *
            FROM unassigned_tickets
            ORDER BY created_at
            LIMIT {limit}
        """)
    )

    return result.mappings().all()