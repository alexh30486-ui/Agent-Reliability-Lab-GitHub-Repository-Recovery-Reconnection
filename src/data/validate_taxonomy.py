import json
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


def validate_trace(trace):
    errors = []

    required_fields = {
        "trace_id",
        "agent_type",
        "task",
        "steps",
        "tool_calls",
        "final_answer",
        "failure_type",
    }

    missing = required_fields - trace.keys()

    if missing:
        errors.append(f"Missing fields: {sorted(missing)}")

    failure_type = trace.get("failure_type")

    if failure_type not in VALID_LABELS:
        errors.append(
            f"Invalid failure_type: {failure_type}"
        )

    if not isinstance(trace.get("steps"), list):
        errors.append("steps must be a list")

    if not isinstance(trace.get("tool_calls"), int):
        errors.append("tool_calls must be an integer")

    if not trace.get("final_answer"):
        errors.append("final_answer is empty")

    return errors


def main():
    print("Agent Reliability Taxonomy Validator")
    print("=" * 45)

    if not INPUT_FILE.exists():
        print(f"ERROR: {INPUT_FILE} does not exist.")
        return

    total = 0
    valid = 0
    invalid = 0

    with INPUT_FILE.open() as file:
        for line_number, line in enumerate(file, start=1):

            if not line.strip():
                continue

            total += 1

            try:
                trace = json.loads(line)
            except json.JSONDecodeError as error:
                print(f"Line {line_number}: INVALID JSON")
                print(f"  {error}")
                invalid += 1
                continue

            errors = validate_trace(trace)

            if errors:
                invalid += 1
                print(f"\nTrace {line_number}: INVALID")

                for error in errors:
                    print(f"  - {error}")

            else:
                valid += 1

    print("\n" + "=" * 45)
    print(f"Total traces:   {total}")
    print(f"Valid traces:   {valid}")
    print(f"Invalid traces: {invalid}")

    if invalid == 0:
        print("\nPASS: All traces conform to the taxonomy.")
    else:
        print("\nFAIL: Dataset contains invalid traces.")


if __name__ == "__main__":
    main()
