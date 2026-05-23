from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db import get_db

router = APIRouter(tags=["Functions"])

@router.get("/is-agent-busy/{agent_id}")
async def is_agent_busy(
    agent_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        text("""
            SELECT is_agent_busy(:agent_id)
        """),
        {"agent_id": agent_id}
    )

    busy = result.scalar()

    return {
        "agent_id": agent_id,
        "is_busy": busy
    }


@router.post("/close-ticket/{ticket_id}")
async def close_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db)
):
    await db.execute(
        text("SELECT close_ticket(:ticket_id)"),
        {"ticket_id": ticket_id}
    )

    await db.commit()

    return {"message": "Ticket closed"}