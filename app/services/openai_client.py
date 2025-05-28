import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

prompt_path = os.path.join(os.path.dirname(__file__), "..", "utils", "prompt.txt")
with open(os.path.abspath(prompt_path), "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

def ask_openai(messages: list[dict[str, str]]) -> dict:
    full_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=full_messages,
        temperature=0.5,
        max_tokens=300,
    )
    return {
        "answer": response.choices[0].message.content,
        "model": response.model,
        "tokens_used": response.usage.total_tokens
    }