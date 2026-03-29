from typing import Annotated, List, Union, TypedDict, Dict, Any
from pydantic import BaseModel, Field

class TaxAgentState(TypedDict):
    """
    Centralized state for the Tax Agent LangGraph.
    """
    task_id: str
    framework: str # e.g., "ITR-4", "GSTR-3B"
    raw_inputs: List[Dict[str, Any]] # Raw data from ML ingestion or MCP
    documents: List[Dict[str, Any]] # Uploaded documents
    normalized_ledger: Dict[str, Any]
    external_web_context: Dict[str, Any] # Data from TinyFish
    applicable_rules: List[str] # Retrieved from Qdrant
    computation_results: Dict[str, Any]
    balance_sheet: Dict[str, Any]
    analysis_report: str # Intelligent Data Analysis
    validation_errors: List[str]
    human_approval_status: str # "pending", "approved", "rejected"
    final_payload: Dict[str, Any] # Ready for submission
    shared_id: str # UUID shared with Weaviate and PostgreSQL
