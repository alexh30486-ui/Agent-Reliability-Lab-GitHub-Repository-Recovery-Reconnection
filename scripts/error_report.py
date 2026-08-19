import pandas as pd
import joblib
from pathlib import Path

MODEL = Path("data/processed/reliability_classifier.joblib")
TEST = Path("data/splits/test.csv")
OUTPUT = Path("reports/error_report.csv")

df = pd.read_csv(TEST)
model = joblib.load(MODEL)

X = df["text"]
y = df["failure_type"]

predictions = model.predict(X)

df["predicted"] = predictions
errors = df[df["failure_type"] != df["predicted"]].copy()

print("=" * 60)
print("AGENT RELIABILITY ERROR REPORT")
print("=" * 60)

print(f"\nTest examples: {len(df)}")
print(f"Correct: {(df['failure_type'] == df['predicted']).sum()}")
print(f"Errors: {len(errors)}")

print("\nCONFUSION PAIRS:")

if len(errors) == 0:
    print("No errors.")
else:
    pairs = (
        errors
        .groupby(["failure_type", "predicted"])
        .size()
        .sort_values(ascending=False)
    )

    for (actual, predicted), count in pairs.items():
        print(
            f"{actual:25} -> {predicted:25} {count}"
        )

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
errors.to_csv(OUTPUT, index=False)

print(f"\nSaved: {OUTPUT}")
