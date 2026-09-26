from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent import (
    ingest_receipt_proactively,
    answer_shopper_query,
)


app = FastAPI(title="CODEX Retail Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    "https://codex-retail-agent-web.vercel.app",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReceiptRequest(BaseModel):
    receipt: str


class ChatRequest(BaseModel):
    message: str


active_session = None


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/load-receipt")
def load_receipt(request: ReceiptRequest):
    global active_session

    if not request.receipt.strip():
        raise HTTPException(status_code=400, detail="Receipt is empty.")

    result = ingest_receipt_proactively(request.receipt)

    active_session = result["session"]
    print("CODEX SESSION LOADED:", active_session is not None)

    return {
        "status": "ok",
        "order_id": result["receipt_data"].get("order_id"),
        "summary": result["proactive_summary"],
    }


@app.post("/chat")
def chat(request: ChatRequest):
    if active_session is None:
        print("CODEX CHAT: NO ACTIVE SESSION")
        return {
            "response": "Please load a receipt first so CODEX can analyze your purchase."
        }

    print("CODEX CHAT: ACTIVE SESSION FOUND")

    try:
        response = answer_shopper_query(
            active_session,
            request.message,
        )

        return {
            "response": response,
        }

    except Exception as e:
        print("CODEX CHAT ERROR:", str(e))
        return {
            "response": f"CODEX encountered an error: {str(e)}"
        }