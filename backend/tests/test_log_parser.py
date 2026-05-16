"""
Tests for log parser service
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path to import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.log_parser import parse_logs


def test_python_attribute_error():
    """Test parsing Python AttributeError traceback"""
    raw_log = """
Traceback (most recent call last):
  File "app/main.py", line 42, in process_data
    result = data.get_value()
  File "app/utils.py", line 15, in get_value
    return self.value.upper()
AttributeError: 'NoneType' object has no attribute 'upper'
"""
    
    result = parse_logs(raw_log)
    
    assert result["error_type"] == "AttributeError"
    assert result["files"][0] == "app/main.py"
    assert result["line_numbers"][0] == 42
    assert "'NoneType' object has no attribute 'upper'" in result["error_message"]
    assert result["severity"] == "ERROR"
    assert len(result["file_line_pairs"]) == 2
    assert result["file_line_pairs"][0] == ("app/main.py", 42)


def test_javascript_type_error():
    """Test parsing JavaScript TypeError stack trace"""
    raw_log = """
TypeError: Cannot read property 'name' of undefined
    at Object.getUserName (src/utils/user.js:23:15)
    at processUser (src/services/auth.js:45:20)
    at main (src/index.js:10:5)
"""
    
    result = parse_logs(raw_log)
    
    assert result["error_type"] == "TypeError"
    assert result["files"][0] == "src/utils/user.js"
    assert result["line_numbers"][0] == 23
    assert "Cannot read property 'name' of undefined" in result["error_message"]
    assert result["severity"] == "ERROR"
    assert len(result["file_line_pairs"]) == 3
    assert result["file_line_pairs"][0] == ("src/utils/user.js", 23)


def test_java_null_pointer_exception():
    """Test parsing Java NullPointerException stack trace"""
    raw_log = """
Exception in thread "main" java.lang.NullPointerException: Cannot invoke "String.length()" because "str" is null
    at com.example.app.StringUtils.processString(StringUtils.java:45)
    at com.example.app.Main.main(Main.java:12)
"""
    
    result = parse_logs(raw_log)
    
    assert result["error_type"] == "NullPointerException"
    assert result["files"][0] == "StringUtils.java"
    assert result["line_numbers"][0] == 45
    assert 'Cannot invoke "String.length()"' in result["error_message"]
    assert result["severity"] == "ERROR"
    assert len(result["file_line_pairs"]) == 2
    assert result["file_line_pairs"][0] == ("StringUtils.java", 45)


def test_malformed_empty_string():
    """Test parsing malformed or empty log string"""
    # Test empty string
    result_empty = parse_logs("")
    
    assert result_empty["error_type"] == "UnknownError"
    assert result_empty["error_message"] is None
    assert result_empty["files"] == []
    assert result_empty["line_numbers"] == []
    assert result_empty["severity"] == "ERROR"
    assert result_empty["file_line_pairs"] == []
    
    # Test malformed string with no recognizable patterns
    malformed_log = "Something went wrong but no stack trace here"
    result_malformed = parse_logs(malformed_log)
    
    assert result_malformed["error_type"] == "UnknownError"
    assert result_malformed["files"] == []
    assert result_malformed["line_numbers"] == []
    assert result_malformed["file_line_pairs"] == []


def test_severity_detection():
    """Test severity level detection"""
    # Test WARNING
    warning_log = "WARNING: Deprecated function called at app.py:10"
    result = parse_logs(warning_log)
    assert result["severity"] == "WARNING"
    
    # Test INFO
    info_log = "INFO: Application started successfully"
    result = parse_logs(info_log)
    assert result["severity"] == "INFO"
    
    # Test ERROR (default)
    error_log = "ERROR: Database connection failed"
    result = parse_logs(error_log)
    assert result["severity"] == "ERROR"


def test_multiple_files_deduplication():
    """Test that duplicate files are removed"""
    raw_log = """
Traceback (most recent call last):
  File "app/main.py", line 10, in func1
    func2()
  File "app/utils.py", line 20, in func2
    func3()
  File "app/main.py", line 30, in func3
    raise ValueError("test")
ValueError: test
"""
    
    result = parse_logs(raw_log)
    
    # Should have unique files only
    assert len(result["files"]) == 2
    assert "app/main.py" in result["files"]
    assert "app/utils.py" in result["files"]
    
    # But file_line_pairs should have all occurrences
    assert len(result["file_line_pairs"]) == 3

# Made with Bob
