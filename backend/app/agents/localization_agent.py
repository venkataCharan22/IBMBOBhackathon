"""
Error Localization Agent
Identifies affected files and determines if they're in the project
"""

import os
import time
from pathlib import Path


def error_localization_node(state: dict) -> dict:
    """
    Localize errors to specific files and determine if they're in the project.
    
    Args:
        state: Must contain "parsed_logs" with file information
        
    Returns:
        Updated state with:
        - affected_files: List of file info dicts
        - progress: 30
        - status: "localization_complete"
        - agent_events: List with event entry
    """
    parsed_logs = state.get("parsed_logs", {})
    file_line_pairs = parsed_logs.get("file_line_pairs", [])
    project_path = state.get("project_path", ".")
    
    affected_files = []
    in_project_count = 0
    
    for file_path, line_number in file_line_pairs:
        # Check if file exists on disk
        full_path = os.path.join(project_path, file_path)
        exists = os.path.isfile(full_path)
        
        # Determine if file is in project (not in external dependencies)
        in_project = not any([
            "site-packages" in file_path,
            "node_modules" in file_path,
            file_path.startswith("/usr/lib/python"),
            file_path.startswith("/Library/Frameworks/Python"),
            file_path.startswith("C:\\Python"),
        ])
        
        if in_project:
            in_project_count += 1
        
        affected_files.append({
            "file_path": file_path,
            "line_number": line_number,
            "exists": exists,
            "in_project": in_project
        })
    
    # Update state
    state["affected_files"] = affected_files
    state["progress"] = 30
    state["status"] = "localization_complete"
    
    # Initialize agent_events if not present
    if "agent_events" not in state:
        state["agent_events"] = []
    
    # Add event
    total_files = len(affected_files)
    state["agent_events"].append({
        "agent": "error_localization",
        "ts": int(time.time() * 1000),
        "summary": f"Localized {total_files} files ({in_project_count} in-project)"
    })
    
    return state

# Made with Bob
