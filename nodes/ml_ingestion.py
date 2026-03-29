import os
import easyocr
from typing import Any, Dict, List
from langchain_aws import ChatBedrock
from pydantic import BaseModel, Field
from state import TaxAgentState
from bedrock_client import get_bedrock_client

# Initialize Bedrock LLM (Claude 3.5 Sonnet)
llm = ChatBedrock(
    model_id=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    client=get_bedrock_client()
)

# Initialize EasyOCR Reader (Local)
# This will download the model on first run (~100MB)
reader = easyocr.Reader(['en'])

class NormalizedEntry(BaseModel):
    date: str
    description: str
    amount: float
    category: str # e.g., "Revenue", "Expense", "Liability"
    vendor_id: str = None
    gstin: str = None

class NormalizedLedger(BaseModel):
    entries: List[NormalizedEntry]

def ml_ingestion_node(state: TaxAgentState) -> Dict[str, Any]:
    """
    ML-Powered Data Ingestion using local OCR for images and 
    Bedrock for high-level structured parsing.
    """
    raw_inputs = state.get("raw_inputs", [])
    processed_texts = []

    for item in raw_inputs:
        # Check if the item looks like a file path to an image
        if isinstance(item, str) and (item.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff'))):
            if os.path.exists(item):
                print(f"Processing local image: {item}")
                results = reader.readtext(item, detail=0) # detail=0 returns just text
                processed_texts.append(" ".join(results))
            else:
                processed_texts.append(f"Image not found at path: {item}")
        else:
            processed_texts.append(str(item))

    combined_input = "\n---\n".join(processed_texts)
    
    if not combined_input:
        return {"normalized_ledger": {"entries": []}}

    # Reasoning prompt for Claude 3.5 Sonnet
    prompt = f"""
    You are an expert Indian Tax Accountant. 
    Parse the following raw financial data (extracted from OCR or text) into a normalized JSON format:
    {combined_input}

    Normalize it as per the following schema:
    - Date (YYYY-MM-DD)
    - Description
    - Amount (float)
    - Category (e.g., Revenue, Professional Fees, Rent, GST Credit)
    - Vendor ID (if any)
    - GSTIN (if any)
    """

    # Bedrock structured output
    structured_llm = llm.with_structured_output(NormalizedLedger)
    try:
        result = structured_llm.invoke(prompt)
        return {
            "normalized_ledger": result.model_dump()
        }
    except Exception as e:
        print(f"Error parsing raw inputs via Bedrock: {e}")
        return {"normalized_ledger": {"entries": []}}
