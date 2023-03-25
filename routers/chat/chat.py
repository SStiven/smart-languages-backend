from fastapi import APIRouter, Depends
from datetime import datetime

router = APIRouter()

@router.post("/chat/exchange")
async def add_exchange(exchange: str):
    request_time = datetime.now()
    return {"time" : request_time}