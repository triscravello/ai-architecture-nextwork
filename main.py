
from dotenv import load_dotenv
# 1. Load the environment variables immediately before any other local imports execute
load_dotenv(override=True)

from fastapi import FastAPI
from pydantic import BaseModel
import orchestrator  # Now safe to import; the environment is guaranteed to be hydrated

app = FastAPI(title="AI Architecture Demo")

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/ask", response_model=AnswerResponse)
async def ask(request: QuestionRequest):
    # Delegate the work to the orchestrator layer
    answer = await orchestrator.answer_question(request.question)
    return AnswerResponse(answer=answer)
