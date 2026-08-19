import pandas as pd
from sklearn.model_selection import train_test_split

INPUT = "data/processed/failure_dataset.csv"

df = pd.read_csv(INPUT)

# 70% train, 15% validation, 15% test
train, temp = train_test_split(
    df,
    test_size=0.30,
    stratify=df["failure_type"],
    random_state=42,
)

validation, test = train_test_split(
    temp,
    test_size=0.50,
    stratify=temp["failure_type"],
    random_state=42,
)

train.to_csv("data/splits/train.csv", index=False)
validation.to_csv("data/splits/validation.csv", index=False)
test.to_csv("data/splits/test.csv", index=False)

print("DATASET SPLIT")
print("=" * 40)
print(f"Train:      {len(train)}")
print(f"Validation: {len(validation)}")
print(f"Test:       {len(test)}")
print(f"Total:      {len(train) + len(validation) + len(test)}")

print("\nTrain labels:")
print(train["failure_type"].value_counts().sort_index())

print("\nValidation labels:")
print(validation["failure_type"].value_counts().sort_index())

print("\nTest labels:")
print(test["failure_type"].value_counts().sort_index())
