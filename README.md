# IN226056002_RAG_Final-Project

---

## 1. Introduction

### 1.1 Overview
This system implements a **Retrieval-Augmented Generation (RAG)** pipeline to enhance customer support automation. It combines information retrieval with large language models to generate accurate, context-aware responses.

---

### 1.2 Objectives
- Improve response accuracy using knowledge grounding  
- Reduce hallucinations in LLM outputs  
- Enable scalable and automated customer support  
- Provide fallback through Human-in-the-Loop (HITL)  

---

## 2. System Architecture

The system integrates multiple components:

- **Retrieval Layer** → ChromaDB (vector database)  
- **LLM Layer** → Groq (primary) / Gemini (fallback)  
- **Workflow Layer** → LangGraph (orchestration engine)  
- **API Layer** → FastAPI  
- **UI Layer** → Streamlit  

---

## 3. Design Decisions

### 3.1 Chunk Size
- Chunk size: **800 characters**  
- Overlap: **100 characters**  

**Reason:**  
Balances context preservation and retrieval efficiency.

---

### 3.2 Embedding Strategy
- Model: `all-mpnet-base-v2` (HuggingFace)  
- Runs locally  

**Advantages:**
- No API cost  
- Fast and scalable  
- Good semantic understanding  

---

### 3.3 Retrieval Approach
Hybrid retrieval is used:

- **Semantic Search** → Vector similarity (ChromaDB)  
- **Keyword Search** → BM25  

**Benefit:**
Improves recall and relevance of retrieved documents.

---

### 3.4 Prompt Design
Prompts are structured to:
- Use only retrieved context  
- Avoid hallucination  
- Maintain conversational clarity  


---

## 4. Workflow Explanation

### 4.1 LangGraph Usage
LangGraph is used to define a **graph-based execution workflow** instead of a linear pipeline.

---

### 4.2 Node Responsibilities

| Node | Responsibility |
|------|---------------|
| Retrieve | Fetch relevant documents |
| Intent | Classify query intent |
| Agent | Generate response |
| Evaluate | Score response confidence |
| HITL | Handle escalation |
| Memory | Store conversation history |

---

### 4.3 State Transitions

A shared state object flows through nodes:

```python
{
  "query": str,
  "intent": str,
  "context": list,
  "response": str,
  "confidence": float,
  "escalate": bool,
  "history": list
}
