import os
import json
import joblib
import shap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from ..utils.logger import setup_logger

logger = setup_logger()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "src", "models", "tuned_xgboost.pkl")
DATA_DIR = os.path.join(BASE_DIR, "src", "data", "processed")
OUTPUT_DIR = os.path.join(BASE_DIR, "src", "evaluation")

os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Starting Day 4 SHAP analysis...")
logger.info("Starting SHAP explainability analysis")

# Load model and data
print("Loading tuned XGBoost model...")
model = joblib.load(MODEL_PATH)
logger.info("Loaded tuned_xgboost.pkl")

X_train = pd.read_csv(os.path.join(DATA_DIR, "X_train.csv"))
feature_names = X_train.columns.tolist()
print(f"Loaded training data: {X_train.shape} (22 features)")
logger.info(f"Loaded X_train: {X_train.shape}")

# Sample for speed (500 rows)
X_sample = X_train[:500].values
print(f"Using sample: {X_sample.shape} for SHAP computation")
logger.info(f"SHAP sample size: {X_sample.shape}")

# SHAP analysis
print("Computing SHAP values...")
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_sample)
print("SHAP values computed successfully")
logger.info("SHAP values computed")

# Summary plot
print("Generating SHAP summary plot...")
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_sample, feature_names=feature_names, 
                  max_display=15, show=False)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "shap_summary.png"), dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: shap_summary.png")
logger.info("Saved shap_summary.png")

# Feature importance bar plot
print("Generating feature importance plot...")
plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_sample, feature_names=feature_names, 
                  plot_type="bar", max_display=15, show=False)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, "feature_importance.png"), dpi=300, bbox_inches='tight')
plt.close()
print(f"Saved: feature_importance.png")
logger.info("Saved feature_importance.png")

# Top 10 features table
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': np.abs(shap_values).mean(0)
}).sort_values('importance', ascending=False).head(10)

importance_df.to_csv(os.path.join(OUTPUT_DIR, "top_features.csv"), index=False)
print(f"Saved top 10 features: top_features.csv")
print("\nTop 5 features:")
print(importance_df.head())
logger.info("Saved top_features.csv")
logger.info(f"Top features: {importance_df['feature'].head().tolist()}")

print("\nSHAP plots saved:")
print("- shap_summary.png")
print("- feature_importance.png") 
print("- top_features.csv")
print("Day 4 SHAP analysis ✅ COMPLETE")
logger.info("Day 4 SHAP analysis complete")
