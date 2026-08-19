import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, accuracy_score
import joblib

TRAIN = "data/splits/train.csv"
VAL = "data/splits/validation.csv"
TEST = "data/splits/test.csv"
MODEL = "data/processed/reliability_classifier.joblib"

train = pd.read_csv(TRAIN)
val = pd.read_csv(VAL)
test = pd.read_csv(TEST)

model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            ngram_range=(1, 2),
            min_df=1
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

model.fit(train["text"], train["failure_type"])

val_predictions = model.predict(val["text"])
test_predictions = model.predict(test["text"])

print("=" * 60)
print("AGENT RELIABILITY FAILURE CLASSIFIER")
print("=" * 60)

print("\nVALIDATION ACCURACY:")
print(accuracy_score(val["failure_type"], val_predictions))

print("\nTEST ACCURACY:")
print(accuracy_score(test["failure_type"], test_predictions))

print("\nTEST CLASSIFICATION REPORT:")
print(
    classification_report(
        test["failure_type"],
        test_predictions,
        zero_division=0
    )
)

joblib.dump(model, MODEL)

print("\nModel saved to:")
print(MODEL)
