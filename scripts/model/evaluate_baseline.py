import pandas as pd
import joblib

from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

TEST = "data/splits/test.csv"
MODEL = "data/processed/reliability_classifier.joblib"

df = pd.read_csv(TEST)
model = joblib.load(MODEL)

predictions = model.predict(df["text"])

labels = sorted(df["failure_type"].unique())

cm = confusion_matrix(
    df["failure_type"],
    predictions,
    labels=labels
)

print("CONFUSION MATRIX")
print("=" * 60)

print("Labels:")
print(labels)

print("\nMatrix:")
print(cm)

print("\nPREDICTIONS")
for actual, predicted, text in zip(
    df["failure_type"],
    predictions,
    df["text"]
):
    status = "CORRECT" if actual == predicted else "WRONG"

    print(f"\n[{status}]")
    print(f"Actual:    {actual}")
    print(f"Predicted: {predicted}")
    print(f"Trace:     {text[:180]}...")

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=labels
)

display.plot(
    xticks_rotation=45
)

plt.tight_layout()
plt.savefig(
    "reports/confusion_matrix.png",
    dpi=150
)

print("\nSaved:")
print("reports/confusion_matrix.png")
