from src.data.validate_taxonomy import validate_trace


def valid_trace():
    return {
        "trace_id": "test_001",
        "agent_type": "tool",
        "task": "Calculate 125 multiplied by 8",
        "steps": ["calculator", "interpret", "answer"],
        "tool_calls": 1,
        "final_answer": "1000",
        "failure_type": "none",
    }


def test_valid_trace():
    errors = validate_trace(valid_trace())
    assert errors == []


def test_invalid_failure_label():
    trace = valid_trace()
    trace["failure_type"] = "made_up_failure"

    errors = validate_trace(trace)

    assert any(
        "Invalid failure_type" in error
        for error in errors
    )


def test_missing_required_field():
    trace = valid_trace()
    del trace["final_answer"]

    errors = validate_trace(trace)

    assert any(
        "Missing fields" in error
        for error in errors
    )
