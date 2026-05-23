from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import Tickets, get_db
from app.schemas.tickets import TicketCreate, TicketResponse

router = APIRouter(prefix = "/tickets", tags=["Tickets"])

@router.get("/")
async def get_tickets(
    status: str | None = None,
    page: int = 1,
    limit: int = 10,
    sort: str = "id",
    order: str = "asc",
    db: AsyncSession = Depends(get_db)
):
    query = select(Tickets)

    if status:
        query = query.where(Tickets.status == status)

    if order == "desc":
        query = query.order_by(getattr(Tickets, sort).desc())
    else:
        query = query.order_by(getattr(Tickets, sort).asc())

    query = query.offset((page - 1) * limit).limit(limit)

    result = await db.execute(query)

    return result.scalars().all()

@router.patch("/{ticket_id}/status")
async def change_ticket_status(
    ticket_id: int,
    status: str,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Tickets).where(Tickets.id == ticket_id)
    )

    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    ticket.status = status

    await db.commit()
    await db.refresh(ticket)

    return {
        "message": "Status updated",
        "ticket": ticket.id,
        "new_status": ticket.status
    }

@router.get("/{ticket_id}", response_model=TicketResponse)
async def get_ticket(ticket_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Tickets).where(Tickets.id == ticket_id)
    )

    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    return ticket


@router.post("/", response_model=TicketResponse)
async def create_ticket(
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db)
):
    ticket = Tickets(**ticket_data.dict())

    db.add(ticket)

    await db.commit()
    await db.refresh(ticket)

    return ticket


@router.put("/{ticket_id}", response_model=TicketResponse)
async def update_ticket(
    ticket_id: int,
    ticket_data: TicketCreate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Tickets).where(Tickets.id == ticket_id)
    )

    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    for key, value in ticket_data.dict().items():
        setattr(ticket, key, value)

    await db.commit()
    await db.refresh(ticket)

    return ticket


@router.delete("/{ticket_id}")
async def delete_ticket(
    ticket_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Tickets).where(Tickets.id == ticket_id)
    )

    ticket = result.scalar_one_or_none()

    if not ticket:
        raise HTTPException(404, "Ticket not found")

    await db.delete(ticket)
    await db.commit()

    return {"message": "Ticket deleted"}
