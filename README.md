# Agent Reliability Lab

A behavior-aware reliability classification system for identifying failure modes in AI agent traces.

The project combines **machine-learning classification** with **explicit behavioral reliability rules** to distinguish successful agent behavior from failures such as bad reasoning, hallucination, incomplete tasks, malformed output, safety violations, and incorrect tool use.

## Project Status

**Modeling and held-out evaluation milestone: complete.**

- Development corpus: **110 agent traces**
- Failure taxonomy: **9 classes**
- Behavioral feature engineering: complete
- V1–V7 classifier iterations: complete
- V8 hybrid reliability layer: complete
- Held-out test set: **17 traces**
- V8 held-out accuracy: **100% (17/17)**
- Final held-out errors: **0**
- Generalization testing: **not yet performed**

The 100% result applies specifically to the existing held-out test set. The project does **not** claim 100% performance on unseen future traces because a genuinely new evaluation corpus has not yet been collected.

## Failure Taxonomy

The system recognizes:

1. `none`
2. `bad_reasoning`
3. `failure_to_recover`
4. `hallucination`
5. `incomplete_task`
6. `malformed_output`
7. `safety_violation`
8. `unnecessary_tool_call`
9. `wrong_tool`

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
