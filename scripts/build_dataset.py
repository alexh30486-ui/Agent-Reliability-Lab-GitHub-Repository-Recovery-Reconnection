import json
import pandas as pd

INPUT = "data/raw/agent_traces.jsonl"
OUTPUT = "data/processed/failure_dataset.csv"

rows = []

with open(INPUT) as f:
    for line in f:
        trace = json.loads(line)

        text = (
            f"Agent type: {trace['agent_type']}. "
            f"Task: {trace['task']}. "
            f"Steps: {' -> '.join(trace['steps'])}. "
            f"Tool calls: {trace['tool_calls']}. "
            f"Evidence: {trace.get('evidence', '')}. "
            f"Final answer: {trace['final_answer']}"
        )

        rows.append({
            "trace_id": trace["trace_id"],
            "agent_type": trace["agent_type"],
            "text": text,
            "failure_type": trace["failure_type"],
        })

df = pd.DataFrame(rows)

df.to_csv(OUTPUT, index=False)

print(f"Created {OUTPUT}")
print(f"Rows: {len(df)}")

print("\nLabels:")
print(df["failure_type"].value_counts().sort_index())
