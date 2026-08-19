from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


DATA = Path("data/processed/behavior_features_v3.csv")
TRAIN = Path("data/splits/train.csv")
VAL = Path("data/splits/validation.csv")
TEST = Path("data/splits/test.csv")

MODEL = Path(
    "data/processed/reliability_classifier_v5.joblib"
)


# ============================================================
# LOAD DATA
# ============================================================

df = pd.read_csv(DATA)

train_ids = pd.read_csv(TRAIN)["trace_id"]
val_ids = pd.read_csv(VAL)["trace_id"]
test_ids = pd.read_csv(TEST)["trace_id"]

train = df[df["trace_id"].isin(train_ids)].copy()
val = df[df["trace_id"].isin(val_ids)].copy()
test = df[df["trace_id"].isin(test_ids)].copy()


# ============================================================
# COMBINED TEXT
# ============================================================

def add_combined_text(data):
    data = data.copy()

    data["combined_text"] = (
        "AGENT " + data["agent_type"].fillna("").astype(str)
        + " TASK " + data["task"].fillna("").astype(str)
        + " STEPS " + data["steps"].fillna("").astype(str)
        + " TEXT " + data["text"].fillna("").astype(str)
    )

    return data


train = add_combined_text(train)
val = add_combined_text(val)
test = add_combined_text(test)


# ============================================================
# BEHAVIOR FEATURES
# ============================================================

behavior_features = [
    # Existing execution behavior
    "tool_calls",
    "step_count",
    "has_evidence",
    "has_answer",

    # Reasoning
    "has_contradiction",
    "answer_supported",

    # Tool behavior
    "uses_expected_tool",
    "tool_step_count",
    "repeated_search",
    "ends_with_answer",
    "has_tool_call",

    # Task completion
    "has_missing_requirement",
    "task_completed",

    # Output format
    "has_format_requirement",
    "has_malformed_json",
    "has_malformed_xml",

    # Safety
    "has_safety_signal",
]


# Verify every feature exists before training
missing = [
    feature
    for feature in behavior_features
    if feature not in df.columns
]

if missing:
    raise ValueError(
        f"Missing behavior features: {missing}"
    )


# ============================================================
# INPUTS
# ============================================================

X_train = train[
    ["combined_text", "agent_type"] + behavior_features
]

X_val = val[
    ["combined_text", "agent_type"] + behavior_features
]

X_test = test[
    ["combined_text", "agent_type"] + behavior_features
]

y_train = train["failure_type"]
y_val = val["failure_type"]
y_test = test["failure_type"]


# ============================================================
# PREPROCESSOR
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "text",
            TfidfVectorizer(
                ngram_range=(1, 2),
                min_df=1,
                sublinear_tf=True,
            ),
            "combined_text",
        ),
        (
            "agent",
            OneHotEncoder(
                handle_unknown="ignore"
            ),
            ["agent_type"],
        ),
        (
            "behavior",
            "passthrough",
            behavior_features,
        ),
    ]
)


# ============================================================
# MODEL
# ============================================================

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            LogisticRegression(
                max_iter=5000,
                class_weight="balanced",
                C=2.0,
            ),
        ),
    ]
)


# ============================================================
# TRAIN
# ============================================================

print("=" * 70)
print("AGENT RELIABILITY V5 BEHAVIOR MODEL")
print("=" * 70)

print(f"\nTraining rows:   {len(train)}")
print(f"Validation rows: {len(val)}")
print(f"Test rows:       {len(test)}")

print("\nBehavior features:")

for feature in behavior_features:
    print(f"  {feature}")

model.fit(X_train, y_train)


# ============================================================
# VALIDATION
# ============================================================

val_pred = model.predict(X_val)

print("\nVALIDATION ACCURACY:")
print(
    f"{accuracy_score(y_val, val_pred):.4f}"
)


# ============================================================
# TEST
# ============================================================

test_pred = model.predict(X_test)

print("\nTEST ACCURACY:")
print(
    f"{accuracy_score(y_test, test_pred):.4f}"
)

print("\nCLASSIFICATION REPORT:")

print(
    classification_report(
        y_test,
        test_pred,
        zero_division=0,
    )
)


# ============================================================
# SAVE
# ============================================================

MODEL.parent.mkdir(
    parents=True,
    exist_ok=True,
)

joblib.dump(model, MODEL)

print("\nMODEL SAVED:")
print(MODEL)
