import os
from typing import Any, Dict, List
from langchain_huggingface import HuggingFaceEmbeddings
from state import TaxAgentState
from vector_db import vector_db

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def rules_retrieval_node(state: TaxAgentState) -> Dict[str, Any]:
    """
    Queries Qdrant to retrieve exact statutory rules (tax slabs, sections) based on the financial framework.
    """
    framework = state.get("framework", "ITR-4")
    
    try:
        query_vector = embedding_model.embed_query(framework)
        search_results = vector_db.qdrant_client.search(
            collection_name="statutory_rules",
            query_vector=query_vector,
            limit=5
        )
        # Extract payload text from search results, assuming it's stored under a 'content' key
        rules = [res.payload.get("content", str(res.payload)) for res in search_results] if search_results else []
        
        # Fallback if no rules found
        if not rules:
            rules = ["No specific rule found in DB for this framework."]
            
    except Exception as e:
        print(f"Error retrieving rules from Qdrant: {e}")
        rules = ["Database error, fallback rules apply."]
    
    return {"applicable_rules": rules}
