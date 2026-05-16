"""
Log Parser Service
Extracts structured information from raw error logs and stack traces
Supports Python, JavaScript, and Java error formats
"""

import re
from typing import Dict, List, Tuple, Optional


def parse_logs(raw_text: str) -> Dict:
    """
    Parse raw error logs and extract structured information.
    
    Supports common formats:
    - Python: File "path/file.py", line N
    - JavaScript: at path/file.js:N:M
    - Java: at package.Class.method(File.java:N)
    
    Args:
        raw_text: Raw error log or stack trace text
        
    Returns:
        Dictionary containing:
        - error_type: Type of error (e.g., "AttributeError")
        - error_message: Error message
        - files: List of file paths
        - line_numbers: List of line numbers
        - stack_trace: Cleaned stack trace
        - severity: "ERROR", "WARNING", or "INFO"
        - file_line_pairs: List of (file, line) tuples
    """
    
    result = {
        "error_type": None,
        "error_message": None,
        "files": [],
        "line_numbers": [],
        "stack_trace": raw_text.strip(),
        "severity": "ERROR",
        "file_line_pairs": []
    }
    
    # Detect severity from log level indicators
    severity_patterns = [
        (r'\b(CRITICAL|FATAL)\b', "ERROR"),
        (r'\b(ERROR|Exception|Error)\b', "ERROR"),
        (r'\b(WARNING|WARN)\b', "WARNING"),
        (r'\b(INFO|DEBUG)\b', "INFO"),
    ]
    
    for pattern, severity in severity_patterns:
        if re.search(pattern, raw_text, re.IGNORECASE):
            result["severity"] = severity
            break
    
    # Extract Python tracebacks
    # Pattern: File "path/to/file.py", line 123
    python_pattern = r'File\s+"([^"]+)",\s+line\s+(\d+)'
    python_matches = re.findall(python_pattern, raw_text)
    
    for file_path, line_num in python_matches:
        result["files"].append(file_path)
        result["line_numbers"].append(int(line_num))
        result["file_line_pairs"].append((file_path, int(line_num)))
    
    # Extract Java stack traces (check before JS to avoid conflicts)
    # Pattern: at package.Class.method(File.java:123)
    java_pattern = r'at\s+[\w.$]+\(([^:)]+):(\d+)\)'
    java_matches = re.findall(java_pattern, raw_text)
    
    for file_path, line_num in java_matches:
        # Extract just the filename from the full path if present
        java_file = file_path.split('/')[-1] if '/' in file_path else file_path
        if java_file not in result["files"]:
            result["files"].append(java_file)
            result["line_numbers"].append(int(line_num))
            result["file_line_pairs"].append((java_file, int(line_num)))
    
    # Extract JavaScript stack traces
    # Pattern: at path/to/file.js:123:45 or at Object.method (file.js:123:45)
    # Only match if NOT in Java format (which has parentheses with method call before file)
    js_pattern = r'at\s+(?:[\w.<>]+\s+)?\(?([^\s:)]+):(\d+)(?::(\d+))?\)?'
    js_matches = re.findall(js_pattern, raw_text)
    
    for match in js_matches:
        file_path = match[0]
        line_num = int(match[1])
        
        # Skip if it looks like a Java method call (contains dots and capital letters)
        # or if already added from Python or Java patterns
        if '.' in file_path and any(c.isupper() for c in file_path.split('.')[-2] if len(file_path.split('.')) > 1):
            continue
            
        if file_path not in result["files"]:
            result["files"].append(file_path)
            result["line_numbers"].append(line_num)
            result["file_line_pairs"].append((file_path, line_num))
    
    # Extract error type and message
    # Python: ErrorType: message
    python_error_pattern = r'(\w+(?:Error|Exception|Warning)):\s*(.+?)(?:\n|$)'
    python_error_match = re.search(python_error_pattern, raw_text)
    
    if python_error_match:
        result["error_type"] = python_error_match.group(1)
        result["error_message"] = python_error_match.group(2).strip()
    
    # JavaScript: Error: message or TypeError: message
    js_error_pattern = r'(\w+Error):\s*(.+?)(?:\n|$)'
    if not result["error_type"]:
        js_error_match = re.search(js_error_pattern, raw_text)
        if js_error_match:
            result["error_type"] = js_error_match.group(1)
            result["error_message"] = js_error_match.group(2).strip()
    
    # Java: Exception in thread "main" java.lang.ExceptionType: message
    java_error_pattern = r'(?:Exception in thread "[^"]+"\s+)?([\w.]+(?:Exception|Error)):\s*(.+?)(?:\n|$)'
    if not result["error_type"]:
        java_error_match = re.search(java_error_pattern, raw_text)
        if java_error_match:
            result["error_type"] = java_error_match.group(1).split('.')[-1]  # Get last part
            result["error_message"] = java_error_match.group(2).strip()
    
    # Generic error message extraction if specific patterns didn't match
    if not result["error_message"]:
        # Try to find any line that looks like an error message
        error_line_pattern = r'(?:error|exception|failed):\s*(.+?)(?:\n|$)'
        error_line_match = re.search(error_line_pattern, raw_text, re.IGNORECASE)
        if error_line_match:
            result["error_message"] = error_line_match.group(1).strip()
    
    # If no error type found, try to infer from keywords
    if not result["error_type"]:
        if re.search(r'\bNullPointerException\b', raw_text):
            result["error_type"] = "NullPointerException"
        elif re.search(r'\bTypeError\b', raw_text):
            result["error_type"] = "TypeError"
        elif re.search(r'\bSyntaxError\b', raw_text):
            result["error_type"] = "SyntaxError"
        elif re.search(r'\bRuntimeError\b', raw_text):
            result["error_type"] = "RuntimeError"
        elif re.search(r'\bAttributeError\b', raw_text):
            result["error_type"] = "AttributeError"
        elif re.search(r'\bValueError\b', raw_text):
            result["error_type"] = "ValueError"
        elif re.search(r'\bKeyError\b', raw_text):
            result["error_type"] = "KeyError"
        elif re.search(r'\bIndexError\b', raw_text):
            result["error_type"] = "IndexError"
        else:
            result["error_type"] = "UnknownError"
    
    # Remove duplicates while preserving order
    seen_files = set()
    unique_files = []
    for f in result["files"]:
        if f not in seen_files:
            seen_files.add(f)
            unique_files.append(f)
    result["files"] = unique_files
    
    # Remove duplicate line numbers
    result["line_numbers"] = list(dict.fromkeys(result["line_numbers"]))
    
    # Remove duplicate file-line pairs
    seen_pairs = set()
    unique_pairs = []
    for pair in result["file_line_pairs"]:
        if pair not in seen_pairs:
            seen_pairs.add(pair)
            unique_pairs.append(pair)
    result["file_line_pairs"] = unique_pairs
    
    return result


def extract_code_context(raw_text: str, context_lines: int = 3) -> Dict[str, List[str]]:
    """
    Extract code snippets from stack trace with context.
    
    Args:
        raw_text: Raw error log text
        context_lines: Number of context lines to extract around error
        
    Returns:
        Dictionary mapping file paths to code snippets
    """
    code_context = {}
    
    # Look for code snippets in Python tracebacks (lines starting with spaces)
    lines = raw_text.split('\n')
    current_file = None
    
    for i, line in enumerate(lines):
        # Check if this is a file reference
        file_match = re.match(r'\s*File\s+"([^"]+)",\s+line\s+(\d+)', line)
        if file_match:
            current_file = file_match.group(1)
            code_context[current_file] = []
            
            # Get the next few lines as code context
            for j in range(i + 1, min(i + context_lines + 1, len(lines))):
                if lines[j].strip() and not lines[j].startswith('  File'):
                    code_context[current_file].append(lines[j])
    
    return code_context

# Made with Bob
