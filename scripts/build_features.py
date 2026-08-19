import pandas as pd
from pathlib import Path

INPUT = Path("data/raw/agent_traces.jsonl")
OUTPUT = Path("data/processed/agent_features.csv")

rows = []

import json

with INPUT.open() as f:
    for line in f:
        trace = json.loads(line)

        steps = trace.get("steps", [])
        evidence = trace.get("evidence", "")
        answer = trace.get("final_answer", "")

        rows.append({
            "trace_id": trace["trace_id"],
            "agent_type": trace["agent_type"],
            "task": trace["task"],
            "steps": " ".join(steps),
            "tool_calls": trace["tool_calls"],
            "step_count": len(steps),
            "has_evidence": int(bool(evidence)),
            "has_answer": int(bool(answer)),
            "first_step": steps[0] if steps else "",
            "last_step": steps[-1] if steps else "",
            "text": (
                f"Task: {trace['task']} "
                f"Steps: {' '.join(steps)} "
                f"Evidence: {evidence} "
                f"Answer: {answer}"
            ),
            "failure_type": trace["failure_type"],
        })

df = pd.DataFrame(rows)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT, index=False)

print("=" * 60)
print("STRUCTURED AGENT FEATURES")
print("=" * 60)
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")
print(f"Saved: {OUTPUT}")

print("\nFeatures:")
for column in df.columns:
    print(f"  {column}")
