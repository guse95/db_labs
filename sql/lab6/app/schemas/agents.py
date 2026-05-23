from pydantic import BaseModel, EmailStr

class AgentCreate(BaseModel):
    agent_name: str
    email: EmailStr


class AgentResponse(AgentCreate):
    id: int

    class Config:
        from_attributes = True