# Agent Reliability Lab - Reproducibility

This document records how to reproduce the current V8 held-out evaluation. Commands assume the working directory is the repository root.

## Environment

Use a Python environment with the packages imported by the pipeline:

- `pandas`
- `scikit-learn`
- `joblib`

The current `requirements.txt` is empty, so it is not a complete dependency lockfile. Install the packages in the active environment explicitly, or populate and pin that file before treating the setup as portable.

Example setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install pandas scikit-learn joblib
```

## Current Artifacts

The committed evaluation uses these inputs:

| Path | Role |
| --- | --- |
| `data/processed/agent_features.csv` | Base engineered dataset |
| `data/processed/behavior_features_v3.csv` | V3 behavior features used by V7/V8 |
| `data/splits/train.csv` | Training membership |
| `data/splits/validation.csv` | Validation membership |
| `data/splits/test.csv` | Existing held-out membership |
| `data/processed/reliability_classifier_v7.joblib` | Persisted V7 model |

The final report is written to `reports/v8_error_analysis.csv`.

## Reproduce the Existing Result

Run the final evaluator:

```bash
python3 scripts/model/evaluate_v8.py
```

Expected summary:

```text
Test examples: 17
Correct: 17
Errors: 0
V8 FINAL ACCURACY: 1.0000
```

The script also prints a classification report and saves the row-level predictions.

## Rebuild the Feature and Model Artifacts

The scripts use repository-relative paths. Run them from the repository root and preserve the split before evaluating:

```bash
python3 scripts/build_behavior_features_v3.py
python3 scripts/model/train_behavior_v7.py
python3 scripts/model/evaluate_v8.py
```

`build_behavior_features_v3.py` reads `data/processed/agent_features.csv` and overwrites `data/processed/behavior_features_v3.csv`. `train_behavior_v7.py` reads the existing train, validation, and test memberships and overwrites `data/processed/reliability_classifier_v7.joblib`.

Do not run `scripts/split_dataset.py` as part of a reproduction of the committed result unless you intend to regenerate the split. It uses stratified 70/15/15 splits with `random_state=42`; regenerating it can still change the committed membership if the source dataset changes.

## Reproducibility Boundaries

- The evaluation is deterministic only for the committed input files, package versions, model artifact, and split membership.
- The repository does not currently pin package versions in `requirements.txt`.
- The 17-trace test set is held out within the original 110-trace corpus; it is not an external generalization set.
- Rebuilding the model can produce different results if dependency versions, source data, or feature logic change.
- The report records predictions and labels, but it is not a substitute for an independently labeled future test corpus.

For the meaning of each dataset field, see [DATA_SCHEMA.md](DATA_SCHEMA.md). For the interpretation of the reported result, see [EVALUATION.md](EVALUATION.md).
