from typing import Any, Dict, List
import pandas as pd
from state import TaxAgentState

def computation_node(state: TaxAgentState) -> Dict[str, Any]:
    """
    Deterministic Python logic for tax calculations.
    Bypasses LLM reasoning for numerical accuracy.
    """
    normalized_ledger = state.get("normalized_ledger", {}).get("entries", [])
    if not normalized_ledger:
        return {"computation_results": {}}

    # Use pandas for deterministic calculation
    df = pd.DataFrame(normalized_ledger)
    total_revenue = df[df["category"] == "Revenue"]["amount"].sum()
    total_expense = df[df["category"] == "Expense"]["amount"].sum()
    taxable_income = max(0, total_revenue - total_expense)
    
    # 44AD Presumptive Calculation (Mock: 8% of revenue)
    presumptive_income = total_revenue * 0.08
    
    # GST Set-off Logic (Mock)
    igst_itc = 2500.0
    cgst_liablity = 1500.0
    sgst_liability = 1500.0
    
    results = {
        "revenue": total_revenue,
        "expense": total_expense,
        "taxable_income": taxable_income,
        "presumptive_income_44ad": presumptive_income,
        "gst_summary": {
            "total_itc": igst_itc,
            "cgst_payable": max(0, cgst_liablity - (igst_itc / 2)),
            "sgst_payable": max(0, sgst_liability - (igst_itc / 2))
        }
    }
    
    return {"computation_results": results}
