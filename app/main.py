from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import time
import uuid

from modules.ingestion import load_and_index
from modules.hybrid_retrieval import HybridRetriever
from app.graph import build_graph

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default"

app = FastAPI(
    title="RAG Customer Support Assistant",
    version="2.0"
)
memory_store = {}
try:
    print("🔄 Loading knowledge base...")

    vectordb, docs = load_and_index()
    retriever = HybridRetriever(vectordb, docs)

    graph = build_graph(retriever)

    print("✅ System ready!")

except Exception as e:
    print("❌ Initialization failed:", str(e))
    raise e

def stream_text(text):
    for word in text.split():
        yield word + " "
        time.sleep(0.02)

@app.get("/")
def root():
    return {"message": "API running"}

@app.post("/query")
def query_api(req: QueryRequest):
    try:
        session_id = req.session_id

        if session_id not in memory_store:
            memory_store[session_id] = []

        result = graph.invoke({
            "query": req.query,
            "history": memory_store[session_id]
        })

        memory_store[session_id].append({
            "user": req.query,
            "bot": result["response"]
        })

        return {
                    "answer": result.get("response", ""),
                    "confidence": result.get("confidence", 0.0),
                    "escalated": result.get("escalate", False) 
                }

    except Exception as e:
        print("❌ Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/query_stream")
def query_stream(req: QueryRequest):
    try:
        session_id = req.session_id

        if session_id not in memory_store:
            memory_store[session_id] = []

        result = graph.invoke({
            "query": req.query,
            "history": memory_store[session_id]
        })

        memory_store[session_id].append({
            "user": req.query,
            "bot": result["response"]
        })

        return StreamingResponse(
            stream_text(result["response"]),
            media_type="text/plain"
        )

    except Exception as e:
        print("❌ Streaming error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))