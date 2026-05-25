# XGBoost Usage Guide

**Official Documentation:** https://xgboost.readthedocs.io/

**Version:** 3.1.3

## Installation

```bash
# Via pip
pip install xgboost

# Specific version
pip install xgboost==3.1.3

# With GPU support (CUDA required)
pip install xgboost[gpu]
```

## Key Parameters

### Tree Booster Parameters

**Learning Rate & Regularization:**
- `learning_rate` (eta): Step size shrinkage (default: 0.3, typical: 0.01-0.3)
- `max_depth`: Maximum tree depth (default: 6, typical: 3-10)
- `min_child_weight`: Minimum sum of instance weight in child (default: 1)
- `gamma`: Minimum loss reduction for split (default: 0)
- `subsample`: Fraction of samples for training each tree (default: 1, typical: 0.5-1)
- `colsample_bytree`: Fraction of features per tree (default: 1, typical: 0.5-1)
- `lambda` (reg_lambda): L2 regularization (default: 1)
- `alpha` (reg_alpha): L1 regularization (default: 0)

**Training Parameters:**
- `n_estimators`: Number of boosting rounds (typical: 100-1000)
- `objective`: Loss function ('binary:logistic', 'multi:softmax', 'reg:squarederror')
- `eval_metric`: Evaluation metric ('auc', 'logloss', 'rmse', 'mae')
- `early_stopping_rounds`: Stop if no improvement for N rounds

**Computational:**
- `tree_method`: Tree construction algorithm ('auto', 'exact', 'approx', 'hist', 'gpu_hist')
- `n_jobs` (nthread): Number of parallel threads (-1 for all cores)
- `random_state` (seed): Random seed for reproducibility

## Common Usage Examples

### 1. Scikit-learn API (Recommended)

```python
import xgboost as xgb
from sklearn.model_selection import train_test_split
import pandas as pd

# Load data
features = pd.read_parquet('results/features.parquet')
X = features.drop('target', axis=1)
y = features['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Binary classification
clf = xgb.XGBClassifier(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    min_child_weight=1,
    gamma=0,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0,
    reg_lambda=1,
    random_state=42,
    n_jobs=-1,
    tree_method='hist'
)

clf.fit(X_train, y_train)

# Predict
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)
```

### 2. Regression

```python
reg = xgb.XGBRegressor(
    n_estimators=100,
    learning_rate=0.05,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

reg.fit(X_train, y_train)
y_pred = reg.predict(X_test)
```

### 3. Cross-Validation with Early Stopping

```python
from sklearn.model_selection import cross_val_score

clf = xgb.XGBClassifier(
    n_estimators=1000,
    learning_rate=0.1,
    max_depth=5,
    early_stopping_rounds=10,
    random_state=42
)

# Fit with validation set for early stopping
clf.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=False
)

print(f"Best iteration: {clf.best_iteration}")
print(f"Best score: {clf.best_score}")
```

### 4. Native XGBoost API with DMatrix

```python
# Create DMatrix (optimized data structure)
dtrain = xgb.DMatrix(X_train, label=y_train)
dtest = xgb.DMatrix(X_test, label=y_test)

# Set parameters
params = {
    'max_depth': 5,
    'eta': 0.1,
    'objective': 'binary:logistic',
    'eval_metric': 'auc',
    'nthread': -1,
    'seed': 42
}

# Train with evaluation
evallist = [(dtrain, 'train'), (dtest, 'test')]
num_round = 100

bst = xgb.train(
    params,
    dtrain,
    num_round,
    evals=evallist,
    early_stopping_rounds=10,
    verbose_eval=10
)

# Predict
y_pred_proba = bst.predict(dtest)
```

### 5. Feature Importance

```python
import matplotlib.pyplot as plt

# Train model
clf.fit(X_train, y_train)

# Get feature importance
importance = clf.feature_importances_
feature_names = X.columns

# Plot top features
xgb.plot_importance(clf, max_num_features=20)
plt.savefig('results/bio-stats-ml-reporting/feature_importance.png')

# Get as DataFrame
importance_df = pd.DataFrame({
    'feature': feature_names,
    'importance': importance
}).sort_values('importance', ascending=False)
```

### 6. Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.3],
    'n_estimators': [100, 200, 500],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0]
}

xgb_model = xgb.XGBClassifier(random_state=42, n_jobs=-1)

grid_search = GridSearchCV(
    xgb_model,
    param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1,
    verbose=1
)

grid_search.fit(X_train, y_train)
print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")
```

### 7. Multi-class Classification

```python
clf_multi = xgb.XGBClassifier(
    objective='multi:softprob',
    num_class=3,  # Number of classes
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

clf_multi.fit(X_train, y_train)
y_pred = clf_multi.predict(X_test)
y_proba = clf_multi.predict_proba(X_test)
```

## Input/Output Formats

### Input Data Formats

**DMatrix accepts:**
- NumPy arrays
- Pandas DataFrames
- Scipy sparse matrices
- XGBoost binary buffer file (`.buffer`)

```python
# From DataFrame
dtrain = xgb.DMatrix(df, label=y)

# From NumPy
dtrain = xgb.DMatrix(X_array, label=y_array)

# From sparse matrix
from scipy.sparse import csr_matrix
X_sparse = csr_matrix(X)
dtrain = xgb.DMatrix(X_sparse, label=y)

# Save/load DMatrix
dtrain.save_binary('train.buffer')
dtrain = xgb.DMatrix('train.buffer')
```

### Model Persistence

```python
import joblib

# Save model (sklearn API)
joblib.dump(clf, 'results/bio-stats-ml-reporting/models/xgboost.joblib')
clf = joblib.load('results/bio-stats-ml-reporting/models/xgboost.joblib')

# Save booster (native API)
bst.save_model('results/bio-stats-ml-reporting/models/xgboost.json')
bst = xgb.Booster()
bst.load_model('results/bio-stats-ml-reporting/models/xgboost.json')
```

## Performance Tips

### 1. Use tree_method='hist' for Large Datasets

```python
# Histogram-based algorithm (faster, memory efficient)
clf = xgb.XGBClassifier(tree_method='hist', n_jobs=-1)

# GPU acceleration (if available)
clf = xgb.XGBClassifier(tree_method='gpu_hist', gpu_id=0)
```

### 2. Tune Learning Rate vs n_estimators

```python
# Lower learning rate with more estimators
clf = xgb.XGBClassifier(
    learning_rate=0.01,
    n_estimators=1000,
    early_stopping_rounds=50
)
```

### 3. Subsample to Prevent Overfitting

```python
clf = xgb.XGBClassifier(
    subsample=0.8,           # Row sampling
    colsample_bytree=0.8,    # Feature sampling per tree
    colsample_bylevel=0.8,   # Feature sampling per level
    colsample_bynode=0.8     # Feature sampling per split
)
```

### 4. Use Early Stopping

```python
clf.fit(
    X_train, y_train,
    eval_set=[(X_val, y_val)],
    early_stopping_rounds=10,
    verbose=False
)
```

### 5. Regularization to Control Complexity

```python
clf = xgb.XGBClassifier(
    reg_alpha=0.1,   # L1 regularization
    reg_lambda=1.0,  # L2 regularization
    gamma=0.1,       # Minimum loss reduction
    min_child_weight=3
)
```

### 6. Parallel Processing

```python
# Use all CPU cores
clf = xgb.XGBClassifier(n_jobs=-1)

# Specific number of threads
clf = xgb.XGBClassifier(n_jobs=4)
```

## Typical Workflow for Bio Stats

```python
#!/usr/bin/env python3
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# 1. Load features
features = pd.read_parquet('results/features.parquet')
X = features.drop(['sample_id', 'target'], axis=1)
y = features['target']

# 2. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Train XGBoost classifier
clf = xgb.XGBClassifier(
    n_estimators=500,
    learning_rate=0.05,
    max_depth=5,
    min_child_weight=1,
    gamma=0,
    subsample=0.8,
    colsample_bytree=0.8,
    reg_alpha=0.1,
    reg_lambda=1.0,
    random_state=42,
    n_jobs=-1,
    tree_method='hist',
    early_stopping_rounds=20
)

# 4. Fit with validation set
clf.fit(
    X_train, y_train,
    eval_set=[(X_test, y_test)],
    verbose=10
)

# 5. Cross-validation
cv_scores = cross_val_score(clf, X_train, y_train, cv=5, scoring='roc_auc')
print(f"CV AUC: {cv_scores.mean():.3f} (+/- {cv_scores.std():.3f})")

# 6. Test set evaluation
y_pred = clf.predict(X_test)
y_proba = clf.predict_proba(X_test)[:, 1]
test_auc = roc_auc_score(y_test, y_proba)
print(f"Test AUC: {test_auc:.3f}")

# 7. Feature importance
importance_df = pd.DataFrame({
    'feature': X.columns,
    'importance': clf.feature_importances_
}).sort_values('importance', ascending=False)

importance_df.to_csv(
    'results/bio-stats-ml-reporting/feature_importance.tsv',
    sep='\t',
    index=False
)

# 8. Save model
joblib.dump(clf, 'results/bio-stats-ml-reporting/models/xgboost_classifier.joblib')

# 9. Log metrics
metrics = {
    'model': 'XGBoost',
    'cv_auc_mean': cv_scores.mean(),
    'cv_auc_std': cv_scores.std(),
    'test_auc': test_auc,
    'best_iteration': clf.best_iteration
}

metrics_df = pd.DataFrame([metrics])
metrics_df.to_csv('results/bio-stats-ml-reporting/xgboost_metrics.tsv', sep='\t', index=False)
```

## Command-Line Interface

XGBoost also provides a CLI for training models:

```bash
# Train from config file
xgboost train.conf

# Example config (train.conf):
# data = "train.buffer"
# eval[test] = "test.buffer"
# max_depth = 5
# eta = 0.1
# objective = binary:logistic
# num_round = 100
```

## References

- Official Docs: https://xgboost.readthedocs.io/
- Python API: https://xgboost.readthedocs.io/en/stable/python/python_intro.html
- Parameters: https://xgboost.readthedocs.io/en/stable/parameter.html
- Tutorials: https://xgboost.readthedocs.io/en/stable/tutorials/index.html
