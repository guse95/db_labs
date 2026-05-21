from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, Request

from app.db import get_db, Clients

router = APIRouter()

@router.post("/create")
async def create_client(request: Request, db: AsyncSession = Depends(get_db)):
    new_client = Clients(
        client_name=request.form.get("name"),
        client_age=request.form.get("age"),
        email=request.form.get("email"),
    )

    db.add(new_client)
    await db.commit()
    db.refresh(new_client)
    return new_client