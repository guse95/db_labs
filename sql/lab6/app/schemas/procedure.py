from pydantic import BaseModel

class CreateTicketWithKB(BaseModel):
    title: str
    description: str
    client_id: int
    kb_id: int