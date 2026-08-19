import pandas as pd

from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report
import joblib

DATA = Path("data/processed/agent_features.csv")
MODEL = Path("data/processed/reliability_classifier_v2.joblib")

df = pd.read_csv(DATA)

print("=" * 60)
print("AGENT RELIABILITY CLASSIFIER V2")
print("=" * 60)

print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")

def make_text(df):
    return (
        "AGENT_TYPE " + df["agent_type"].astype(str)
        + " TASK " + df["task"].astype(str)
        + " STEPS " + df["steps"].astype(str)
        + " TOOL_CALLS " + df["tool_calls"].astype(str)
        + " STEP_COUNT " + df["step_count"].astype(str)
        + " HAS_EVIDENCE " + df["has_evidence"].astype(str)
        + " HAS_ANSWER " + df["has_answer"].astype(str)
        + " FIRST_STEP " + df["first_step"].astype(str)
        + " LAST_STEP " + df["last_step"].astype(str)
        + " TEXT " + df["text"].astype(str)
    )

# Reproducible stratified split
from sklearn.model_selection import train_test_split

train, test = train_test_split(
    df,
    test_size=0.20,
    random_state=42,
    stratify=df["failure_type"]
)

X_train = make_text(train)
X_test = make_text(test)

y_train = train["failure_type"]
y_test = test["failure_type"]

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            ngram_range=(1, 2),
            min_df=1,
            sublinear_tf=True
        )
    ),
    (
        "classifier",
        LogisticRegression(
            max_iter=2000,
            class_weight="balanced"
        )
    )
])

model.fit(X_train, y_train)

predictions = model.predict(X_test)

accuracy = accuracy_score(y_test, predictions)

print("\nTRAINING COMPLETE")
print("-" * 60)

print(f"Train rows: {len(train)}")
print(f"Test rows:  {len(test)}")

print("\nTEST ACCURACY:")
print(f"{accuracy:.4f}")

print("\nCLASSIFICATION REPORT:")
print(
    classification_report(
        y_test,
        predictions,
        zero_division=0
    )
)

MODEL.parent.mkdir(parents=True, exist_ok=True)

joblib.dump(model, MODEL)

print("\nMODEL SAVED:")
print(MODEL)
