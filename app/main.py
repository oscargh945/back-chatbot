import logging
import os
from typing import Literal

from fastapi import FastAPI, HTTPException
from openai import OpenAIError
from pydantic import BaseModel, field_validator
from starlette.middleware.cors import CORSMiddleware

from app.services.openai_client import ask_openai

logger = logging.getLogger(__name__)

app = FastAPI()

_raw_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5500,http://127.0.0.1:5500")
ALLOWED_ORIGINS = [o.strip() for o in _raw_origins.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str

    @field_validator("content")
    @classmethod
    def content_no_vacio_ni_largo(cls, v):
        if not v or not v.strip():
            raise ValueError("El contenido no puede estar vacío")
        if len(v) > 4000:
            raise ValueError("El mensaje supera el límite de 4000 caracteres")
        return v.strip()


class QuestionRequest(BaseModel):
    messages: list[ChatMessage]

    @field_validator("messages")
    @classmethod
    def messages_validos(cls, v):
        if not v:
            raise ValueError("Se requiere al menos un mensaje")
        if len(v) > 30:
            raise ValueError("El historial no puede superar los 30 mensajes")
        return v


@app.post("/chat")
def chat(request: QuestionRequest):
    try:
        answer = ask_openai(request.messages)
        return answer
    except OpenAIError as e:
        logger.error("OpenAI API error: %s", e)
        raise HTTPException(status_code=502, detail="Servicio de IA no disponible")
    except Exception:
        logger.exception("Error inesperado en /chat")
        raise HTTPException(status_code=500, detail="Error interno del servidor")
