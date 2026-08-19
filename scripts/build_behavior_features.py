import pandas as pd
from pathlib import Path

INPUT = Path("data/processed/agent_features.csv")
OUTPUT = Path("data/processed/behavior_features.csv")

df = pd.read_csv(INPUT)


def contains_any(text, terms):
    text = str(text).lower()
    return int(any(term in text for term in terms))


# Evidence contradicts the answer
df["has_contradiction"] = df["text"].apply(
    lambda x: contains_any(
        x,
        [
            "but agent claims",
            "but answer claims",
            "contradicts",
            "wrong",
            "incorrect",
            "does not support",
        ],
    )
)


# Evidence explicitly says something required was missing
df["has_missing_requirement"] = df["text"].apply(
    lambda x: contains_any(
        x,
        [
            "omits",
            "omitted",
            "only one",
            "never",
            "missing",
            "incomplete",
        ],
    )
)


# Tool selection indicators
df["uses_expected_tool"] = (
    (
        (df["task"].str.contains("calculate", case=False, na=False))
        & (df["steps"].str.contains("calculator", case=False, na=False))
    )
    |
    (
        (df["task"].str.contains("database|average|count|rating", case=False, na=False))
        & (df["steps"].str.contains("sql", case=False, na=False))
    )
    |
    (
        (df["task"].str.contains("file|csv|column|revenue|users", case=False, na=False))
        & (df["steps"].str.contains("open_file", case=False, na=False))
    )
).astype(int)


# Repeated / unnecessary tool behavior
df["has_repeated_tool"] = (
    df["step_count"] < df["tool_calls"] + 2
).astype(int)


# Evidence exists and answer exists
df["answer_supported"] = (
    (df["has_evidence"] == 1)
    & (df["has_answer"] == 1)
    & (df["has_contradiction"] == 0)
).astype(int)


# Basic completion signal
df["task_completed"] = (
    (df["has_answer"] == 1)
    & (df["has_missing_requirement"] == 0)
).astype(int)


OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print("=" * 60)
print("BEHAVIOR FEATURE ENGINEERING")
print("=" * 60)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nNew features:")

for column in [
    "has_contradiction",
    "has_missing_requirement",
    "uses_expected_tool",
    "has_repeated_tool",
    "answer_supported",
    "task_completed",
]:
    print(f"  {column}")

print(f"\nSaved: {OUTPUT}")
