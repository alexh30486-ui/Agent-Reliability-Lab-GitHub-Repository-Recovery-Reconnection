import pandas as pd

PATH = "data/raw/agent_traces.jsonl"

df = pd.read_json(PATH, lines=True)

EXPECTED = {
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

print("=" * 55)
print("AGENT RELIABILITY DATASET CHECK")
print("=" * 55)

print(f"\nTotal traces: {len(df)}")

print("\nLabels:")
counts = df["failure_type"].value_counts()

for label in sorted(EXPECTED):
    print(f"{label:25} {counts.get(label, 0)}")

print("\nMissing labels:")
missing = EXPECTED - set(df["failure_type"])

if missing:
    for label in sorted(missing):
        print(" -", label)
else:
    print("NONE")

print("\nAgent types:")
print(df["agent_type"].value_counts())

print("\nDuplicate trace IDs:", df["trace_id"].duplicated().sum())

print("\n" + "=" * 55)

if len(df) >= 100 and not missing and df["trace_id"].duplicated().sum() == 0:
    print("PASS: Dataset ready for modeling.")
else:
    print("STATUS: Dataset needs more real examples before modeling.")
