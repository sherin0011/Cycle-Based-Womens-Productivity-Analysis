import os
import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Set plot styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

def run_pipeline():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    data_path = os.path.join(base_dir, 'data', 'womens_cycle_productivity_dataset.csv')
    img_dir = os.path.join(base_dir, 'images')
    model_dir = os.path.join(base_dir, 'models')
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(model_dir, exist_ok=True)
    
    print("=" * 70)
    print("PHASE 4: DATA UNDERSTANDING & EXTENDED HEALTH METRICS")
    print("=" * 70)
    df = pd.read_csv(data_path)
    print(f"Raw Dataset Shape: {df.shape}")
    print(df.info())
    print("\nStatistical Summary:")
    print(df.describe())
    
    print("\n" + "=" * 70)
    print("PHASE 5: DATA CLEANING & IMPUTATION")
    print("=" * 70)
    duplicate_count = df.duplicated().sum()
    print(f"Duplicate Rows Identified: {duplicate_count}")
    if duplicate_count > 0:
        df.drop_duplicates(inplace=True)
        
    missing = df.isnull().sum()
    print(f"\nMissing Values:\n{missing}")
    if missing.sum() > 0:
        if 'Sleep_Hours' in df.columns:
            df['Sleep_Hours'].fillna(df['Sleep_Hours'].median(), inplace=True)
        if 'Stress_Level' in df.columns:
            df['Stress_Level'].fillna(df['Stress_Level'].median(), inplace=True)
            
    print("\n" + "=" * 70)
    print("PHASE 6: FEATURE ENGINEERING & PCOD ENCODING")
    print("=" * 70)
    phase_order = {'Menstrual': 0, 'Follicular': 1, 'Ovulation': 2, 'Luteal': 3}
    df['Cycle_Phase_Encoded'] = df['Cycle_Phase'].map(phase_order)
    
    # Encode PCOD / PCOS Condition (Yes=1, No=0)
    df['PCOS_PCOD_Encoded'] = (df['PCOS_PCOS_Condition'] == 'Yes').astype(int) if 'PCOS_PCOS_Condition' in df.columns else (df['PCOS_PCOD_Condition'] == 'Yes').astype(int)
    
    le_work = LabelEncoder()
    df['Work_Mode_Encoded'] = le_work.fit_transform(df['Work_Mode'])
    
    # Feature: Health Score
    df['Health_Score'] = (df['Energy_Level'] + df['Mood_Score'] - df['Stress_Level'] - (0.5 * df['Pain_Level']) - (0.3 * df['Hormonal_Imbalance_Score'])).round(2)
    
    print("Sample Feature Rows:")
    print(df[['Cycle_Phase', 'PCOS_PCOD_Condition', 'Period_Delay_Days', 'Health_Score']].head())

    print("\n" + "=" * 70)
    print("PHASE 7: EXPLORATORY DATA ANALYSIS (EDA)")
    print("=" * 70)
    palette = ['#e63946', '#457b9d', '#2a9d8f', '#e76f51']
    
    # Plot 1: Productivity by Cycle Phase
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(data=df, x='Cycle_Phase', y='Productivity_Score', order=['Menstrual', 'Follicular', 'Ovulation', 'Luteal'], palette=palette, ax=ax, capsize=0.1, errorbar=('ci', 95))
    ax.set_title("Average Productivity Score by Cycle Phase", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Cycle Phase", fontsize=12, fontweight='bold')
    ax.set_ylabel("Productivity Score (0-100)", fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'productivity_by_cycle_phase.png'))
    plt.close()
    
    # Plot 2: PCOD/PCOS Impact on Productivity & Stress
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    pcod_col = 'PCOS_PCOD_Condition'
    sns.barplot(data=df, x=pcod_col, y='Productivity_Score', palette=['#2a9d8f', '#e63946'], ax=axes[0])
    axes[0].set_title("Productivity: PCOD vs Non-PCOD", fontsize=13, fontweight='bold')
    axes[0].set_ylabel("Productivity Score", fontsize=11, fontweight='bold')
    
    sns.barplot(data=df, x=pcod_col, y='Stress_Level', palette=['#2a9d8f', '#e76f51'], ax=axes[1])
    axes[1].set_title("Stress Index: PCOD vs Non-PCOD", fontsize=13, fontweight='bold')
    axes[1].set_ylabel("Stress Level (1-10)", fontsize=11, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'pcod_vs_productivity.png'))
    plt.close()
    
    # Plot 3: Period Delay Days vs Productivity
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(data=df, x='Period_Delay_Days', y='Productivity_Score', scatter_kws={'alpha':0.3, 'color':'#e76f51'}, line_kws={'color':'#e63946', 'linewidth':2}, ax=ax)
    ax.set_title("Period Delay (Days) vs Productivity Score", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Period Delay (Days)", fontsize=12, fontweight='bold')
    ax.set_ylabel("Productivity Score", fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'period_delay_vs_productivity.png'))
    plt.close()

    # Plot 4: Correlation Heatmap
    fig, ax = plt.subplots(figsize=(10, 8))
    num_cols = ['Age', 'Cycle_Phase_Encoded', 'PCOS_PCOD_Encoded', 'Period_Delay_Days', 'Hormonal_Imbalance_Score', 'Sleep_Hours', 'Stress_Level', 'Pain_Level', 'Mood_Score', 'Energy_Level', 'Health_Score', 'Productivity_Score']
    corr = df[num_cols].corr()
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", cbar=True, ax=ax, linewidths=0.5)
    ax.set_title("Correlation Matrix of Cycle, PCOD & Health Metrics", fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'correlation_heatmap.png'))
    plt.close()

    print("[SUCCESS] Extended EDA visualizations saved to 'images/'.")

    print("\n" + "=" * 70)
    print("PHASE 10-13: MACHINE LEARNING MODEL BUILDING & EVALUATION")
    print("=" * 70)
    
    feature_cols = ['Cycle_Phase_Encoded', 'PCOS_PCOD_Encoded', 'Period_Delay_Days', 'Hormonal_Imbalance_Score', 'Symptom_Severity', 'Sleep_Hours', 'Stress_Level', 'Pain_Level', 'Mood_Score', 'Energy_Level', 'Health_Score']
    X = df[feature_cols]
    y = df['Productivity_Score']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Train samples: {len(X_train)} | Test samples: {len(X_test)}")
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    y_pred_lr = lr.predict(X_test_scaled)
    
    rf = RandomForestRegressor(n_estimators=150, max_depth=14, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    
    gb = GradientBoostingRegressor(n_estimators=150, learning_rate=0.08, max_depth=5, random_state=42)
    gb.fit(X_train, y_train)
    y_pred_gb = gb.predict(X_test)
    
    def evaluate_model(name, y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)
        rmse = np.sqrt(mse)
        r2 = r2_score(y_true, y_pred)
        print(f"\n--- {name} Performance ---")
        print(f"  MAE  : {mae:.4f}")
        print(f"  MSE  : {mse:.4f}")
        print(f"  RMSE : {rmse:.4f}")
        print(f"  R²   : {r2:.4f}")
        return {'MAE': round(mae, 4), 'MSE': round(mse, 4), 'RMSE': round(rmse, 4), 'R2_Score': round(r2, 4)}

    metrics = {
        'Linear Regression': evaluate_model('Linear Regression', y_test, y_pred_lr),
        'Random Forest': evaluate_model('Random Forest Regressor', y_test, y_pred_rf),
        'Gradient Boosting': evaluate_model('Gradient Boosting Regressor', y_test, y_pred_gb)
    }
    
    importances = rf.feature_importances_
    feat_imp = pd.Series(importances, index=feature_cols).sort_values(ascending=True)
    
    print("\n" + "=" * 70)
    print("FEATURE IMPORTANCE ANALYSIS")
    print("=" * 70)
    for feat, imp in feat_imp.sort_values(ascending=False).items():
        print(f"  {feat:25s}: {imp*100:.2f}%")
        
    fig, ax = plt.subplots(figsize=(9, 5))
    feat_imp.plot(kind='barh', color='#2a9d8f', ax=ax)
    ax.set_title("Random Forest Feature Importance Analysis", fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel("Relative Importance Score", fontsize=12, fontweight='bold')
    ax.set_ylabel("Features", fontsize=12, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(img_dir, 'feature_importance.png'))
    plt.close()
    
    joblib.dump(rf, os.path.join(model_dir, 'random_forest_model.joblib'))
    joblib.dump(scaler, os.path.join(model_dir, 'scaler.joblib'))
    
    export_metadata = {
        'metrics': metrics,
        'feature_importance': feat_imp.to_dict(),
        'feature_names': feature_cols
    }
    with open(os.path.join(model_dir, 'model_metrics.json'), 'w') as f:
        json.dump(export_metadata, f, indent=2)
        
    print(f"\n[SUCCESS] Trained model pipeline completed and saved into '{model_dir}'")

if __name__ == '__main__':
    run_pipeline()
