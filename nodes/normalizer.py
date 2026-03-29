import os
from typing import Any, Dict, List
from state import TaxAgentState

def normalizer_node(state: TaxAgentState) -> Dict[str, Any]:
    """
    Handles structured data intake via MCP interfaces and merges with ML-ingested data.
    """
    mcp_data = state.get("mcp_raw_ledger", [])
    ml_ingested_ledger = state.get("normalized_ledger", {})
    
    # Logic to merge data and de-duplicate
    # For now, merge the mock results
    merged_ledger = {
        "entries": ml_ingested_ledger.get("entries", []) + [
            {
                "date": "2026-03-05",
                "description": "Tally Export: Sales",
                "amount": 50000.0,
                "category": "Revenue",
                "gstin": "27AAACB1234F1Z1"
            }
        ]
    }
    
    return {"normalized_ledger": merged_ledger}
