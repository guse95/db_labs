from pydantic import BaseModel
from datetime import datetime

class TicketCreate(BaseModel):
    title: str
    description: str
    client_id: int
    agent_id: int | None
    status: str


class TicketResponse(TicketCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True