# Agent Reliability Lab

A behavior-aware reliability classification system for identifying failure modes in AI agent traces.

The project combines **machine-learning classification** with **explicit behavioral reliability rules** to distinguish successful agent behavior from failures such as bad reasoning, hallucination, incomplete tasks, malformed output, safety violations, and incorrect tool use.

## Project Status

**Modeling and held-out evaluation milestone: complete.**

* Development corpus: **110 agent traces**
* Failure taxonomy: **9 classes**
* Behavioral feature engineering: complete
* V1–V7 classifier iterations: complete
* V8 hybrid reliability layer: complete
* Held-out test set: **17 traces**
* V8 held-out accuracy: **100% (17/17)**
* Final held-out errors: **0**
* Generalization testing: **not yet performed**

The 100% result applies specifically to the existing held-out test set. The project does **not** claim 100% performance on unseen future traces because a genuinely new evaluation corpus has not yet been collected.

---

## Problem

AI agents can fail even when their final response appears superficially reasonable.

Examples include:

* using the wrong tool;
* performing incomplete work;
* producing malformed structured output;
* hallucinating unsupported information;
* making incorrect logical or analytical conclusions;
* repeatedly using tools unnecessarily;
* violating safety requirements;
* failing to recover from an unsuccessful operation.

Traditional text classification alone can miss important behavioral signals.

This project therefore models both:

1. **What the agent said**
2. **How the agent behaved**

---

## Failure Taxonomy

The classifier recognizes nine reliability categories:

| Failure Type            | Description                                                     |
| ----------------------- | --------------------------------------------------------------- |
| `none`                  | Successful or acceptable agent behavior                         |
| `bad_reasoning`         | Incorrect reasoning, interpretation, calculation, or conclusion |
| `failure_to_recover`    | Agent fails to recover from an unsuccessful operation           |
| `hallucination`         | Unsupported or contradicted information                         |
| `incomplete_task`       | Required task components are missing                            |
| `malformed_output`      | Required output format is invalid                               |
| `safety_violation`      | Agent provides prohibited or unsafe operational guidance        |
| `unnecessary_tool_call` | Tool use is unnecessary or excessive                            |
| `wrong_tool`            | Agent selects an inappropriate tool                             |

The taxonomy is documented in:

`docs/taxonomy/failure_taxonomy.md`

---

## System Architecture

```text
Agent Trace
    |
    v
Dataset
    |
    v
Behavior Feature Engineering
    |
    +----------------------+
    |                      |
    v                      v
Text Features        Behavioral Features
TF-IDF               Tool usage
                     Task completion
                     Evidence support
                     Format signals
                     Safety signals
                     Reasoning signals
    |                      |
    +----------+-----------+
               |
               v
       ML Reliability Classifier
               |
               v
       V8 Hybrid Reliability Layer
               |
       +-------+--------+
       |                |
       v                v
 Statistical       Deterministic
 Prediction           Rules
       |                |
       +-------+--------+
               |
               v
        Final Prediction
```

---

## Behavioral Feature Engineering

The final feature set includes signals such as:

* `tool_calls`
* `step_count`
* `has_evidence`
* `has_answer`
* `has_contradiction`
* `has_reasoning_error_signal`
* `answer_supported`
* `uses_expected_tool`
* `tool_step_count`
* `repeated_search`
* `ends_with_answer`
* `has_tool_call`
* `has_missing_requirement`
* `task_completed`
* `has_format_requirement`
* `has_malformed_json`
* `has_malformed_xml`
* `has_safety_signal`

These features allow the model to reason about observable agent behavior rather than relying exclusively on natural-language text.

---

## Why the Hybrid V8 System Exists

During model evaluation, one important failure exposed a limitation of purely statistical classification.

### Trace 055

The trace was labeled:

```text
bad_reasoning
```

The ML model predicted:

```text
none
```

The trace contained:

```text
Agent uses the wrong aggregate interpretation.
```

The behavioral feature engineering correctly detected:

```text
has_reasoning_error_signal = 1
```

However, the statistical classifier did not assign enough weight to that signal.

A deterministic V8 rule was therefore introduced:

```text
reasoning-error signal
        ↓
bad_reasoning
```

The hybrid system changed the final prediction to:

```text
bad_reasoning
```

This demonstrates the central engineering principle of the project:

> Statistical models are useful for pattern recognition, but explicit reliability rules can provide important safeguards when a critical behavioral condition is directly observable.

---

## V8 Evaluation

The final V8 system was evaluated against the existing held-out test set.

### Result

```text
Test examples: 17
Correct:        17
Errors:          0
Accuracy:      1.00
```

Classification performance:

| Class                 | Precision | Recall |   F1 |
| --------------------- | --------: | -----: | ---: |
| bad_reasoning         |      1.00 |   1.00 | 1.00 |
| failure_to_recover    |      1.00 |   1.00 | 1.00 |
| hallucination         |      1.00 |   1.00 | 1.00 |
| incomplete_task       |      1.00 |   1.00 | 1.00 |
| malformed_output      |      1.00 |   1.00 | 1.00 |
| none                  |      1.00 |   1.00 | 1.00 |
| safety_violation      |      1.00 |   1.00 | 1.00 |
| unnecessary_tool_call |      1.00 |   1.00 | 1.00 |
| wrong_tool            |      1.00 |   1.00 | 1.00 |

Overall:

```text
Accuracy:        1.00
Macro F1:        1.00
Weighted F1:     1.00
```

The complete V8 error analysis is stored in:

```text
reports/v8_error_analysis.csv
```

---

## Important Evaluation Limitation

The current 100% score should **not** be interpreted as proof that the system generalizes perfectly to unseen agent behavior.

The available dataset currently contains only the original 110 development traces.

The attempted generalization-set creation correctly stopped when it detected that no genuinely new traces were available.

That safeguard prevents accidental evaluation on traces that were already used during development.

The next meaningful experiment is therefore:

```text
Collect genuinely new traces
        ↓
Do NOT modify the existing model/rules
        ↓
Run V8 unchanged
        ↓
Measure generalization performance
        ↓
Analyze new failures
```

This separation between development evaluation and true out-of-sample testing is intentional.

---

## Reproducibility

From the repository root:

```bash
pip install -r requirements.txt
```

Build the behavioral features:

```bash
python3 scripts/build_behavior_features_v3.py
```

Train the V7 statistical classifier:

```bash
python3 scripts/model/train_behavior_v7.py
```

Run the V8 hybrid evaluation:

```bash
python3 scripts/model/evaluate_v8.py
```

The resulting model and evaluation artifacts are written under:

```text
data/processed/
reports/
```

Additional reproducibility information is documented in:

`docs/REPRODUCIBILITY.md`

---

## Repository Structure

```text
agent-reliability-lab/
│
├── configs/
│
├── data/
│   ├── processed/
│   ├── splits/
│   └── ...
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DATA_SCHEMA.md
│   ├── EVALUATION.md
│   ├── REPRODUCIBILITY.md
│   └── taxonomy/
│       └── failure_taxonomy.md
│
├── reports/
│   ├── confusion_matrix.png
│   ├── error_report.csv
│   └── v8_error_analysis.csv
│
├── scripts/
│   ├── build_dataset.py
│   ├── build_features.py
│   ├── build_behavior_features_v3.py
│   ├── check_dataset.py
│   ├── create_generalization_set.py
│   ├── error_report.py
│   ├── expand_dataset.py
│   ├── generate_real_dataset.py
│   ├── split_dataset.py
│   └── model/
│       ├── train_baseline.py
│       ├── train_baseline_v2.py
│       ├── train_behavior_v3.py
│       ├── train_behavior_v4.py
│       ├── train_behavior_v5.py
│       ├── train_behavior_v6.py
│       ├── train_behavior_v7.py
│       ├── predict_v8.py
│       └── evaluate_v8.py
│
├── src/
│
├── tests/
│   ├── test_structure.py
│   └── test_taxonomy.py
│
├── web/
│   └── index.html
│
├── requirements.txt
└── README.md
```

---

## Engineering Lessons

### 1. Behavioral features can expose failure modes that text alone misses

Tool selection, task completion, output formatting, evidence support, and safety signals provide useful reliability information.

### 2. Model performance should be investigated at the error level

The most useful discovery was not simply the accuracy score. The error analysis identified a specific failure:

```text
bad_reasoning → none
```

That led directly to a targeted reliability rule.

### 3. Hybrid systems can be safer than relying exclusively on statistical prediction

When a critical condition is directly observable, a deterministic rule can act as a guardrail around the statistical model.

### 4. Evaluation boundaries matter

A held-out test score and genuine generalization performance are different measurements.

The project deliberately refuses to create a fake generalization benchmark from previously seen traces.

---

## Current Milestone

**Completed:**

* Dataset construction
* Failure taxonomy
* Feature engineering
* Baseline modeling
* Behavioral modeling
* Error analysis
* V8 hybrid classifier
* Held-out evaluation
* Evaluation documentation
* Reproducibility documentation

**Next milestone:**

Collect a genuinely new set of agent traces and run the unchanged V8 system against them for true generalization testing.

---

## Git Milestones

Recent commits:

```text
7b9aceb Document reliability evaluation and reproducibility
4467237 Complete agent reliability V8 evaluation
fef9458 Add V8 hybrid reliability classifier
```

The repository is currently clean and the modeling/evaluation milestone is complete.
