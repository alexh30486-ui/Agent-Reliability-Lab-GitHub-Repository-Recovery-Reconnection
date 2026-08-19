# Agent Reliability Lab

A behavior-aware reliability classifier for AI agent traces. The system predicts one of nine outcome or failure classes using both the agent's text and observable execution behavior.

## Status

**The modeling and held-out evaluation milestone is complete.**

| Item | Status |
| --- | --- |
| Development corpus | 110 traces |
| Taxonomy | 9 classes |
| Feature engineering | Complete |
| Classifier iterations | V1-V7 complete |
| Hybrid reliability layer | V8 complete |
| Existing held-out test set | 17 traces |
| V8 result on that set | 17/17 correct, 100% |
| Independent generalization test | Not yet performed |

The 100% result is a result for the existing held-out split. It is not evidence that future, independently collected traces will receive perfect predictions. The repository does not currently contain a separate external evaluation corpus.

## What It Measures

The classifier recognizes:

1. `none`
2. `bad_reasoning`
3. `failure_to_recover`
4. `hallucination`
5. `incomplete_task`
6. `malformed_output`
7. `safety_violation`
8. `unnecessary_tool_call`
9. `wrong_tool`

Features describe both the trace text and behavior such as tool use, evidence support, task completion, contradictions, format validity, safety signals, and explicit reasoning-error signals. See [docs/DATA_SCHEMA.md](docs/DATA_SCHEMA.md) for the data contract.

## Architecture

```text
Agent trace
    |
    v
Processed dataset
    |
    +--------------------------+
    |                          |
    v                          v
Combined trace text       Behavioral features
    |                      tool use, evidence,
    v                      completion, format,
TF-IDF representation     safety, reasoning
    |                          |
    +------------+-------------+
                 v
       V7 logistic-regression model
                 |
                 v
       Statistical ML prediction
                 |
                 v
       V8 deterministic rule layer
                 |
                 v
          Final prediction
```

V8 overrides the statistical prediction for explicit high-confidence signals: safety, malformed JSON/XML, reasoning error, and missing requirements. This keeps the model useful for broad pattern recognition while making directly observable reliability conditions auditable.

## Repository Guide

| Path | Purpose |
| --- | --- |
| `data/raw/` | Source traces |
| `data/processed/` | Labeled data, engineered features, and model artifacts |
| `data/splits/` | Train, validation, and held-out test membership |
| `scripts/` | Dataset, feature, training, and evaluation scripts |
| `docs/` | Architecture, schema, evaluation, and reproducibility notes |
| `reports/` | Versioned error-analysis outputs |
| `src/` | Application and supporting package code |

## Run the Held-Out Evaluation

From the repository root, with the required Python packages available:

```bash
python3 scripts/model/evaluate_v8.py
```

The script reads the V7 model and V3 behavior features, evaluates the existing test split, prints accuracy and a classification report, and writes `reports/v8_error_analysis.csv`.

For the evaluation boundary and known limitations, see [docs/EVALUATION.md](docs/EVALUATION.md). For the exact setup and command order, see [docs/REPRODUCIBILITY.md](docs/REPRODUCIBILITY.md).
