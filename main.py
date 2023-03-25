from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.chat import chat

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(chat.router, tags=["Chat"])
