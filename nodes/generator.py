import json
from typing import Any, Dict, List
from state import TaxAgentState

def artifact_generator_node(state: TaxAgentState) -> Dict[str, Any]:
    """
    Formats the computation results into the exact JSON schema required by 
    the government portal (ITR-4 or GSTR-3B) and generates a Standard Balance Sheet.
    """
    results = state.get("computation_results", {})
    if not results:
        return {"final_payload": {}, "balance_sheet": {}}

    # GSTR-3B Payload Schema Mapping 
    gstr_payload = {
        "gstin": "27AAACB1234F1Z1",
        "ret_period": "032026",
        "sup_details": {
            "osup_det": {
                "txval": results.get("revenue", 0),
                "iamt": 0,
                "camt": (results.get("revenue", 0) * 0.09), # CGST 9%
                "samt": (results.get("revenue", 0) * 0.09)  # SGST 9%
            }
        },
        "itc_elg": {
            "itc_avl": [
                {
                    "ty": "ALL_OTHER_ITC",
                    "iamt": results.get("gst_summary", {}).get("total_itc", 0),
                    "camt": 0,
                    "samt": 0
                }
            ]
        }
    }
    
    # Standard Balance Sheet
    balance_sheet = {
        "liabilities": {
            "share_capital": 500000.0,
            "reserves_and_surplus": results.get("taxable_income", 0),
            "current_liabilities": results.get("gst_summary", {}).get("cgst_payable", 0) + results.get("gst_summary", {}).get("sgst_payable", 0)
        },
        "assets": {
            "fixed_assets": 400000.0,
            "current_assets": results.get("revenue", 0) + 100000.0,
            "itc_receivable": results.get("gst_summary", {}).get("total_itc", 0)
        }
    }
    
    return {
        "final_payload": gstr_payload,
        "balance_sheet": balance_sheet
    }
