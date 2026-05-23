from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import Agents, get_db
from app.schemas.agents import AgentCreate, AgentResponse

router = APIRouter(prefix="/agents", tags=["Agents"])

@router.get("/", response_model=list[AgentResponse])
async def get_agents(
    page: int = 1,
    limit: int = 10,
    sort: str = "id",
    order: str = "asc",
    db: AsyncSession = Depends(get_db)
):
    query = select(Agents)

    if order == "desc":
        query = query.order_by(getattr(Agents, sort).desc())
    else:
        query = query.order_by(getattr(Agents, sort).asc())

    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Agents).where(Agents.id == agent_id)
    )

    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(404, "Agent not found")

    return agent


@router.post("/", response_model=AgentResponse)
async def create_agent(
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db)
):
    agent = Agents(**agent_data.dict())

    db.add(agent)

    await db.commit()
    await db.refresh(agent)

    return agent


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: int,
    agent_data: AgentCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Agents).where(Agents.id == agent_id)
    )

    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(404, "Agent not found")

    for key, value in agent_data.dict().items():
        setattr(agent, key, value)

    await db.commit()
    await db.refresh(agent)

    return agent


@router.delete("/{agent_id}")
async def delete_agent(
    agent_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Agents).where(Agents.id == agent_id)
    )

    agent = result.scalar_one_or_none()

    if not agent:
        raise HTTPException(404, "Agent not found")

    await db.delete(agent)
    await db.commit()

    return {"message": "Agent deleted"}