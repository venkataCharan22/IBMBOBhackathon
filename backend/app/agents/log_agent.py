"""
Log Analysis Agent
Parses raw error logs and extracts structured information
"""

import time
from app.services.log_parser import parse_logs


def log_analysis_node(state: dict) -> dict:
    """
    Parse raw error logs and extract structured information.
    
    Args:
        state: Must contain "logs" key with raw error log text
        
    Returns:
        Updated state with:
        - parsed_logs: Structured log information
        - progress: 15
        - status: "log_analysis_complete"
        - agent_events: List with event entry
    """
    # Parse the logs
    parsed_logs = parse_logs(state["logs"])
    
    # Update state
    state["parsed_logs"] = parsed_logs
    state["progress"] = 15
    state["status"] = "log_analysis_complete"
    
    # Initialize agent_events if not present
    if "agent_events" not in state:
        state["agent_events"] = []
    
    # Add event
    files = parsed_logs.get("files", [])
    error_type = parsed_logs.get("error_type", "Unknown")
    
    state["agent_events"].append({
        "agent": "log_analysis",
        "ts": int(time.time() * 1000),
        "summary": f"Parsed {error_type} with {len(files)} frame(s)"
    })
    
    return state

# Made with Bob
