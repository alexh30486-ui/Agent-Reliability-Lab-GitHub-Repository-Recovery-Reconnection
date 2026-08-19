# Agent Reliability Lab — Evaluation

## Final Evaluation Status

The modeling and evaluation milestone is complete.

### Dataset

- Total traces: 110
- Failure categories: 9
- Train: 77
- Validation: 16
- Test: 17

## V7 Machine Learning Model

The V7 behavioral classifier combines:

- TF-IDF text features
- agent type
- tool usage
- step count
- evidence presence
- answer presence
- contradiction detection
- reasoning-error signals
- expected-tool behavior
- repeated tool/search behavior
- task completion signals
- formatting signals
- malformed JSON/XML signals
- safety signals

V7 test performance:

**Accuracy: 94.12%**

## V8 Hybrid Reliability System

V8 combines the trained ML classifier with deterministic reliability rules.

Explicit rules handle high-confidence behavioral signals:

1. Reasoning-error signal → `bad_reasoning`
2. Malformed JSON/XML → `malformed_output`
3. Safety signal → `safety_violation`
4. Missing requirement → `incomplete_task`

### Held-Out Test Result

| Metric | Result |
|---|---:|
| Test examples | 17 |
| Correct | 17 |
| Errors | 0 |
| Accuracy | 100% |

The V8 system correctly classified every example in the held-out test set.

## Important Evaluation Limitation

A separate generalization evaluation was attempted.

The repository currently contains only the original 110 traces. Therefore, no genuinely unseen traces were available for an independent generalization test.

The project intentionally does **not** report the existing test set as a generalization result.

This distinction prevents evaluation leakage and overclaiming.

## Key Error-Analysis Result

One important failure was identified during evaluation:

`trace_055`

The ML model predicted:

`none`

The labeled failure was:

`bad_reasoning`

The trace contained an explicit reasoning-error signal describing an incorrect aggregate interpretation.

A deterministic reasoning-error rule was added to the V8 hybrid layer. The final V8 prediction correctly became:

`bad_reasoning`

This demonstrates why the project uses both statistical classification and explicit behavioral reliability rules.

## Final Conclusion

The V8 hybrid system successfully completed the held-out evaluation with 17/17 correct predictions.

The next meaningful evaluation would require collecting genuinely new traces that were not used during development or test-set optimization.
