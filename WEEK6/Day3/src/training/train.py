import pandas as pd
import numpy as np
import json
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

from ..utils.logger import setup_logger  
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

logger = setup_logger()

# ---------------- PATHS ----------------
BASE = Path(__file__).resolve().parent.parent
DATA_DIR = BASE / "data/processed"
MODEL_DIR = BASE / "models"
EVAL_DIR = BASE / "evaluation"

MODEL_DIR.mkdir(parents=True, exist_ok=True)
EVAL_DIR.mkdir(parents=True, exist_ok=True)

logger.info("Starting training pipeline")

# ---------------- LOAD & SCALE ----------------
logger.info("Loading training data...")
X_train = pd.read_csv(DATA_DIR / "X_train.csv")
y_train = pd.read_csv(DATA_DIR / "y_train.csv").values.ravel()
X_test  = pd.read_csv(DATA_DIR / "X_test.csv")
y_test  = pd.read_csv(DATA_DIR / "y_test.csv").values.ravel()

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)    

logger.info(f"Data loaded: X_train={X_train_scaled.shape}, y_train={y_train.shape}")

# ---------------- MODELS ----------------
models = {
    "LinearRegression": LinearRegression(),
    "Ridge": Ridge(),
    "RandomForest": RandomForestRegressor(n_estimators=200, random_state=2025),
    "XGBoost": XGBRegressor(n_estimators=200, random_state=2025)
}

# ---------------- 5-FOLD CV ----------------
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=2025)
results = {}

for name, model in models.items():
    print(f"Training {name}...")
    logger.info(f"Training {name}...")
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=cv, scoring='r2')
    results[name] = {'r2': cv_scores.mean()}
    print(f"  R²: {results[name]['r2']:.3f}")
    logger.info(f"  R²: {results[name]['r2']:.3f}")

# ---------------- BEST MODEL ----------------
best_name = max(results, key=lambda x: results[x]["r2"])
best_model = models[best_name]

logger.info(f"Best model: {best_name} (R²: {results[best_name]['r2']:.3f})")

best_model.fit(X_train_scaled, y_train)
joblib.dump(best_model, MODEL_DIR / "best_model.pkl")

# ---------------- TEST & PLOT ----------------
y_pred = best_model.predict(X_test_scaled)
test_r2 = r2_score(y_test, y_pred)

plt.figure(figsize=(6,5))
plt.scatter(y_test, y_pred, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel("Actual"); plt.ylabel("Predicted")
plt.title(f"{best_name}\nTest R²: {test_r2:.3f}")
plt.savefig(EVAL_DIR / "predictions.png")
plt.close()

# ---------------- SAVE ----------------
json.dump({
    "cv_results": results,
    "test_r2": test_r2,
    "best_model": best_name
}, open(EVAL_DIR / "metrics.json", "w"), indent=2)

logger.info(f"Training complete! Test R²: {test_r2:.3f}")
logger.info(f"Saved: best_model.pkl, metrics.json")

print(f"Best: {best_name} (Test R²: {test_r2:.3f})")
print("Saved: best_model.pkl, metrics.json")
