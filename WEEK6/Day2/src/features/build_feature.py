from ..utils import logger as log_module
import pandas as pd
import numpy as np
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logger = log_module.setup_logger()

# Dynamic paths
BASE = Path(__file__).resolve().parent.parent
INPUT = BASE / "data/processed/final.csv"
OUTPUT_DIR = BASE / "data/processed"
FEAT_DIR = BASE.parent / "features"
FEAT_DIR.mkdir(exist_ok=True)

def generate_features(df):
    # Encode categorical
    df = pd.get_dummies(df, columns=['ocean_proximity'], drop_first=True)
    
    # 10 new features
    df['rooms_per_hh'] = df['total_rooms'] / df['households']
    df['bed_per_room'] = df['total_bedrooms'] / df['total_rooms']
    df['pop_per_hh'] = df['population'] / df['households']
    df['log_income'] = np.log1p(df['median_income'])
    df['log_rooms'] = np.log1p(df['total_rooms'])
    df['income_sq'] = df['median_income'] ** 2
    df['income_per_room'] = df['median_income'] / df['total_rooms']
    df['age_income'] = df['housing_median_age'] * df['median_income']
    df['dist_coast'] = np.abs(df['longitude'] + 120)
    df['is_north'] = (df['latitude'] > 37).astype(int)
    
    logger.info("Features created")
    return df

def build_pipeline(data_path):
    # Load data
    df = pd.read_csv(data_path)
    logger.info("Data loaded")
    
    # Generate features
    df = generate_features(df)
    
    # Split X and y
    y = df['median_house_value']
    X = df.drop(columns=['median_house_value'])
    
    # Train/test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2025)
    logger.info("Train/test split done")
    
    # Normalize
    scaler = StandardScaler()
    X_train = pd.DataFrame(scaler.fit_transform(X_train), columns=X.columns)
    X_test = pd.DataFrame(scaler.transform(X_test), columns=X.columns)
    logger.info("Features normalized")
    
    # Save outputs
    X_train.to_csv(OUTPUT_DIR / 'X_train.csv', index=False)
    X_test.to_csv(OUTPUT_DIR / 'X_test.csv', index=False)
    y_train.to_csv(OUTPUT_DIR / 'y_train.csv', index=False, header=['median_house_value'])
    y_test.to_csv(OUTPUT_DIR / 'y_test.csv', index=False, header=['median_house_value'])
    
    # Save feature list
    with open(FEAT_DIR / 'feature_list.json', 'w') as f:
        json.dump(list(X.columns), f, indent=2)
    
    logger.info("Pipeline completed with %d features", len(X.columns))
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    build_pipeline(INPUT)
