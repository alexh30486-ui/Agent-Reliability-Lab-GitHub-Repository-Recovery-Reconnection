import json
from collections import Counter
from pathlib import Path

VALID_LABELS = {
    "none",
    "hallucination",
    "wrong_tool",
    "bad_reasoning",
    "incomplete_task",
    "malformed_output",
    "unnecessary_tool_call",
    "failure_to_recover",
    "safety_violation",
}

INPUT_FILE = Path("data/raw/agent_traces.jsonl")


def main():
    print("AGENT RELIABILITY DATA QUALITY CHECK")
    print("=" * 50)

    traces = []
    errors = []

    with INPUT_FILE.open() as file:
        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            try:
                trace = json.loads(line)
                traces.append(trace)
            except json.JSONDecodeError:
                errors.append(
                    f"Line {line_number}: invalid JSON"
                )

    print(f"\nTotal traces: {len(traces)}")

    # --------------------------------------------------
    # Duplicate trace IDs
    # --------------------------------------------------

    trace_ids = [t.get("trace_id") for t in traces]
    duplicate_ids = [
        trace_id
        for trace_id, count in Counter(trace_ids).items()
        if count > 1
    ]

    print(f"Duplicate trace IDs: {len(duplicate_ids)}")

    # --------------------------------------------------
    # Missing values
    # --------------------------------------------------

    required_fields = [
        "trace_id",
        "agent_type",
        "task",
        "steps",
        "tool_calls",
        "final_answer",
        "failure_type",
    ]

    missing_count = 0

    for trace in traces:
        for field in required_fields:
            if field not in trace or trace[field] in ("", None):
                missing_count += 1
                errors.append(
                    f"{trace.get('trace_id', 'UNKNOWN')}: "
                    f"missing {field}"
                )

    print(f"Missing required values: {missing_count}")

    # --------------------------------------------------
    # Invalid labels
    # --------------------------------------------------

    invalid_labels = []

    for trace in traces:
        label = trace.get("failure_type")

        if label not in VALID_LABELS:
            invalid_labels.append(
                (trace.get("trace_id"), label)
            )

    print(f"Invalid labels: {len(invalid_labels)}")

    # --------------------------------------------------
    # Tool call validation
    # --------------------------------------------------

    invalid_tool_calls = 0

    for trace in traces:
        tool_calls = trace.get("tool_calls")

        if not isinstance(tool_calls, int) or tool_calls < 0:
            invalid_tool_calls += 1

    print(f"Invalid tool-call counts: {invalid_tool_calls}")

    # --------------------------------------------------
    # Label distribution
    # --------------------------------------------------

    labels = Counter(
        trace.get("failure_type")
        for trace in traces
    )

    print("\nFailure distribution:")

    for label in sorted(VALID_LABELS):
        print(
            f"  {label:25} {labels.get(label, 0)}"
        )

    # --------------------------------------------------
    # Final status
    # --------------------------------------------------

    print("\n" + "=" * 50)

    if errors or invalid_labels or invalid_tool_calls or duplicate_ids:
        print("FAIL: Data quality issues detected.")

        for error in errors:
            print(f"  - {error}")

        for trace_id, label in invalid_labels:
            print(
                f"  - {trace_id}: invalid label '{label}'"
            )

    else:
        print("PASS: No structural data-quality errors detected.")


if __name__ == "__main__":
    main()
