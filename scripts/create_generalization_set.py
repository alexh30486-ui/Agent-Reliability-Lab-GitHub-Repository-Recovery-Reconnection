import pandas as pd
from pathlib import Path

SOURCE = Path("data/processed/agent_features.csv")
OUTPUT = Path("data/generalization/generalization_traces.csv")

df = pd.read_csv(SOURCE)

# Use traces outside the existing 110-row corpus as the source pool.
# If the dataset contains only the original 110 rows, stop rather than
# accidentally evaluating on previously seen data.
if len(df) <= 110:
    raise SystemExit(
        f"STOP: source contains only {len(df)} rows. "
        "Need genuinely new traces before running generalization testing."
    )

# Reserve rows that were not part of the original 110-row development corpus.
new_df = df.iloc[110:].copy()

new_df.to_csv(OUTPUT, index=False)

print("=" * 70)
print("GENERALIZATION SET")
print("=" * 70)
print(f"Original development rows: 110")
print(f"New unseen rows available: {len(new_df)}")
print(f"Saved: {OUTPUT}")
