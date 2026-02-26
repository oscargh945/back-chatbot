import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

logger = logging.getLogger(__name__)


def _init_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("La variable de entorno OPENAI_API_KEY no está configurada")
    return OpenAI(api_key=api_key)


def _load_system_prompt() -> str:
    prompt_path = Path(__file__).parent.parent / "utils" / "prompt.txt"
    try:
        return prompt_path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        raise RuntimeError(f"No se encontró el archivo de prompt: {prompt_path}")


client = _init_client()
SYSTEM_PROMPT = _load_system_prompt()


def ask_openai(messages: list) -> dict:
    serialized = [
        m.model_dump() if hasattr(m, "model_dump") else dict(m)
        for m in messages
    ]
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + serialized

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=full_messages,
        temperature=0.5,
        max_tokens=300,
    )
    return {
        "answer": response.choices[0].message.content,
        "model": response.model,
        "tokens_used": response.usage.total_tokens,
    }
