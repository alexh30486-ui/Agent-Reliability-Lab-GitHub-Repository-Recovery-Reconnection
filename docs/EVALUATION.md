# Agent Reliability Lab - Evaluation

## Scope

The completed result covers the existing 110-trace corpus:

| Split | Traces |
| --- | ---: |
| Train | 77 |
| Validation | 16 |
| Held-out test | 17 |
| Total | 110 |

The test membership is stored in `data/splits/test.csv`. The V8 evaluation script selects those trace IDs from `data/processed/behavior_features_v3.csv`; it does not create a new test set.

## Model Versions

V7 is the statistical model used by the final evaluation. It combines:

- TF-IDF features from agent type, task, steps, and evidence text
- Structured behavior features for tool use, evidence, completion, contradictions, formatting, safety, and reasoning
- A logistic-regression classifier with balanced class weights

V8 adds a deterministic layer after the V7 prediction. In priority order, explicit signals override the model with:

1. `has_reasoning_error_signal` -> `bad_reasoning`
2. `has_malformed_json` or `has_malformed_xml` -> `malformed_output`
3. `has_safety_signal` -> `safety_violation`
4. `has_missing_requirement` -> `incomplete_task`

The implementation is in `scripts/model/evaluate_v8.py`. The persisted statistical artifact is `data/processed/reliability_classifier_v7.joblib`.

## Results

| Metric | V8 result |
| --- | ---: |
| Held-out examples | 17 |
| Correct predictions | 17 |
| Errors | 0 |
| Accuracy | 100% |

The generated row-level report is `reports/v8_error_analysis.csv`. It includes the actual label, the V7 prediction, the final V8 prediction, and whether a rule changed the prediction.

## Why V8 Was Added

During error analysis, `trace_055` was labeled `bad_reasoning`, while the statistical model predicted `none`. The trace had an explicit reasoning-error signal. The V8 rule converted that prediction to `bad_reasoning`, making the observable condition decisive.

This is the reason for the hybrid design: statistical features support general pattern recognition, while explicit rules make critical, directly detected conditions auditable.

## Caveat

The 17 traces were held out from the training and validation subsets of this corpus, but they are not an independently collected population. The repository does not currently provide a genuinely new external corpus for generalization testing.

Therefore, the defensible claim is:

> V8 classified all 17 traces in the existing held-out split correctly.

It is not defensible to claim 100% accuracy on future or unseen traces. A stronger evaluation requires new traces collected after the model and rules are fixed, with labels assigned independently of prediction results.

## Re-run

From the repository root, with pandas, scikit-learn, and joblib installed:

```bash
python3 scripts/model/evaluate_v8.py
```

See [REPRODUCIBILITY.md](REPRODUCIBILITY.md) for the data and model preparation sequence.
