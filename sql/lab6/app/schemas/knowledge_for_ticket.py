from pydantic import BaseModel

class KnowledgeLink(BaseModel):
    ticket_id: int
    knowledge_id: int