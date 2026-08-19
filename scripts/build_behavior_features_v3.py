import pandas as pd
from pathlib import Path

INPUT = Path("data/processed/agent_features.csv")
OUTPUT = Path("data/processed/behavior_features_v3.csv")

df = pd.read_csv(INPUT)

steps = df["steps"].fillna("").str.lower()
tasks = df["task"].fillna("").str.lower()
text = df["text"].fillna("").str.lower()
answers = df["text"].fillna("").str.lower()


# 1. Evidence contradiction
df["has_contradiction"] = (
    text.str.contains(
        "but agent claims|but answer claims|contradicts|says .* but",
        regex=True
    )
).astype(int)


# 2. Expected tool
df["expected_tool_type"] = "unknown"

df.loc[
    tasks.str.contains("calculate|multiply|add|subtract|divide"),
    "expected_tool_type"
] = "calculator"

df.loc[
    tasks.str.contains(
        "database|sql|average|count|rating|records|trend|revenue"
    ),
    "expected_tool_type"
] = "sql"

df.loc[
    tasks.str.contains(
        "file|csv|column|users|json|xml"
    ),
    "expected_tool_type"
] = "file"

df.loc[
    tasks.str.contains(
        "publication|release|director|article|movie|author|research"
    ),
    "expected_tool_type"
] = "search"


df["uses_expected_tool"] = (
    (
        (df["expected_tool_type"] == "calculator")
        & steps.str.contains("calculator")
    )
    |
    (
        (df["expected_tool_type"] == "sql")
        & steps.str.contains("sql")
    )
    |
    (
        (df["expected_tool_type"] == "file")
        & steps.str.contains("open_file")
    )
    |
    (
        (df["expected_tool_type"] == "search")
        & steps.str.contains("search|retrieve")
    )
).astype(int)


# 3. Step count
df["step_count"] = steps.apply(
    lambda x: len(x.split()) if x else 0
)


# 4. Tool execution count
tool_words = [
    "search",
    "retrieve",
    "calculator",
    "sql",
    "open_file",
    "web_search",
]

df["tool_step_count"] = steps.apply(
    lambda x: sum(word in x.split() for word in tool_words)
)


# 5. Repeated search
df["repeated_search"] = steps.apply(
    lambda x: int(
        x.split().count("search") > 1
        or x.split().count("web_search") > 1
    )
)


# 6. Ends with answer
df["ends_with_answer"] = (
    df["last_step"].fillna("").str.lower() == "answer"
).astype(int)


# 7. Has tool call
df["has_tool_call"] = (
    df["tool_calls"].fillna(0) > 0
).astype(int)


# 8. Explicit output-format requirement
df["has_format_requirement"] = (
    tasks.str.contains("json|xml|format|schema|structured output")
    |
    text.str.contains("required json|required xml|schema")
).astype(int)


# 9. Malformed JSON
df["has_malformed_json"] = (
    (
        text.str.contains("json")
        | tasks.str.contains("json")
    )
    &
    text.str.contains(
        "malformed|invalid|missing|closing|unterminated"
    )
).astype(int)


# 10. Malformed XML
df["has_malformed_xml"] = (
    (
        text.str.contains("xml")
        | tasks.str.contains("xml")
    )
    &
    text.str.contains(
        "malformed|invalid|missing|closing|unterminated"
    )
).astype(int)


# 11. Missing task requirement
df["has_missing_requirement"] = (
    text.str.contains(
        "omits|omitted|missing|only one|never|fails to"
    )
).astype(int)


# 12. Answer supported
df["answer_supported"] = (
    ~text.str.contains(
        "contradict|malformed|invalid|unsupported|claims|omits"
    )
).astype(int)


# 13. Task completion
df["task_completed"] = (
    ~text.str.contains(
        "omits|omitted|missing|only one|never|fails to complete"
    )
).astype(int)


# 14. Safety signal
df["has_safety_signal"] = (
    tasks.str.contains(
        "restricted|prohibited|unsafe|dangerous|harmful"
    )
    |
    text.str.contains(
        "prohibited|unsafe|restricted operational|dangerous action"
    )
).astype(int)


OUTPUT.parent.mkdir(parents=True, exist_ok=True)

df.to_csv(OUTPUT, index=False)

print("=" * 60)
print("BEHAVIOR FEATURES V3")
print("=" * 60)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nNew behavioral features:")

for column in [
    "has_contradiction",
    "expected_tool_type",
    "uses_expected_tool",
    "tool_step_count",
    "repeated_search",
    "ends_with_answer",
    "has_tool_call",
    "has_format_requirement",
    "has_malformed_json",
    "has_malformed_xml",
    "has_missing_requirement",
    "answer_supported",
    "task_completed",
    "has_safety_signal",
]:
    print(f"  {column}")

print(f"\nSaved: {OUTPUT}")
