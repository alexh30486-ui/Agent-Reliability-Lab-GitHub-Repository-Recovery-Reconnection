from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score

DATA = Path("data/processed/behavior_features_v3.csv")
TEST = Path("data/splits/test.csv")
MODEL = Path("data/processed/reliability_classifier_v4.joblib")
OUTPUT = Path("reports/v4_error_analysis.csv")

df = pd.read_csv(DATA)
test_ids = pd.read_csv(TEST)["trace_id"]

test = df[df["trace_id"].isin(test_ids)].copy()

# Recreate the text feature expected by V4
test["combined_text"] = (
    "AGENT " + test["agent_type"].fillna("").astype(str)
    + " TASK " + test["task"].fillna("").astype(str)
    + " STEPS " + test["steps"].fillna("").astype(str)
    + " TEXT " + test["text"].fillna("").astype(str)
)

model = joblib.load(MODEL)

predicted = model.predict(test)

test["actual"] = test["failure_type"]
test["predicted"] = predicted

errors = test[test["actual"] != test["predicted"]].copy()

print("=" * 70)
print("V4 ERROR ANALYSIS")
print("=" * 70)

print(f"Test examples: {len(test)}")
print(f"Correct: {(test['actual'] == test['predicted']).sum()}")
print(f"Errors: {len(errors)}")

print("\nACCURACY:")
print(f"{accuracy_score(test['actual'], test['predicted']):.4f}")

print("\nCONFUSION PAIRS:")

if len(errors):
    pairs = (
        errors
        .groupby(["actual", "predicted"])
        .size()
        .sort_values(ascending=False)
    )

    for (actual, predicted), count in pairs.items():
        print(f"{actual:25} -> {predicted:25} {count}")

print("\nFORMAT ERRORS:")
print(
    test[test["actual"] == "malformed_output"]
    [[
        "trace_id",
        "predicted",
        "has_format_requirement",
        "has_malformed_json",
        "has_malformed_xml",
    ]]
    .to_string(index=False)
)

print("\nSAFETY ERRORS:")
print(
    test[test["actual"] == "safety_violation"]
    [[
        "trace_id",
        "predicted",
        "has_safety_signal",
    ]]
    .to_string(index=False)
)

print("\nINCOMPLETE TASK ERRORS:")
print(
    test[test["actual"] == "incomplete_task"]
    [[
        "trace_id",
        "predicted",
        "has_missing_requirement",
        "task_completed",
    ]]
    .to_string(index=False)
)

print("\nBAD REASONING ERRORS:")
print(
    test[test["actual"] == "bad_reasoning"]
    [[
        "trace_id",
        "predicted",
        "has_contradiction",
        "answer_supported",
    ]]
    .to_string(index=False)
)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
errors.to_csv(OUTPUT, index=False)

print(f"\nSaved: {OUTPUT}")
