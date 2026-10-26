
from pathlib import Path

import pandas as pd

project_root = Path(__file__).resolve().parent.parent

# Load your customer churn dataset
df = pd.read_csv(project_root / "data" / "raw" / "Customer-Churn-Analysis.csv")

# Display the first five rows
print(df.head())

# Display the number of rows and columns
print("Dataset shape:", df.shape)

# Check column names and data types
print(df.info())

# Check missing values
print(df.isnull().sum())

# Remove duplicate customer records
df = df.drop_duplicates(subset="customerID")

# Convert TotalCharges to numbers
df["TotalCharges"] = pd.to_numeric(
    df["TotalCharges"], errors="coerce"
)

# Check missing values
print(df["TotalCharges"].isnull().sum())

# Fill missing values with zero
df["TotalCharges"] = df["TotalCharges"].fillna(0)

# Save the cleaned dataset
df.to_csv(
    project_root / "data" / "raw" / "cleaned_churn.csv",
    index=False
)

print("Data cleaning completed!")

print(df["Churn"].value_counts())

churn_rate = (df["Churn"] == "Yes").mean() * 100

print("Churn rate:", round(churn_rate, 2), "%")


contract_analysis = pd.crosstab(
    df["Contract"],
    df["Churn"],
    normalize="index"
) * 100

print(contract_analysis.round(2))

import matplotlib.pyplot as plt
import seaborn as sns

sns.countplot(data=df, x="Contract", hue="Churn")
plt.title("Customer Churn by Contract Type")
plt.xticks(rotation=15)
plt.tight_layout()
plt.show()
sns.boxplot(data=df, x="Churn", y="MonthlyCharges")
plt.title("Monthly Charges by Churn Status")
plt.show()


import pandas as pd

# Load the cleaned dataset
# Load your raw dataset instead since the processed file doesn't exist yet
df = pd.read_csv("data/raw/Customer-Churn-Analysis.csv")

# Remove ID and target columns from the features
X = df.drop(columns=["Churn", "customerID"])

# Convert Churn into numbers
y = df["Churn"].map({"No": 0, "Yes": 1})

print("Features:", X.shape)
print("Target:", y.shape)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Training rows:", len(X_train))
print("Testing rows:", len(X_test))

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

numeric_columns = X_train.select_dtypes(
    include="number"
).columns.tolist()

categorical_columns = X_train.select_dtypes(
    exclude="number"
).columns.tolist()

numeric_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("scaler", StandardScaler())
])

categorical_pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="most_frequent")),
    ("encoder", OneHotEncoder(handle_unknown="ignore"))
])

preprocessor = ColumnTransformer([
    ("numeric", numeric_pipeline, numeric_columns),
    ("categorical", categorical_pipeline, categorical_columns)
])

model = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ))
])

model.fit(X_train, y_train)

print("Model training completed!")

y_pred = model.predict(X_test)

# Probability of churn, from 0 to 1
churn_probability = model.predict_proba(X_test)[:, 1]

print(y_pred[:10])
print(churn_probability[:10])

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

print("Accuracy:", round(accuracy_score(y_test, y_pred), 3))
print("Precision:", round(precision_score(y_test, y_pred, zero_division=0), 3))
print("Recall:", round(recall_score(y_test, y_pred, zero_division=0), 3))
print("F1-score:", round(f1_score(y_test, y_pred, zero_division=0), 3))
print("ROC-AUC:", round(roc_auc_score(y_test, churn_probability), 3))

print(classification_report(y_test, y_pred, zero_division=0))
print("Confusion matrix:")
print(confusion_matrix(y_test, y_pred))

import os
import joblib
import pandas as pd

# Create folders if they do not exist
os.makedirs("../data/processed", exist_ok=True)
os.makedirs("../models", exist_ok=True)

# Predict churn risk for the dataset
all_features = df.drop(columns=["Churn", "customerID"])

scored_df = df.copy()

scored_df["Churn_Probability"] = model.predict_proba(
    all_features
)[:, 1]

scored_df["Predicted_Churn"] = model.predict(all_features)

scored_df["Risk_Level"] = pd.cut(
    scored_df["Churn_Probability"],
    bins=[-0.001, 0.30, 0.60, 1.001],
    labels=["Low", "Medium", "High"]
)

# Export dashboard data
scored_df.to_csv(
    "../data/processed/churn_predictions.csv",
    index=False
)

# Save the trained model
joblib.dump(model, "../models/churn_model.joblib")

print("Predictions exported successfully!")

