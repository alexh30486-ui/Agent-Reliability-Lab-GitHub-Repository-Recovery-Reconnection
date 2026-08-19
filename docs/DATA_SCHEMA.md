# Agent Reliability Lab — Data Schema

This document explains **exactly** what data the system uses, how it is shaped, and what every important file means.

We keep three main kinds of data:

1. The original agent story (raw trace)
2. The cleaned and labeled version of that story
3. The special “behavior numbers” we give to the computer so it can judge the agent

Everything is designed so we can always go back and check our work. No secrets. No hidden changes.

---

## 1. The Big Picture (Easy Version)

Imagine an AI agent is like a little robot helper that tries to do a job.

Sometimes the robot does a great job.  
Sometimes it makes mistakes (uses the wrong tool, says things that aren’t true, forgets part of the job, etc.).

Our system looks at the robot’s whole story (the “trace”) and gives it a grade:

- “Good job” (`none`)
- or one of 8 different kinds of mistakes

We do this in two ways at the same time:
- We let a smart computer model guess the grade (machine learning)
- We also have simple, clear rules that can correct the model when it is obviously wrong

That combination is called the **V8 Hybrid System**.

---

## 2. Raw Agent Trace (The Original Story)

This is the full story of what the agent did, written down step by step.

| Field            | What it means (simple)                          | Required? |
|------------------|--------------------------------------------------|-----------|
| `trace_id`       | A special name for this story                    | Yes       |
| `task_id`        | Which job the agent was trying to do             | Yes       |
| `agent_name`     | Which robot did the job                          | No        |
| `model_name`     | Which brain (LLM) the robot used                 | No        |
| `steps`          | The list of everything the robot thought and did | Yes       |
| `tool_calls`     | Every time the robot used a tool                 | Yes       |
| `final_answer`   | The last thing the robot said                    | Yes       |
| `raw_log`        | The complete messy original log                  | No        |
| `metadata`       | Extra notes (time, cost, etc.)                   | No        |

### Example of one step
```json
{
  "step_number": 3,
  "type": "tool_call",
  "content": "I am searching for the correct number...",
  "tool_name": "code_interpreter",
  "tool_input": {"code": "print(df.mean())"},
  "tool_output": "42.7"
}

---

**Phase 2 – Copy this entire block next**

```markdown
---

## 3. Processed Dataset Record (The Clean Version)

After we clean the story and give it a grade, it looks like this:

| Field                  | What it means                                      | Required? |
|------------------------|----------------------------------------------------|-----------|
| `trace_id`             | Same special name                                  | Yes       |
| `split`                | Which group this story belongs to (`train`, `held_out`, etc.) | Yes |
| `label`                | The correct grade we humans decided                | Yes       |
| `text`                 | All the words from the story stuck together        | Yes       |
| `behavior_features`    | The special numbers about how the robot behaved    | Yes       |
| `ml_prediction`        | What the computer model guessed                    | After training |
| `hybrid_prediction`    | The final grade after the special V8 rules         | After evaluation |
| `error_analysis_notes` | Notes we wrote when the model was wrong            | Optional  |

### The 9 possible grades (`label`)

none                  → Good job
bad_reasoning         → Robot thought wrong
failure_to_recover    → Robot got stuck and didn’t fix it
hallucination         → Robot made up things that aren’t true
incomplete_task       → Robot forgot part of the job
malformed_output      → Robot’s answer was in the wrong shape
safety_violation      → Robot said something dangerous
unnecessary_tool_call → Robot used tools for no good reason
wrong_tool            → Robot picked the wrong tool

---

## 4. Behavioral Features (The Special Numbers)

These are the most important numbers.  
They tell us **how** the robot behaved, not just what it said.

| Feature Name                 | Simple Meaning                                      | Type    |
|------------------------------|-----------------------------------------------------|---------|
| `tool_calls`                 | How many times the robot used any tool              | number  |
| `tool_step_count`            | How many steps had a tool in them                   | number  |
| `has_tool_call`              | Did the robot use a tool at least once?             | yes/no  |
| `step_count`                 | How many steps did the robot take?                  | number  |
| `repeated_search`            | Did the robot ask the same question more than once? | yes/no  |
| `has_evidence`               | Did the robot show proof for its answer?            | yes/no  |
| `answer_supported`           | Is the final answer backed up by the proof?         | yes/no  |
| `has_contradiction`          | Did the robot say two things that fight each other? | yes/no  |
| `has_reasoning_error_signal` | **Very important!** Did the robot clearly think wrong? | yes/no |
| `uses_expected_tool`         | Did the robot pick the right tool for the job?      | yes/no  |
| `ends_with_answer`           | Did the robot finish with a clear answer?           | yes/no  |
| `has_missing_requirement`    | Did the robot forget something important?           | yes/no  |
| `task_completed`             | Did the robot finish the whole job?                 | yes/no  |
| `has_format_requirement`     | Was the robot supposed to answer in a special shape?| yes/no  |
| `has_malformed_json`         | Was the JSON broken?                                | yes/no  |
| `has_malformed_xml`          | Was the XML broken?                                 | yes/no  |
| `has_safety_signal`          | Did the robot say something unsafe?                 | yes/no  |

### Why `has_reasoning_error_signal` is special

One time the smart computer model said “Good job” (`none`) even though the robot clearly thought wrong.

We added a simple rule:

> If `has_reasoning_error_signal` is “yes”,  
> then the final grade must be `bad_reasoning`.

That rule fixed the mistake.  
This is why we use a **hybrid** system (computer + clear rules).
---

## 4. Behavioral Features (The Special Numbers)

These are the most important numbers.  
They tell us **how** the robot behaved, not just what it said.

| Feature Name                 | Simple Meaning                                      | Type    |
|------------------------------|-----------------------------------------------------|---------|
| `tool_calls`                 | How many times the robot used any tool              | number  |
| `tool_step_count`            | How many steps had a tool in them                   | number  |
| `has_tool_call`              | Did the robot use a tool at least once?             | yes/no  |
| `step_count`                 | How many steps did the robot take?                  | number  |
| `repeated_search`            | Did the robot ask the same question more than once? | yes/no  |
| `has_evidence`               | Did the robot show proof for its answer?            | yes/no  |
| `answer_supported`           | Is the final answer backed up by the proof?         | yes/no  |
| `has_contradiction`          | Did the robot say two things that fight each other? | yes/no  |
| `has_reasoning_error_signal` | **Very important!** Did the robot clearly think wrong? | yes/no |
| `uses_expected_tool`         | Did the robot pick the right tool for the job?      | yes/no  |
| `ends_with_answer`           | Did the robot finish with a clear answer?           | yes/no  |
| `has_missing_requirement`    | Did the robot forget something important?           | yes/no  |
| `task_completed`             | Did the robot finish the whole job?                 | yes/no  |
| `has_format_requirement`     | Was the robot supposed to answer in a special shape?| yes/no  |
| `has_malformed_json`         | Was the JSON broken?                                | yes/no  |
| `has_malformed_xml`          | Was the XML broken?                                 | yes/no  |
| `has_safety_signal`          | Did the robot say something unsafe?                 | yes/no  |

### Why `has_reasoning_error_signal` is special

One time the smart computer model said “Good job” (`none`) even though the robot clearly thought wrong.

We added a simple rule:

> If `has_reasoning_error_signal` is “yes”,  
> then the final grade must be `bad_reasoning`.

That rule fixed the mistake.  
This is why we use a **hybrid** system (computer + clear rules).
---

## 5. Evaluation Model & Reports (The Most Important Part)

### What “Build Complete” means

We have finished building and testing the current version of the system:

- All 110 training stories have been processed
- All behavioral features have been calculated
- The computer model (V7) has been trained
- The special V8 rules have been added
- We tested the whole system on 17 secret stories it had never seen
- The system got **every single one correct** (17 out of 17)

That is what “Build Complete” means for the modeling and held-out evaluation milestone.

### Important Warning (Be Critical)

Getting 17 out of 17 correct is **great**, but it does **not** mean the system is perfect forever.

Those 17 stories came from the same big group of 110 stories.  
We have **not** yet tested the system on brand-new stories that the computer has never seen in any way.

Until we collect completely new stories and test again, we cannot claim the system will always work this well.

This is honest and important.

---

## 6. Evaluation Reports (Where the Proof Lives)

After we run the final test, we save several reports:

| Report File                     | What it shows                                      | Why it matters |
|--------------------------------|----------------------------------------------------|----------------|
| `reports/v8_error_analysis.csv`| Every prediction the system made on the 17 stories | Shows zero mistakes |
| `reports/confusion_matrix.png` | A picture of how the grades matched                | Easy to see perfect results |
| `reports/error_report.csv`     | Older error reports from earlier versions          | Shows how we improved |

### What the final numbers look like
Test stories tried : 17
Stories correct    : 17
Stories wrong      :  0
Accuracy           : 100%
Every single grade (all 9 kinds) also scored perfectly.
---

## 7. Where Everything Lives

| Kind of data                     | Folder / File                              |
|----------------------------------|--------------------------------------------|
| Original stories                 | `data/raw/`                                |
| Cleaned and labeled stories      | `data/processed/`                          |
| Train / test groups              | `data/splits/`                             |
| Behavior numbers                 | `data/processed/behavior_features_v3.*`    |
| Final evaluation results         | `reports/v8_error_analysis.csv`            |
| Picture of the results           | `reports/confusion_matrix.png`             |

---

## 8. Rules We Never Break

1. We never let the test stories help train the model.
2. Once a story has a correct grade, we do not change it later.
3. The same story always produces the same behavior numbers.
4. We always write down which version of the features we used.

---

## 9. Related Documents

- How the whole system works → `docs/ARCHITECTURE.md`
- What each kind of mistake means → `docs/taxonomy/failure_taxonomy.md`
- How we test the system → `docs/EVALUATION.md`
- How to run everything again → `docs/REPRODUCIBILITY.md`

---

**Status: Modeling and held-out evaluation build is complete.**  
Next big job: collect completely new agent stories and test the system on them without changing anything.

---

*Last updated: August 2026*  
*Aligned with V8 Hybrid System*