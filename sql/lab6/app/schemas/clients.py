from pydantic import BaseModel, EmailStr

class ClientCreate(BaseModel):
    client_name: str
    client_age: int
    email: EmailStr


class ClientResponse(ClientCreate):
    id: int

    class Config:
        from_attributes = True