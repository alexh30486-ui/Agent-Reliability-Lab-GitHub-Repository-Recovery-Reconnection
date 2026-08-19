import pandas as pd
import joblib

from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix

DATA = Path("data/processed/agent_features.csv")
MODEL = Path("data/processed/reliability_classifier_v2.joblib")

df = pd.read_csv(DATA)

def make_text(df):
    return (
        "AGENT_TYPE " + df["agent_type"].astype(str)
        + " TASK " + df["task"].astype(str)
        + " STEPS " + df["steps"].astype(str)
        + " TOOL_CALLS " + df["tool_calls"].astype(str)
        + " STEP_COUNT " + df["step_count"].astype(str)
        + " HAS_EVIDENCE " + df["has_evidence"].astype(str)
        + " HAS_ANSWER " + df["has_answer"].astype(str)
        + " FIRST_STEP " + df["first_step"].astype(str)
        + " LAST_STEP " + df["last_step"].astype(str)
        + " TEXT " + df["text"].astype(str)
    )

train, test = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["failure_type"]
)

model = joblib.load(MODEL)

predicted = model.predict(make_text(test))

results = test.copy()
results["predicted"] = predicted
results["correct"] = (
    results["failure_type"] == results["predicted"]
)

errors = results[~results["correct"]]

print("=" * 70)
print("V2 ERROR ANALYSIS")
print("=" * 70)

print(f"Test examples: {len(results)}")
print(f"Correct: {results['correct'].sum()}")
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
        f"{predicted_label:25} "
        f"{count}"
    )

print("\nMISCLASSIFIED EXAMPLES")
print("=" * 70)

for _, row in errors.iterrows():

    print("\nTRACE:", row["trace_id"])
    print("AGENT:", row["agent_type"])
    print("TASK:", row["task"])
    print("STEPS:", row["steps"])
    print("EVIDENCE:", row["text"])
    print("ACTUAL:", row["failure_type"])
    print("PREDICTED:", row["predicted"])
    print("-" * 70)

OUTPUT = Path("reports/v2_error_analysis.csv")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

errors.to_csv(OUTPUT, index=False)

print(f"\nSaved: {OUTPUT}")
