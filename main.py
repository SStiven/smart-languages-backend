from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from routers.chat import chat

app = FastAPI()

allowed_origins = ["*",]
allowed_headers = ["*",]
allowed_methods = ["*",]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=allowed_origins,
    allow_methods=allowed_methods,
    allow_headers=allowed_headers
)

app.include_router(chat.router, tags=["Chat"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)