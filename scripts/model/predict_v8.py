from pathlib import Path

import joblib
import pandas as pd


MODEL = Path(
    "data/processed/reliability_classifier_v7.joblib"
)

DATA = Path(
    "data/processed/behavior_features_v3.csv"
)


def apply_reliability_rules(row, ml_prediction):
    """
    Hybrid reliability classifier.

    High-confidence behavioral signals override the
    statistical classifier when the evidence is explicit.
    """

    # Safety is highest priority.
    if row["has_safety_signal"] == 1:
        return "safety_violation"

    # Output-format failures are explicit.
    if (
        row["has_malformed_json"] == 1
        or row["has_malformed_xml"] == 1
    ):
        return "malformed_output"

    # Explicit reasoning-error evidence.
    if row["has_reasoning_error_signal"] == 1:
        return "bad_reasoning"

    # Explicit missing requirement.
    if row["has_missing_requirement"] == 1:
        return "incomplete_task"

    return ml_prediction


df = pd.read_csv(DATA)
model = joblib.load(MODEL)


def build_input(data):
    data = data.copy()

    data["combined_text"] = (
        "TASK "
        + data["task"].fillna("").astype(str)
        + " STEPS "
        + data["steps"].fillna("").astype(str)
        + " EVIDENCE "
        + data["text"].fillna("").astype(str)
        + " REASONING_SIGNAL_"
        + data["has_reasoning_error_signal"].astype(str)
        + " FORMAT_SIGNAL_"
        + data["has_format_requirement"].astype(str)
        + " MALFORMED_JSON_"
        + data["has_malformed_json"].astype(str)
        + " MALFORMED_XML_"
        + data["has_malformed_xml"].astype(str)
        + " SAFETY_SIGNAL_"
        + data["has_safety_signal"].astype(str)
        + " CONTRADICTION_"
        + data["has_contradiction"].astype(str)
        + " MISSING_REQUIREMENT_"
        + data["has_missing_requirement"].astype(str)
        + " ANSWER_SUPPORTED_"
        + data["answer_supported"].astype(str)
        + " TASK_COMPLETED_"
        + data["task_completed"].astype(str)
    )

    features = [
        "tool_calls",
        "step_count",
        "has_evidence",
        "has_answer",
        "has_contradiction",
        "has_reasoning_error_signal",
        "answer_supported",
        "uses_expected_tool",
        "tool_step_count",
        "repeated_search",
        "ends_with_answer",
        "has_tool_call",
        "has_missing_requirement",
        "task_completed",
        "has_format_requirement",
        "has_malformed_json",
        "has_malformed_xml",
        "has_safety_signal",
    ]

    return data[
        ["combined_text", "agent_type"] + features
    ]


# ============================================================
# TEST TRACE 055
# ============================================================

row = df[df["trace_id"] == "trace_055"].copy()

X = build_input(row)

ml_prediction = model.predict(X)[0]

final_prediction = apply_reliability_rules(
    row.iloc[0],
    ml_prediction,
)

print("=" * 70)
print("V8 HYBRID RELIABILITY CHECK")
print("=" * 70)

print("TRACE:", row["trace_id"].iloc[0])
print("ACTUAL:", row["failure_type"].iloc[0])
print("ML PREDICTION:", ml_prediction)
print("FINAL PREDICTION:", final_prediction)
print(
    "REASONING SIGNAL:",
    row["has_reasoning_error_signal"].iloc[0],
)

print("\nRULE STATUS:")

if row["has_reasoning_error_signal"].iloc[0] == 1:
    print("  BAD_REASONING RULE: TRIGGERED")
else:
    print("  BAD_REASONING RULE: not triggered")
