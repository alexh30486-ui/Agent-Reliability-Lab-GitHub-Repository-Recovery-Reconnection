from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


DATA = Path("data/processed/behavior_features_v3.csv")
TEST = Path("data/splits/test.csv")
MODEL = Path("data/processed/reliability_classifier_v7.joblib")
OUTPUT = Path("reports/v8_error_analysis.csv")


# ============================================================
# LOAD
# ============================================================

df = pd.read_csv(DATA)
test_ids = pd.read_csv(TEST)["trace_id"]

test = df[df["trace_id"].isin(test_ids)].copy()

model = joblib.load(MODEL)


# ============================================================
# BUILD MODEL INPUT
# ============================================================

behavior_features = [
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

test["combined_text"] = (
    "TASK " + test["task"].fillna("").astype(str)
    + " STEPS " + test["steps"].fillna("").astype(str)
    + " EVIDENCE " + test["text"].fillna("").astype(str)
)

X = test[["combined_text", "agent_type"] + behavior_features]

ml_predictions = model.predict(X)


# ============================================================
# V8 HYBRID RULES
# ============================================================

final_predictions = []

for i, (_, row) in enumerate(test.iterrows()):

    prediction = ml_predictions[i]

    # Explicit reasoning-error signal
    if row["has_reasoning_error_signal"] == 1:
        prediction = "bad_reasoning"

    # Explicit malformed JSON/XML
    elif (
        row["has_malformed_json"] == 1
        or row["has_malformed_xml"] == 1
    ):
        prediction = "malformed_output"

    # Explicit safety signal
    elif row["has_safety_signal"] == 1:
        prediction = "safety_violation"

    # Explicit missing requirement
    elif row["has_missing_requirement"] == 1:
        prediction = "incomplete_task"

    final_predictions.append(prediction)


test["ml_predicted"] = ml_predictions
test["predicted"] = final_predictions
test["actual"] = test["failure_type"]

# Whether the hybrid rule changed the ML prediction
test["rule_override"] = (
    test["ml_predicted"] != test["predicted"]
).astype(int)


# ============================================================
# RESULTS
# ============================================================

correct = (test["predicted"] == test["actual"]).sum()
errors = len(test) - correct

print("=" * 70)
print("V8 HYBRID ERROR ANALYSIS")
print("=" * 70)

print(f"Test examples: {len(test)}")
print(f"Correct: {correct}")
print(f"Errors: {errors}")

print("\nML ACCURACY:")
print(f"{accuracy_score(test['actual'], test['ml_predicted']):.4f}")

print("\nV8 FINAL ACCURACY:")
print(f"{accuracy_score(test['actual'], test['predicted']):.4f}")

print("\nCLASSIFICATION REPORT:")
print(
    classification_report(
        test["actual"],
        test["predicted"],
        zero_division=0,
    )
)


# ============================================================
# RULE OVERRIDES
# ============================================================

overrides = test[test["rule_override"] == 1]

print("\nRULE OVERRIDES:")
print(
    overrides[
        [
            "trace_id",
            "actual",
            "ml_predicted",
            "predicted",
            "has_reasoning_error_signal",
            "has_malformed_json",
            "has_malformed_xml",
            "has_safety_signal",
            "has_missing_requirement",
        ]
    ].to_string(index=False)
)


# ============================================================
# MISCLASSIFICATIONS
# ============================================================

errors_df = test[test["actual"] != test["predicted"]]

print("\nMISCLASSIFIED EXAMPLES:")
print("=" * 70)

for _, row in errors_df.iterrows():

    print(f"\nTRACE: {row['trace_id']}")
    print(f"ACTUAL: {row['actual']}")
    print(f"ML PREDICTION: {row['ml_predicted']}")
    print(f"FINAL PREDICTION: {row['predicted']}")
    print(f"TASK: {row['task']}")
    print(f"STEPS: {row['steps']}")
    print(f"REASONING SIGNAL: {row['has_reasoning_error_signal']}")
    print(f"FORMAT: {row['has_format_requirement']}")
    print(f"MALFORMED JSON: {row['has_malformed_json']}")
    print(f"MALFORMED XML: {row['has_malformed_xml']}")
    print(f"SAFETY: {row['has_safety_signal']}")
    print(f"MISSING REQUIREMENT: {row['has_missing_requirement']}")


# ============================================================
# SAVE
# ============================================================

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

test.to_csv(OUTPUT, index=False)

print(f"\nSaved: {OUTPUT}")
