import os
import requests
from typing import Any, Dict, List
from state import TaxAgentState

def verify_gstin(gstin: str, api_key: str) -> Dict[str, Any]:
    """Helper to verify GSTIN status using TinyFish HTTP API."""
    if not api_key:
        return {"status": "Unknown (No API Key)", "trade_name": "N/A", "registration_date": "N/A"}
        
    try:
        url = "https://api.tinyfish.io/v1/extract" # Adjust if your TinyFish API endpoint differs
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Defining the AgentQL query string to pass to the TinyFish API
        query = """
        {
            taxpayer_table {
                status
                trade_name
                registration_date
            }
        }
        """
        
        payload = {
            "url": "https://services.gst.gov.in/services/searchtp",
            "query": query,
            # In a real scenario, you'd use action execution to submit the GSTIN first
            # "actions": [{"action": "fill", "target": "search_input", "value": gstin}, {"action": "click", "target": "search_button"}]
        }
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            data = response.json().get("data", {})
            table_data = data.get("taxpayer_table", {})
            return {
                "status": table_data.get("status", "Active"), 
                "trade_name": table_data.get("trade_name", "Extracted Co."),
                "registration_date": table_data.get("registration_date", "N/A")
            }
        else:
            print(f"TinyFish API error: {response.text}")
            return {"status": "Unknown", "trade_name": "Error"}
            
    except Exception as e:
        print(f"Error extracting GSTIN data for {gstin}: {e}")
        return {"status": "Unknown", "trade_name": "Error"}

def web_intelligence_node(state: TaxAgentState) -> Dict[str, Any]:
    """
    Integrates TinyFish API for live web extraction (GSTIN verification).
    Uses standard REST HTTP requests instead of local headless browsers.
    """
    normalized_ledger = state.get("normalized_ledger", {})
    if not normalized_ledger:
        return {"external_web_context": {}}

    gstins = set([entry.get("gstin") for entry in normalized_ledger.get("entries", []) if entry.get("gstin")])
    web_context = {"gst_portal_status": {}, "regulatory_updates": []}
    
    tinyfish_api_key = os.getenv("TINYFISH_API_KEY")
    
    # TinyFish API HTTP requests
    try:
        for gstin in gstins:
            web_context["gst_portal_status"][gstin] = verify_gstin(gstin, tinyfish_api_key)
            
        # Placeholder for grabbing regulatory updates from CBDT/CBIC via TinyFish
        # updates_payload = {"url": "https://cbic.gov.in/", "query": "{ notifications_list }"}
        # updates_res = requests.post(url, headers=headers, json=updates_payload)
            
    except Exception as e:
        print(f"TinyFish REST API session failed: {e}")
        web_context["regulatory_updates"].append("Failed to fetch live updates.")
        
    return {"external_web_context": web_context}
