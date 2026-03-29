from typing import Dict, Any
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver
from state import TaxAgentState
from nodes.ml_ingestion import ml_ingestion_node
from nodes.normalizer import normalizer_node
from nodes.web_intelligence import web_intelligence_node
from nodes.rag import rules_retrieval_node
from nodes.computation import computation_node
from nodes.analyst import financial_analyst_node
from nodes.generator import artifact_generator_node

def create_tax_graph():
    """
    Constructs the Tax Agent LangGraph with deterministic nodes 
    and HITL interrupt.
    """
    workflow = StateGraph(TaxAgentState)

    # 1. Add Nodes
    workflow.add_node("ML_Ingestion", ml_ingestion_node)
    workflow.add_node("Normalizer", normalizer_node)
    workflow.add_node("Web_Intelligence", web_intelligence_node)
    workflow.add_node("Rules_Retrieval", rules_retrieval_node)
    workflow.add_node("Computation", computation_node)
    workflow.add_node("Financial_Analyst", financial_analyst_node)
    workflow.add_node("Artifact_Generator", artifact_generator_node)

    # 2. Define Edges (Deterministic path)
    workflow.set_entry_point("ML_Ingestion")
    workflow.add_edge("ML_Ingestion", "Normalizer")
    workflow.add_edge("Normalizer", "Web_Intelligence")
    workflow.add_edge("Web_Intelligence", "Rules_Retrieval")
    workflow.add_edge("Rules_Retrieval", "Computation")
    workflow.add_edge("Computation", "Financial_Analyst")
    
    # 3. HITL Interrupt Point (Manual Approval)
    # The workflow automatically pauses before the artifact generator
    # and waits for human_approval_status = "approved"
    
    # We use a conditional edge to implement approval logic or LangGraph's native interrupt()
    def check_approval(state: TaxAgentState):
        if state.get("human_approval_status") == "approved":
            return "Artifact_Generator"
        return "Financial_Analyst" # Retry/Backtrack if not approved

    workflow.add_conditional_edges(
        "Financial_Analyst", 
        check_approval, 
        {
            "Artifact_Generator": "Artifact_Generator",
            "Financial_Analyst": END # Stops if rejected/pending
        }
    )
    workflow.add_edge("Artifact_Generator", END)

    return workflow.compile()

tax_app = create_tax_graph()
