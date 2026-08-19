from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import accuracy_score, classification_report


DATA = Path("data/processed/behavior_features_v3.csv")
TEST = Path("data/splits/test.csv")
MODEL = Path("data/processed/reliability_classifier_v3.joblib")
OUTPUT = Path("reports/v3_error_analysis.csv")


df = pd.read_csv(DATA)
test_ids = pd.read_csv(TEST)["trace_id"]

test = df[df["trace_id"].isin(test_ids)].copy()


def make_text(frame):
    return (
        frame["task"].astype(str)
        + " STEPS "
        + frame["steps"].astype(str)
        + " AGENT "
        + frame["agent_type"].astype(str)
        + " TEXT "
        + frame["text"].astype(str)
    )


behavior_features = [
    "tool_calls",
    "step_count",
    "has_evidence",
    "has_answer",
    "has_contradiction",
    "uses_expected_tool",
    "tool_step_count",
    "repeated_search",
    "ends_with_answer",
    "has_tool_call",
]

test["combined_text"] = make_text(test)

X_test = test[
    ["combined_text", "agent_type"] + behavior_features
]

y_test = test["failure_type"]

model = joblib.load(MODEL)

predicted = model.predict(X_test)

test["predicted"] = predicted

errors = test[test["failure_type"] != test["predicted"]].copy()

print("=" * 70)
print("V3 ERROR ANALYSIS")
print("=" * 70)

print(f"Test examples: {len(test)}")
print(f"Correct: {(test['failure_type'] == test['predicted']).sum()}")
print(f"Errors: {len(errors)}")

print("\nCONFUSION PAIRS")

pairs = (
    errors
    .groupby(["failure_type", "predicted"])
    .size()
    .sort_values(ascending=False)
)

for (actual, predicted_label), count in pairs.items():
    print(
        f"{actual:25} -> "
        f"{predicted_label:25} {count}"
    )

print("\nMISCLASSIFIED EXAMPLES")
print("=" * 70)

for _, row in errors.iterrows():
    print(f"\nTRACE: {row['trace_id']}")
    print(f"AGENT: {row['agent_type']}")
    print(f"TASK: {row['task']}")
    print(f"STEPS: {row['steps']}")
    print(f"EVIDENCE: {row['text']}")
    print(f"ACTUAL: {row['failure_type']}")
    print(f"PREDICTED: {row['predicted']}")
    print("-" * 70)


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
errors.to_csv(OUTPUT, index=False)

print(f"\nSaved: {OUTPUT}")
