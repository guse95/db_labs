from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import KnowledgeForTicket, get_db
from app.schemas.knowledge_for_ticket import KnowledgeLink

router = APIRouter(prefix = "/tickets", tags=["Knowledge for tickets"])

@router.post("/add-knowledge", response_model=KnowledgeLink)
async def add_knowledge_to_ticket(
    link_data: KnowledgeLink,
    db: AsyncSession = Depends(get_db)
):
    link = KnowledgeForTicket(**link_data.dict())

    db.add(link)

    await db.commit()
    await db.refresh(link)

    return link

@router.get("/{ticket_id}/knowledges")
async def get_knowledges(
    ticket_id: int,
    page: int = 1,
    limit: int = 10,
    sort: str = "knowledge_id",
    order: str = "asc",
    db: AsyncSession = Depends(get_db)
):
    query = select(KnowledgeForTicket).where(KnowledgeForTicket.ticket_id == ticket_id)

    if order == "desc":
        query = query.order_by(getattr(KnowledgeForTicket, sort).desc())
    else:
        query = query.order_by(getattr(KnowledgeForTicket, sort).asc())

    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()
