from contextlib import asynccontextmanager

from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from app.api import ping, clients, agents, views, functions, tickets, knowledge_base, knowledge_for_ticket, reports
from app.db import engine

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        print("Successfully connected to the database")
    yield
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ping.router)
app.include_router(clients.router)
app.include_router(agents.router)
app.include_router(knowledge_base.router)
app.include_router(tickets.router)
app.include_router(knowledge_for_ticket.router)
app.include_router(reports.router)
app.include_router(views.router)
app.include_router(functions.router)