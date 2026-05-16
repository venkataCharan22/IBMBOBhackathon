"""
Code Retrieval Agent
Retrieves relevant code chunks from ChromaDB vector store
"""

import time
import chromadb
from app.config import settings


def code_retrieval_node(state: dict) -> dict:
    """
    Retrieve relevant code chunks from vector store based on error context.
    
    Args:
        state: Must contain "parsed_logs" with error information
        
    Returns:
        Updated state with:
        - code_chunks: List of retrieved code chunks
        - progress: 50
        - status: "retrieval_complete"
        - agent_events: List with event entry
    """
    parsed_logs = state.get("parsed_logs", {})
    error_type = parsed_logs.get("error_type", "")
    error_message = parsed_logs.get("error_message", "")
    files = parsed_logs.get("files", [])
    
    # Lazy-load ChromaDB client
    try:
        chromadb_path = settings.chromadb_path or "./chromadb"
        client = chromadb.PersistentClient(path=chromadb_path)
        collection = client.get_or_create_collection("codebase")
        
        # Check if collection has any data
        if collection.count() == 0:
            # No indexed code - store empty list and continue
            state["code_chunks"] = []
            chunk_count = 0
        else:
            # Build query from error context
            query_parts = [error_type, error_message] + files[:3]
            query = " ".join(filter(None, query_parts))
            
            # Query the collection
            results = collection.query(
                query_texts=[query],
                n_results=5
            )
            
            # Format results
            code_chunks = []
            if results and results.get("documents") and results["documents"][0]:
                for i, doc in enumerate(results["documents"][0]):
                    metadata = results.get("metadatas", [[]])[0]
                    distances = results.get("distances", [[]])[0]
                    
                    chunk = {
                        "snippet": doc,
                        "path": metadata[i].get("path", "unknown") if i < len(metadata) else "unknown",
                        "score": 1.0 - (distances[i] if i < len(distances) else 0.5)
                    }
                    code_chunks.append(chunk)
            
            state["code_chunks"] = code_chunks
            chunk_count = len(code_chunks)
    
    except Exception as e:
        # If ChromaDB fails, continue with empty chunks
        # This allows the pipeline to continue even without vector store
        state["code_chunks"] = []
        chunk_count = 0
    
    # Update state
    state["progress"] = 50
    state["status"] = "retrieval_complete"
    
    # Initialize agent_events if not present
    if "agent_events" not in state:
        state["agent_events"] = []
    
    # Add event
    state["agent_events"].append({
        "agent": "code_retrieval",
        "ts": int(time.time() * 1000),
        "summary": f"Retrieved {chunk_count} code chunks"
    })
    
    return state

# Made with Bob
