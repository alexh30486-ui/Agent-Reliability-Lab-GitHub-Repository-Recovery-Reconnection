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
MODEL = Path("data/processed/reliability_classifier_v4.joblib")


df = pd.read_csv(DATA)
train_ids = pd.read_csv(TRAIN)["trace_id"]
val_ids = pd.read_csv(VAL)["trace_id"]
test_ids = pd.read_csv(TEST)["trace_id"]

train = df[df["trace_id"].isin(train_ids)].copy()
val = df[df["trace_id"].isin(val_ids)].copy()
test = df[df["trace_id"].isin(test_ids)].copy()


def make_text(frame):
    return (
        frame["task"].astype(str)
        + " STEPS "
        + frame["steps"].astype(str)
        + " AGENT "
        + frame["agent_type"].astype(str)
        + " TEXT "
        + frame["text"].astype(str)
    )


behavior_features = [
    "tool_calls",
    "step_count",
    "has_evidence",
    "has_answer",
    "has_contradiction",
    "uses_expected_tool",
    "tool_step_count",
    "repeated_search",
    "ends_with_answer",
    "has_tool_call",
]

preprocessor = ColumnTransformer(
    transformers=[
        ("text", TfidfVectorizer(ngram_range=(1, 2), min_df=1), "combined_text"),
        ("behavior", "passthrough", behavior_features),
        (
            "agent",
            OneHotEncoder(handle_unknown="ignore"),
            ["agent_type"],
        ),
    ]
)

train = train.copy()
val = val.copy()
test = test.copy()

train["combined_text"] = make_text(train)
val["combined_text"] = make_text(val)
test["combined_text"] = make_text(test)

X_train = train[["combined_text", "agent_type"] + behavior_features]
X_val = val[["combined_text", "agent_type"] + behavior_features]
X_test = test[["combined_text", "agent_type"] + behavior_features]

y_train = train["failure_type"]
y_val = val["failure_type"]
y_test = test["failure_type"]

model = Pipeline(
    [
        ("features", preprocessor),
        (
            "classifier",
            LogisticRegression(
                max_iter=3000,
                class_weight="balanced",
            ),
        ),
    ]
)

model.fit(X_train, y_train)

val_pred = model.predict(X_val)
test_pred = model.predict(X_test)

print("=" * 70)
print("AGENT RELIABILITY V3 BEHAVIOR MODEL")
print("=" * 70)

print("\nVALIDATION ACCURACY:")
print(f"{accuracy_score(y_val, val_pred):.4f}")

print("\nTEST ACCURACY:")
print(f"{accuracy_score(y_test, test_pred):.4f}")

print("\nCLASSIFICATION REPORT:")
print(
    classification_report(
        y_test,
        test_pred,
        zero_division=0,
    )
)

MODEL.parent.mkdir(parents=True, exist_ok=True)
joblib.dump(model, MODEL)

print("\nMODEL SAVED:")
print(MODEL)
