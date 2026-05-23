from pydantic import BaseModel

class KnowledgeCreate(BaseModel):
    title: str
    knowledge_base_content: str


class KnowledgeResponse(KnowledgeCreate):
    id: int

    class Config:
        from_attributes = True