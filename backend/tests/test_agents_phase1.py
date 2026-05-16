"""
Tests for Phase 1 Agents (deterministic, no LLM)
"""

import pytest
import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.agents import log_analysis_node, error_localization_node, code_retrieval_node


def test_log_analysis_node():
    """Test log analysis agent with Python AttributeError"""
    # Sample Python AttributeError trace
    raw_log = """
Traceback (most recent call last):
  File "app/main.py", line 42, in process_data
    result = data.get_value()
AttributeError: 'NoneType' object has no attribute 'get_value'
"""
    
    # Initial state
    state = {
        "logs": raw_log
    }
    
    # Run agent
    result = log_analysis_node(state)
    
    # Assertions
    assert "parsed_logs" in result
    assert result["parsed_logs"]["error_type"] == "AttributeError"
    assert result["progress"] == 15
    assert result["status"] == "log_analysis_complete"
    assert "agent_events" in result
    assert len(result["agent_events"]) == 1
    assert result["agent_events"][0]["agent"] == "log_analysis"
    assert "AttributeError" in result["agent_events"][0]["summary"]
    assert "ts" in result["agent_events"][0]


def test_error_localization_node():
    """Test error localization with real and fake files"""
    # Use the actual log_parser.py file path (we know it exists)
    real_file = "app/services/log_parser.py"
    fake_file = "app/nonexistent/fake.py"
    external_file = "/usr/lib/python3.11/site-packages/requests/api.py"
    
    # State with parsed logs
    state = {
        "parsed_logs": {
            "file_line_pairs": [
                (real_file, 10),
                (fake_file, 20),
                (external_file, 30)
            ]
        },
        "project_path": "."
    }
    
    # Run agent
    result = error_localization_node(state)
    
    # Assertions
    assert "affected_files" in result
    assert len(result["affected_files"]) == 3
    
    # Check real file
    real_file_info = result["affected_files"][0]
    assert real_file_info["file_path"] == real_file
    assert real_file_info["line_number"] == 10
    assert real_file_info["in_project"] is True
    
    # Check fake file
    fake_file_info = result["affected_files"][1]
    assert fake_file_info["file_path"] == fake_file
    assert fake_file_info["line_number"] == 20
    assert fake_file_info["in_project"] is True
    
    # Check external file (site-packages)
    external_file_info = result["affected_files"][2]
    assert external_file_info["file_path"] == external_file
    assert external_file_info["line_number"] == 30
    assert external_file_info["in_project"] is False
    
    # Check progress and status
    assert result["progress"] == 30
    assert result["status"] == "localization_complete"
    assert "agent_events" in result
    assert len(result["agent_events"]) == 1
    assert result["agent_events"][0]["agent"] == "error_localization"
    assert "2 in-project" in result["agent_events"][0]["summary"]


def test_code_retrieval_node_empty_chromadb():
    """Test code retrieval with empty ChromaDB (no exceptions)"""
    # State with parsed logs
    state = {
        "parsed_logs": {
            "error_type": "AttributeError",
            "error_message": "test error",
            "files": ["app/main.py"]
        }
    }
    
    # Run agent - should not raise exception even if ChromaDB is empty
    result = code_retrieval_node(state)
    
    # Assertions
    assert "code_chunks" in result
    assert result["code_chunks"] == []  # Empty because no indexed code
    assert result["progress"] == 50
    assert result["status"] == "retrieval_complete"
    assert "agent_events" in result
    assert len(result["agent_events"]) == 1
    assert result["agent_events"][0]["agent"] == "code_retrieval"
    assert "Retrieved 0 code chunks" in result["agent_events"][0]["summary"]


def test_agent_events_accumulation():
    """Test that agent events accumulate across multiple agents"""
    raw_log = """
Traceback (most recent call last):
  File "app/test.py", line 10
    result = None.value
AttributeError: 'NoneType' object has no attribute 'value'
"""
    
    # Run through multiple agents
    state = {"logs": raw_log}
    
    # Agent 1
    state = log_analysis_node(state)
    assert len(state["agent_events"]) == 1
    
    # Agent 2
    state = error_localization_node(state)
    assert len(state["agent_events"]) == 2
    
    # Agent 3
    state = code_retrieval_node(state)
    assert len(state["agent_events"]) == 3
    
    # Verify all agents are recorded
    agent_names = [event["agent"] for event in state["agent_events"]]
    assert "log_analysis" in agent_names
    assert "error_localization" in agent_names
    assert "code_retrieval" in agent_names
    
    # Verify progress increases
    assert state["progress"] == 50


def test_state_preservation():
    """Test that agents preserve existing state keys"""
    initial_state = {
        "logs": "Error: test",
        "custom_key": "custom_value",
        "project_id": 123
    }
    
    result = log_analysis_node(initial_state)
    
    # Original keys should be preserved
    assert result["custom_key"] == "custom_value"
    assert result["project_id"] == 123
    
    # New keys should be added
    assert "parsed_logs" in result
    assert "progress" in result
    assert "status" in result

# Made with Bob
