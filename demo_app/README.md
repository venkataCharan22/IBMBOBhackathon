# Demo App - Bug2PR Testing Application

## 📋 Overview

This directory will contain a Flask application with **5 intentionally staged bugs** designed to test and demonstrate the Bug2PR autonomous bug-fixing pipeline.

## 🚧 Status: Placeholder (Phase 9)

This demo app will be implemented in **Phase 9** once the core Bug2PR pipeline is fully built and operational.

## 🎯 Purpose

The demo app serves as a controlled testing environment to validate that Bug2PR can:
1. Detect and analyze various types of bugs
2. Generate appropriate fixes
3. Create regression tests
4. Perform security audits
5. Submit working pull requests

## 🐛 Planned Staged Bugs

The demo app will include 5 different bug categories:

### 1. **Syntax Error**
- **Type**: Python syntax error
- **Example**: Missing colon, incorrect indentation
- **Severity**: High
- **Expected Fix**: Syntax correction

### 2. **Logic Error**
- **Type**: Incorrect business logic
- **Example**: Wrong calculation, off-by-one error
- **Severity**: Medium
- **Expected Fix**: Logic correction with test case

### 3. **Runtime Error**
- **Type**: Exception during execution
- **Example**: Division by zero, null pointer
- **Severity**: High
- **Expected Fix**: Error handling implementation

### 4. **Security Vulnerability**
- **Type**: Security flaw
- **Example**: SQL injection, XSS vulnerability
- **Severity**: Critical
- **Expected Fix**: Input sanitization, parameterized queries

### 5. **Performance Issue**
- **Type**: Inefficient code
- **Example**: N+1 query problem, unnecessary loops
- **Severity**: Low-Medium
- **Expected Fix**: Code optimization

## 🏗️ Planned Structure

```
demo_app/
├── app.py              # Main Flask application
├── requirements.txt    # Flask and dependencies
├── routes/            # API endpoints with bugs
├── models/            # Database models
├── utils/             # Helper functions
├── tests/             # Initial test suite (incomplete)
└── bugs/              # Documentation of each staged bug
    ├── bug1_syntax.md
    ├── bug2_logic.md
    ├── bug3_runtime.md
    ├── bug4_security.md
    └── bug5_performance.md
```

## 🔄 Integration with Bug2PR

Once implemented, the workflow will be:

1. **Trigger Bug**: Run demo app to generate error logs
2. **Feed to Bug2PR**: Upload error logs to Bug2PR pipeline
3. **Agent Processing**: Watch 8 AI agents analyze and fix
4. **PR Generation**: Receive automated pull request with:
   - Bug fix implementation
   - Regression test
   - Security audit report
   - Documentation
5. **Validation**: Verify the fix resolves the issue

## 📅 Implementation Timeline

- **Phase 1-8**: Build Bug2PR core pipeline
- **Phase 9**: Implement demo app with staged bugs
- **Phase 10**: End-to-end testing and validation

## 🧪 Testing Scenarios

Each bug will test specific Bug2PR capabilities:

| Bug Type | Tests Agent | Expected Outcome |
|----------|-------------|------------------|
| Syntax | Error Analyzer, Fix Generator | Syntax correction |
| Logic | Root Cause Analyzer, Test Generator | Logic fix + test |
| Runtime | Error Analyzer, Fix Generator | Exception handling |
| Security | Security Auditor, Fix Generator | Vulnerability patch |
| Performance | Code Locator, Fix Generator | Optimization |

## 📝 Notes

- All bugs will be **intentionally introduced** and documented
- Each bug will have a **known correct solution** for validation
- Error logs will be **pre-generated** for consistent testing
- The app will be **simple enough** to allow clear bug identification
- **Multiple difficulty levels** to test agent capabilities

## 🚀 Future Enhancements

- Add more complex bug scenarios
- Include multi-file bugs
- Test cross-language bug fixing
- Add integration test scenarios
- Create bug difficulty ratings

---

**Status**: 🚧 Placeholder - To be implemented in Phase 9

**Dependencies**: Bug2PR core pipeline (Phases 1-8)

**Priority**: Low (after core pipeline is operational)