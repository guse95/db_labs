from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import Clients, get_db
from app.schemas.clients import ClientCreate, ClientResponse

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.get("/", response_model=list[ClientResponse])
async def get_clients(
    page: int = 1,
    limit: int = 10,
    sort: str = "id",
    order: str = "asc",
    db: AsyncSession = Depends(get_db)
):
    query = select(Clients)

    if order == "desc":
        query = query.order_by(getattr(Clients, sort).desc())
    else:
        query = query.order_by(getattr(Clients, sort).asc())

    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()


@router.get("/{client_id}", response_model=ClientResponse)
async def get_client(client_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Clients).where(Clients.id == client_id)
    )

    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(404, "Client not found")

    return client


@router.post("/", response_model=ClientResponse)
async def create_client(
    client_data: ClientCreate,
    db: AsyncSession = Depends(get_db)
):
    try:
        client = Clients(**client_data.dict())

        db.add(client)

        await db.commit()
        await db.refresh(client)

        return client

    except DBAPIError as e:
        await db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e.orig)
        )


@router.put("/{client_id}", response_model=ClientResponse)
async def update_client(
    client_id: int,
    client_data: ClientCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Clients).where(Clients.id == client_id)
    )

    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(404, "Client not found")

    for key, value in client_data.dict().items():
        setattr(client, key, value)

    await db.commit()
    await db.refresh(client)

    return client


@router.delete("/{client_id}")
async def delete_client(
    client_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Clients).where(Clients.id == client_id)
    )

    client = result.scalar_one_or_none()

    if not client:
        raise HTTPException(404, "Client not found")

    await db.delete(client)
    await db.commit()

    return {"message": "Client deleted"}