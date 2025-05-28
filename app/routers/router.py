from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.schemas import ChatRequest
from app.services.openai_client import ask_openai

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home():
    with open("static/index.html", "r") as f:
        return f.read()

@app.post("/chat")
async def chat(req: ChatRequest):
    response = await ask_openai(
        message=req.message,
        history=[msg.dict() for msg in req.history] if req.history else None,
        model=req.model,
        temperature=req.temperature
    )
    return {"response": response}