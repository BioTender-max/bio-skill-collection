# Scikit-learn Usage Guide

**Official Documentation:** https://scikit-learn.org/stable/

**Version:** 1.8.0

## Installation

```bash
# Via pip
pip install scikit-learn

# Specific version
pip install scikit-learn==1.8.0

# With optional dependencies
pip install scikit-learn[alldeps]
```

## Key Modules for Stats/ML

### Classification
```python
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
```

### Regression
```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
```

### Model Selection & Validation
```python
from sklearn.model_selection import (
    train_test_split,
    cross_val_score,
    KFold,
    StratifiedKFold,
    GridSearchCV,
    RandomizedSearchCV
)
```

### Preprocessing & Feature Engineering
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.feature_selection import SelectKBest, RFE, SelectFromModel
from sklearn.pipeline import Pipeline
```

### Metrics
```python
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix, classification_report,
    mean_squared_error, mean_absolute_error, r2_score
)
```

## Common Usage Examples

### 1. Basic Classification Pipeline

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

# Load data
df = pd.read_parquet('results/features.parquet')
X = df.drop('target', axis=1)
y = df['target']

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_train_scaled, y_train)

# Evaluate
y_pred = model.predict(X_test_scaled)
print(classification_report(y_test, y_pred))
```

### 2. Cross-Validation with Multiple Models

```python
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

models = {
    'Logistic': LogisticRegression(max_iter=1000),
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM': SVC(kernel='rbf', random_state=42)
}

for name, model in models.items():
    scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='accuracy')
    print(f"{name}: {scores.mean():.3f} (+/- {scores.std():.3f})")
```

### 3. Pipeline with Feature Selection

```python
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectKBest, f_classif

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('feature_selection', SelectKBest(f_classif, k=20)),
    ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
])

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)
```

### 4. Hyperparameter Tuning

```python
from sklearn.model_selection import GridSearchCV

param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [5, 10, 15, None],
    'min_samples_split': [2, 5, 10]
}

rf = RandomForestClassifier(random_state=42)
grid_search = GridSearchCV(
    rf, param_grid, cv=5, scoring='f1', n_jobs=-1, verbose=1
)
grid_search.fit(X_train, y_train)

print(f"Best params: {grid_search.best_params_}")
print(f"Best score: {grid_search.best_score_:.3f}")

best_model = grid_search.best_estimator_
```

### 5. Stratified K-Fold Cross-Validation

```python
from sklearn.model_selection import StratifiedKFold, cross_validate

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

scoring = ['accuracy', 'precision', 'recall', 'f1', 'roc_auc']
cv_results = cross_validate(
    model, X, y, cv=skf, scoring=scoring, return_train_score=True, n_jobs=-1
)

for metric in scoring:
    train_scores = cv_results[f'train_{metric}']
    test_scores = cv_results[f'test_{metric}']
    print(f"{metric}:")
    print(f"  Train: {train_scores.mean():.3f} (+/- {train_scores.std():.3f})")
    print(f"  Test:  {test_scores.mean():.3f} (+/- {test_scores.std():.3f})")
```

### 6. Regression Pipeline

```python
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

# Train regressor
gbr = GradientBoostingRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42
)

gbr.fit(X_train_scaled, y_train)

# Evaluate
y_pred = gbr.predict(X_test_scaled)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print(f"RMSE: {rmse:.3f}")
print(f"R²: {r2:.3f}")
```

## Input/Output Formats

**Input Data Formats:**
- NumPy arrays (`np.ndarray`)
- Pandas DataFrames (`pd.DataFrame`)
- Scipy sparse matrices (`scipy.sparse`)
- List of lists (converted internally)

**Model Persistence:**
```python
import joblib

# Save model
joblib.dump(model, 'results/bio-stats-ml-reporting/models/classifier.joblib')

# Load model
loaded_model = joblib.load('results/bio-stats-ml-reporting/models/classifier.joblib')
```

## Performance Tips

### 1. Use n_jobs for Parallelization

```python
# Parallel cross-validation
cross_val_score(model, X, y, cv=5, n_jobs=-1)

# Parallel grid search
GridSearchCV(model, param_grid, cv=5, n_jobs=-1)

# Parallel ensemble methods
RandomForestClassifier(n_estimators=100, n_jobs=-1)
```

### 2. Handle Large Datasets

```python
# Use partial_fit for incremental learning
from sklearn.linear_model import SGDClassifier

sgd = SGDClassifier()
for batch in batches:
    sgd.partial_fit(batch_X, batch_y, classes=np.unique(y))
```

### 3. Feature Selection to Reduce Dimensionality

```python
# Remove low-variance features
from sklearn.feature_selection import VarianceThreshold

selector = VarianceThreshold(threshold=0.01)
X_reduced = selector.fit_transform(X)

# Select top k features
from sklearn.feature_selection import SelectKBest, mutual_info_classif

selector = SelectKBest(mutual_info_classif, k=50)
X_selected = selector.fit_transform(X, y)
```

### 4. Memory-Efficient Sparse Matrices

```python
from scipy.sparse import csr_matrix

# Convert dense to sparse for high-dimensional data
X_sparse = csr_matrix(X)
model.fit(X_sparse, y)
```

### 5. Set random_state for Reproducibility

```python
# Always set random_state for reproducible results
model = RandomForestClassifier(random_state=42)
train_test_split(X, y, random_state=42)
```

## Typical Workflow for Bioinformatics

```python
#!/usr/bin/env python3
import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import classification_report, roc_auc_score
import joblib

# 1. Load feature table from DuckDB export
features = pd.read_parquet('results/features.parquet')

# 2. Prepare data
X = features.drop(['sample_id', 'target'], axis=1)
y = features['target']

# 3. Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 4. Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Train baseline models
models = {
    'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
    'GradientBoosting': GradientBoostingClassifier(n_estimators=100, random_state=42)
}

results = []
for name, model in models.items():
    # Cross-validation
    cv_scores = cross_val_score(model, X_train_scaled, y_train, cv=5, scoring='roc_auc')

    # Train on full training set
    model.fit(X_train_scaled, y_train)

    # Test set evaluation
    y_pred = model.predict(X_test_scaled)
    y_proba = model.predict_proba(X_test_scaled)[:, 1]
    test_auc = roc_auc_score(y_test, y_proba)

    results.append({
        'model': name,
        'cv_auc_mean': cv_scores.mean(),
        'cv_auc_std': cv_scores.std(),
        'test_auc': test_auc
    })

    # Save model
    joblib.dump(model, f'results/bio-stats-ml-reporting/models/{name}.joblib')

# 6. Save metrics
metrics_df = pd.DataFrame(results)
metrics_df.to_csv('results/bio-stats-ml-reporting/metrics.tsv', sep='\t', index=False)
```

## References

- User Guide: https://scikit-learn.org/stable/user_guide.html
- API Reference: https://scikit-learn.org/stable/modules/classes.html
- Examples: https://scikit-learn.org/stable/auto_examples/
- Model Selection: https://scikit-learn.org/stable/model_selection.html
