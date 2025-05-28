from typing import Literal

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware

from app.services.openai_client import ask_openai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # O usa ["http://127.0.0.1:5500"] para ser más seguro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class QuestionRequest(BaseModel):
    messages: list[ChatMessage]

@app.post("/chat")
def chat(request: QuestionRequest):
    try:
        answer = ask_openai(request.messages)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))