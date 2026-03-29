from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any, Dict
from graph import tax_app
from state import TaxAgentState

app = FastAPI(title="Bharat Biz Tax Agent A2A Server")

# Allow CORS for local frontend testing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AgentTaskRequest(BaseModel):
    task_id: str
    framework: str
    raw_inputs: list
    approval_status: str = "pending"
    documents: list = []

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/v1/execute")
async def execute_tax_task(request: AgentTaskRequest):
    """
    Exposes the Tax Agent as a JSON-RPC 2.0 / A2A service.
    """
    initial_state = {
        "task_id": request.task_id,
        "framework": request.framework,
        "raw_inputs": request.raw_inputs,
        "human_approval_status": request.approval_status,
        "documents": request.documents
    }
    
    # Run the graph
    config = {"configurable": {"thread_id": request.task_id}}
    try:
        result = tax_app.invoke(initial_state, config)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Returning the final state dict
    return {
        "jsonrpc": "2.0",
        "result": {
            "status": "success",
            "task_id": request.task_id,
            "agent_state": result
        },
        "id": request.task_id
    }

@app.get("/.well-known/agent-card.json")
async def get_agent_card():
    """
    Metadata document advertising agent capabilities.
    """
    with open(".well-known/agent-card.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
