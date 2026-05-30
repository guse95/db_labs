from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import KnowledgeBase, get_db
from app.schemas.knowledge_base import KnowledgeCreate, KnowledgeResponse

router = APIRouter(prefix="/knowledge_base", tags=["KnowledgeBase"])

@router.get("/", response_model=list[KnowledgeResponse])
async def get_knowledge(
    page: int = 1,
    limit: int = 10,
    sort: str = "id",
    is_desc_order: bool | None = False,
    db: AsyncSession = Depends(get_db)
):
    query = select(KnowledgeBase)

    if is_desc_order:
        query = query.order_by(getattr(KnowledgeBase, sort).desc())
    elif is_desc_order == False:
        query = query.order_by(getattr(KnowledgeBase, sort).asc())

    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()


@router.get("/{knowledge_id}", response_model=KnowledgeResponse)
async def get_knowledge(knowledge_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == knowledge_id)
    )

    knowledge = result.scalar_one_or_none()

    if not knowledge:
        raise HTTPException(404, "Knowledge not found")

    return knowledge


@router.post("/", response_model=KnowledgeResponse)
async def create_knowledge(
    knowledge_data: KnowledgeCreate,
    db: AsyncSession = Depends(get_db)
):
    knowledge = KnowledgeBase(**knowledge_data.dict())

    db.add(knowledge)

    await db.commit()
    await db.refresh(knowledge)

    return knowledge


@router.put("/{knowledge_id}", response_model=KnowledgeResponse)
async def update_knowledge(
    knowledge_id: int,
    knowledge_data: KnowledgeCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == knowledge_id)
    )

    knowledge = result.scalar_one_or_none()

    if not knowledge:
        raise HTTPException(404, "Knowledge not found")

    for key, value in knowledge_data.dict().items():
        setattr(knowledge, key, value)

    await db.commit()
    await db.refresh(knowledge)

    return knowledge


@router.delete("/{knowledge_id}")
async def delete_knowledge(
    knowledge_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(KnowledgeBase).where(KnowledgeBase.id == knowledge_id)
    )

    knowledge = result.scalar_one_or_none()

    if not knowledge:
        raise HTTPException(404, "Knowledge not found")

    await db.delete(knowledge)
    await db.commit()

    return {"message": "Knowledge deleted"}