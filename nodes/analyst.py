import os
from typing import Any, Dict, List
from langchain_aws import ChatBedrock
from state import TaxAgentState
from bedrock_client import get_bedrock_client

llm = ChatBedrock(
    model_id=os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-5-sonnet-20240620-v1:0"),
    region_name=os.getenv("AWS_REGION", "us-east-1"),
    client=get_bedrock_client()
)

def financial_analyst_node(state: TaxAgentState) -> Dict[str, Any]:
    """
    Intelligent Data Analysis: Performs trend analysis, liquidity ratios, 
    and tax risk assessment using LLM-based reasoning grounded in the computation results.
    """
    results = state.get("computation_results", {})
    if not results:
        return {"analysis_report": "No computation data to analyze."}

    # High-level prompt for LLM based analysis
    prompt = f"""
    Analyze the following financial results:
    {results}

    Provide insights on:
    - Net Margin
    - Presumptive Income (44AD) vs. Actual Taxable Income
    - Tax Risks (e.g., high-risk categories)
    - Recommendations for GST ITC optimization
    """
    
    try:
        response = llm.invoke(prompt)
        analysis = response.content
    except Exception as e:
        print(f"Error during financial analysis: {e}")
        analysis = f"Analysis failed dynamically. Raw results: {results}"
        
    return {"analysis_report": analysis}
