import joblib
import pandas as pd
import numpy as np
import os
from catboost import CatBoostClassifier

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "Models", "best_model.cbm")
TRANSFORMER_PATH = os.path.join(BASE_DIR, "Models", "column_transformer.pkl")

model = CatBoostClassifier()
model.load_model(MODEL_PATH)

transformer = joblib.load(TRANSFORMER_PATH)

# =========================
# Colonnes attendues par le transformer
# =========================

MODEL_FEATURES = [
    "Married/Single",
    "House_Ownership",
    "Car_Ownership",
    "CURRENT_HOUSE_YRS",
    "Région",
    "Catégorie de métier",
    "income_per_age",
    "married_owns_house",
    "owns_car_high_income",
    "age_bin",
    "experience_bin",
    "income_bin",
    "cur_job_years_bin"
]

# =========================
# Feature Engineering
# =========================

def feature_engineering(df):

    # Clip des valeurs avant binning
    df["Age"] = df["Age"].clip(18, 80)
    df["Experience"] = df["Experience"].clip(0, 20)
    df["Income"] = df["Income"].clip(0, 10_000_000)
    df["CURRENT_JOB_YRS"] = df["CURRENT_JOB_YRS"].clip(0, 14)

    df["income_per_age"] = df["Income"] / df["Age"]

    df["married_owns_house"] = np.where(
        (df["Married/Single"] == "married") &
        (df["House_Ownership"] == "owned"),
        "yes", "no"
    )

    df["owns_car_high_income"] = np.where(
        (df["Car_Ownership"] == "yes") &
        (df["Income"] > df["Income"].median()),
        "yes", "no"
    )

    df["age_bin"] = pd.cut(
        df["Age"],
        bins=[20, 30, 40, 50, 60, 80],
        labels=["21-30", "31-40", "41-50", "51-60", "61-80"],
        include_lowest=True
    )

    df["experience_bin"] = pd.cut(
        df["Experience"],
        bins=[-1, 2, 5, 10, 15, 20],
        labels=["0-2", "3-5", "6-10", "11-15", "16-20"]
    )

    df["income_bin"] = pd.cut(
        df["Income"],
        bins=[0, 2_000_000, 4_000_000, 6_000_000, 8_000_000, 10_000_000],
        labels=["0-2M", "2-4M", "4-6M", "6-8M", "8-10M"],
        include_lowest=True
    )

    df["cur_job_years_bin"] = pd.cut(
        df["CURRENT_JOB_YRS"],
        bins=[-1, 2, 5, 9, 14],
        labels=["0-2", "3-5", "6-9", "10-14"]
    )

    return df

# =========================
# Fonction principale de prédiction
# =========================

def predict_risk(data_dict):

    # Transformer en DataFrame
    df = pd.DataFrame([data_dict])

    # Mapping colonnes Django -> dataset ML
    df = df.rename(columns={
        "marital_status": "Married/Single",
        "house_ownership": "House_Ownership",
        "car_ownership": "Car_Ownership",
        "current_house_yrs": "CURRENT_HOUSE_YRS",
        "job_category": "Catégorie de métier",
        "region": "Région",
        "income": "Income",
        "age": "Age",
        "experience": "Experience",
        "cur_job_years": "CURRENT_JOB_YRS"
    })

    # Feature engineering
    df = feature_engineering(df)

    # Garder uniquement les colonnes attendues
    df = df[MODEL_FEATURES]

    # Transformer les données
    X = transformer.transform(df)

    # Prédiction
    proba = model.predict_proba(X)[0][1]

    return float(proba)