import pandas as pd
from pathlib import Path

INPUT = Path("data/processed/failure_dataset.csv")
OUTPUT = Path("data/error_analysis/error_cases.csv")

df = pd.read_csv(INPUT)

# Manually inspect examples that represent the hardest classes.
target_labels = [
    "hallucination",
    "wrong_tool",
    "bad_reasoning",
    "incomplete_task",
    "unnecessary_tool_call",
    "none",
]

errors = df[df["failure_type"].isin(target_labels)].copy()

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
errors.to_csv(OUTPUT, index=False)

print("=" * 60)
print("ERROR ANALYSIS DATASET")
print("=" * 60)
print(f"Rows exported: {len(errors)}")
print(f"Saved to: {OUTPUT}")
print()
print(errors["failure_type"].value_counts())
