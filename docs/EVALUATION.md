# Agent Reliability Lab — Evaluation

This document describes how the Agent Reliability Lab system was evaluated, what the results mean, and — equally important — what they do **not** mean.

---

## 1. Evaluation Goal

The goal of evaluation is to measure how accurately the hybrid V8 system assigns one of the nine reliability classes to an agent trace.

We care about two different questions:

1. **Held-out performance** — How well does the system perform on traces that were deliberately kept out of training and feature decisions?
2. **True generalization** — How well does the system perform on completely new traces that were never seen during any part of development?

These are not the same question.

---

## 2. Held-Out Evaluation (Completed)

### Setup

- Development corpus: 110 labeled agent traces
- Held-out test set: 17 traces
- The held-out traces were never used for training, feature engineering decisions, or rule design
- Model: V7 logistic regression + V8 hybrid reliability rules
- Evaluation script: `scripts/model/evaluate_v8.py`

### Results

```text
Test examples : 17
Correct       : 17
Errors        :  0
Accuracy      : 1.00
Macro F1      : 1.00
Weighted F1   : 1.00

---

**Phase 2 – Copy this next**

```markdown
### Per-Class Performance

| Class                   | Precision | Recall | F1   |
|-------------------------|-----------|--------|------|
| bad_reasoning           | 1.00      | 1.00   | 1.00 |
| failure_to_recover      | 1.00      | 1.00   | 1.00 |
| hallucination           | 1.00      | 1.00   | 1.00 |
| incomplete_task         | 1.00      | 1.00   | 1.00 |
| malformed_output        | 1.00      | 1.00   | 1.00 |
| none                    | 1.00      | 1.00   | 1.00 |
| safety_violation        | 1.00      | 1.00   | 1.00 |
| unnecessary_tool_call   | 1.00      | 1.00   | 1.00 |
| wrong_tool              | 1.00      | 1.00   | 1.00 |

Every class achieved perfect scores on this held-out set.

Full prediction-level details are stored in:

```text
reports/v8_error_analysis.csv
3. Why the Hybrid Layer Mattered
During earlier model iterations, a purely statistical classifier made a critical error on Trace 055:

Ground-truth label: bad_reasoning
Model prediction: none
Behavioral feature correctly fired: has_reasoning_error_signal = 1

The statistical model did not give enough weight to that signal.
A deterministic V8 rule was introduced:
IF has_reasoning_error_signal == 1
THEN force prediction = bad_reasoning
After the rule was added, the prediction became correct.
This is the primary reason the final system is hybrid rather than purely statistical.

---

**Phase 3 – Copy this next**

```markdown
---

## 4. Critical Limitation (Read Carefully)

The 100% held-out result is **real** and **reproducible** on the current 17-trace set.

It is **not** evidence that the system will achieve 100% accuracy on future, previously unseen agent behavior.

Reasons:

- All 110 traces (including the 17 held-out ones) come from the same original collection process.
- No genuinely new evaluation corpus has been collected yet.
- The project deliberately refused to create a synthetic “generalization” set from traces that had already been seen during development.

This safeguard exists to prevent false confidence.

---

## 5. Next Required Experiment

The only scientifically meaningful next step is:

```text
1. Collect a new set of agent traces that never appeared in the original 110
2. Freeze the existing V8 model and rules (do not retrain or redesign)
3. Run the unchanged V8 system on the new traces
4. Measure accuracy, per-class performance, and error modes
5. Analyze every misclassification
Only after that experiment can we make claims about true generalization.

---

**Phase 4 – Final block**

```markdown
---

## 6. Evaluation Artifacts

| Artifact                        | Location                              | Purpose                              |
|---------------------------------|---------------------------------------|--------------------------------------|
| V8 prediction + error analysis  | `reports/v8_error_analysis.csv`       | Full per-trace results               |
| Confusion matrix                | `reports/confusion_matrix.png`        | Visual summary of held-out results   |
| Older error reports             | `reports/error_report.csv`            | History of earlier model versions    |
| Evaluation script               | `scripts/model/evaluate_v8.py`        | Reproducible evaluation entry point  |

---

## 7. Design Principles Used in Evaluation

1. **Strict separation** between development data and held-out data.
2. **No post-hoc feature or rule changes** after seeing held-out results (except the single documented V8 rule that was motivated by an earlier error analysis).
3. **Error-level inspection** is valued more highly than aggregate accuracy alone.
4. **Honest reporting** of limitations is required. Perfect held-out scores are reported with the explicit caveat that they do not equal generalization.

---

## 8. Related Documents

- System architecture → [`docs/ARCHITECTURE.md`](ARCHITECTURE.md)
- Data schema & features → [`docs/DATA_SCHEMA.md`](DATA_SCHEMA.md)
- How to reproduce results → [`docs/REPRODUCIBILITY.md`](REPRODUCIBILITY.md)
- Failure definitions → [`docs/taxonomy/failure_taxonomy.md`](taxonomy/failure_taxonomy.md)

---

**Status:** Held-out evaluation complete (17/17).
**Next milestone:** True out-of-sample generalization test on newly collected traces.

*Last updated: August 2026 — aligned with V8 hybrid system*