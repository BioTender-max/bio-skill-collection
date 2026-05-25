#!/usr/bin/env python3
"""
Biomarker Signature Studio

End-to-end biomarker discovery workflow that combines feature-selection ensembles,
nested cross-validation, explainability, and optional survival validation.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.base import clone
from sklearn.ensemble import RandomForestClassifier
from sklearn.exceptions import ConvergenceWarning
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    roc_auc_score,
)
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.utils import check_random_state

try:
    from boruta import BorutaPy
except ImportError:  # pragma: no cover - optional dependency
    BorutaPy = None  # type: ignore

try:
    from mrmr import mrmr_classif
except ImportError:  # pragma: no cover
    mrmr_classif = None  # type: ignore

try:
    from xgboost import XGBClassifier
except ImportError:  # pragma: no cover
    XGBClassifier = None  # type: ignore

try:
    import shap  # type: ignore
except ImportError:  # pragma: no cover
    shap = None  # type: ignore

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    yaml = None  # type: ignore

try:
    from lifelines import CoxPHFitter  # type: ignore
except ImportError:  # pragma: no cover
    CoxPHFitter = None  # type: ignore


@dataclass
class SkillConfig:
    expression: Path
    metadata: Path
    label_column: str
    id_column: str = "sample_id"
    feature_list: Optional[Path] = None
    output_dir: Path = Path("biomarker_outputs")
    selectors: Tuple[str, ...] = ("boruta", "lasso", "mrmr", "mi_topk")
    models: Tuple[str, ...] = ("logit", "rf", "xgb")
    k_features: int = 75
    nested_folds: int = 5
    inner_folds: int = 3
    test_size: float = 0.2
    random_state: int = 42
    survival: bool = False
    shap_sample_size: int = 500
    max_features: int = 250
    min_features: int = 5
    bootstraps: int = 200
    strata_column: Optional[str] = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Biomarker Signature Studio")
    parser.add_argument("--config", type=Path, help="Optional YAML/JSON config file")
    parser.add_argument("--expression", type=Path, help="Expression matrix CSV/TSV")
    parser.add_argument("--metadata", type=Path, help="Metadata CSV/TSV")
    parser.add_argument("--label-column", dest="label_column", help="Label column name")
    parser.add_argument("--id-column", dest="id_column", default="sample_id")
    parser.add_argument("--feature-list", dest="feature_list", type=Path)
    parser.add_argument("--output-dir", dest="output_dir", type=Path)
    parser.add_argument("--selectors", help="Comma-separated selectors")
    parser.add_argument("--models", help="Comma-separated models")
    parser.add_argument("--k-features", dest="k_features", type=int)
    parser.add_argument("--nested-folds", dest="nested_folds", type=int)
    parser.add_argument("--inner-folds", dest="inner_folds", type=int)
    parser.add_argument("--test-size", dest="test_size", type=float)
    parser.add_argument("--random-state", dest="random_state", type=int)
    parser.add_argument("--survival", action="store_true")
    parser.add_argument("--shap-sample-size", dest="shap_sample_size", type=int)
    parser.add_argument("--max-features", dest="max_features", type=int)
    parser.add_argument("--min-features", dest="min_features", type=int)
    parser.add_argument("--bootstraps", dest="bootstraps", type=int)
    parser.add_argument("--strata-column", dest="strata_column")
    return parser.parse_args()


def load_config(ns: argparse.Namespace) -> SkillConfig:
    cfg: Dict[str, Any] = {}
    if ns.config:
        if not ns.config.exists():
            raise FileNotFoundError(f"Config file {ns.config} not found.")
        if ns.config.suffix.lower() in {".yaml", ".yml"}:
            if yaml is None:
                raise RuntimeError("PyYAML is required to read YAML configs.")
            cfg = yaml.safe_load(ns.config.read_text())
        else:
            cfg = json.loads(ns.config.read_text())
    attrs = {k: getattr(ns, k) for k in vars(ns) if getattr(ns, k) not in (None, False)}
    cfg.update({k: v for k, v in attrs.items() if k != "config"})

    required = ["expression", "metadata", "label_column"]
    for field in required:
        if field not in cfg:
            raise ValueError(f"Missing required parameter '{field}'.")

    # Normalize selectors/models to tuples
    for key in ("selectors", "models"):
        if key in cfg and isinstance(cfg[key], str):
            cfg[key] = tuple(part.strip() for part in cfg[key].split(",") if part.strip())

    # Cast paths
    for path_key in ("expression", "metadata", "feature_list", "output_dir"):
        if path_key in cfg and cfg[path_key] is not None:
            cfg[path_key] = Path(cfg[path_key])

    return SkillConfig(**cfg)  # type: ignore[arg-type]


def read_table(path: Path) -> pd.DataFrame:
    if path.suffix.lower() in {".tsv", ".txt"}:
        return pd.read_csv(path, sep="\t", index_col=0)
    return pd.read_csv(path, index_col=0)


def align_inputs(
    expression_path: Path,
    metadata_path: Path,
    label_column: str,
    id_column: str,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    expr = read_table(expression_path)
    meta = read_table(metadata_path)
    if id_column not in meta.columns:
        raise KeyError(f"Metadata missing id_column '{id_column}'.")
    if label_column not in meta.columns:
        raise KeyError(f"Metadata missing label column '{label_column}'.")

    # If metadata ids match columns instead of index, transpose
    meta_ids = meta[id_column].astype(str)
    expr_index = expr.index.astype(str)
    expr_cols = expr.columns.astype(str)

    if not set(meta_ids).intersection(expr_index) and set(meta_ids).intersection(expr_cols):
        expr = expr.T
        expr_index = expr.index.astype(str)

    expr = expr.loc[~expr.index.duplicated()].copy()
    meta = meta.set_index(id_column)

    common = meta.index.intersection(expr.index)
    if common.empty:
        raise ValueError("No overlapping sample IDs between metadata and expression.")

    meta = meta.loc[common]
    expr = expr.loc[common]

    return expr, meta


def filter_features(
    X: pd.DataFrame,
    feature_list: Optional[Path],
) -> pd.DataFrame:
    if not feature_list:
        return X
    genes = [line.strip() for line in feature_list.read_text().splitlines() if line.strip()]
    keep = [g for g in genes if g in X.columns]
    if not keep:
        raise ValueError("Feature list provided but no genes matched matrix columns.")
    return X[keep]


def select_boruta(
    X: np.ndarray,
    y: np.ndarray,
    feature_names: List[str],
    random_state: int,
) -> Tuple[List[str], pd.DataFrame]:
    if BorutaPy is None:
        raise RuntimeError("boruta is not installed. pip install boruta.")
    rf = RandomForestClassifier(
        n_estimators=100,
        max_depth=5,
        n_jobs=-1,
        random_state=random_state,
    )
    selector = BorutaPy(rf, n_estimators="auto", random_state=random_state, verbose=0)
    selector.fit(X, y)
    support = selector.support_
    ranks = selector.ranking_
    selected = [name for name, keep in zip(feature_names, support) if keep]
    ranking_df = pd.DataFrame(
        {
            "feature": feature_names,
            "selector": "boruta",
            "rank": ranks,
            "selected": support,
        }
    ).sort_values("rank")
    return selected, ranking_df


def select_lasso_stability(
    X: np.ndarray,
    y: np.ndarray,
    feature_names: List[str],
    bootstraps: int,
    random_state: int,
) -> Tuple[List[str], pd.DataFrame]:
    rng = check_random_state(random_state)
    counts = np.zeros(len(feature_names), dtype=float)
    for i in range(bootstraps):
        idx = rng.choice(len(y), size=len(y), replace=True)
        model = LogisticRegression(penalty="l1", solver="saga", C=0.5, max_iter=2000)
        with warnings_suppressed():
            model.fit(X[idx], y[idx])
        counts += (model.coef_[0] != 0).astype(float)
    freqs = counts / bootstraps
    selected = [f for f, freq in zip(feature_names, freqs) if freq >= 0.6]
    df = pd.DataFrame(
        {
            "feature": feature_names,
            "selector": "lasso",
            "stability": freqs,
            "selected": freqs >= 0.6,
        }
    ).sort_values("stability", ascending=False)
    return selected, df


def select_mrmr(
    X_df: pd.DataFrame,
    y: np.ndarray,
    k_features: int,
) -> Tuple[List[str], pd.DataFrame]:
    if mrmr_classif is None:
        raise RuntimeError("mrmr not installed. pip install pymrmr or mrmr-selection.")
    selected = mrmr_classif(X=X_df, y=pd.Series(y), K=min(k_features, X_df.shape[1]))
    df = pd.DataFrame(
        {"feature": selected, "selector": "mrmr", "rank": range(1, len(selected) + 1)}
    )
    return selected, df


def select_mi_topk(
    X: np.ndarray,
    y: np.ndarray,
    feature_names: List[str],
    k_features: int,
) -> Tuple[List[str], pd.DataFrame]:
    scores = mutual_info_classif(X, y, random_state=0)
    order = np.argsort(scores)[::-1]
    top_idx = order[: min(k_features, len(order))]
    selected = [feature_names[i] for i in top_idx]
    df = pd.DataFrame(
        {
            "feature": [feature_names[i] for i in order],
            "selector": "mi_topk",
            "score": scores[order],
        }
    )
    return selected, df


def ensure_bounds(features: List[str], min_features: int, max_features: int) -> List[str]:
    if len(features) < min_features:
        raise ValueError(
            f"Selector returned {len(features)} features (<{min_features}). "
            "Adjust thresholds or provide more samples."
        )
    if len(features) > max_features:
        return features[:max_features]
    return features


def build_model(model_name: str, random_state: int):
    if model_name == "logit":
        return LogisticRegression(penalty="l2", solver="saga", max_iter=5000)
    if model_name == "rf":
        return RandomForestClassifier(n_estimators=300, random_state=random_state, n_jobs=-1)
    if model_name == "xgb":
        if XGBClassifier is None:
            raise RuntimeError("xgboost not installed.")
        return XGBClassifier(
            objective="binary:logistic",
            eval_metric="logloss",
            random_state=random_state,
            n_estimators=500,
            n_jobs=-1,
        )
    raise ValueError(f"Unknown model '{model_name}'.")


def model_param_grid(model_name: str) -> Dict[str, List[Any]]:
    if model_name == "logit":
        return {"C": [0.01, 0.1, 1.0, 5.0], "penalty": ["l1", "l2"]}
    if model_name == "rf":
        return {"max_depth": [None, 5, 8], "min_samples_leaf": [1, 5, 10]}
    if model_name == "xgb":
        return {
            "max_depth": [3, 5, 7],
            "subsample": [0.7, 0.9, 1.0],
            "colsample_bytree": [0.5, 0.8, 1.0],
        }
    raise ValueError(f"Unknown model '{model_name}'.")


def nested_cv_train(
    X: np.ndarray,
    y: np.ndarray,
    model_name: str,
    outer_folds: int,
    inner_folds: int,
    random_state: int,
) -> Tuple[float, float, Dict[str, Any], Any]:
    outer = StratifiedKFold(n_splits=outer_folds, shuffle=True, random_state=random_state)
    scores: List[float] = []
    aps: List[float] = []
    best_params_list: List[Dict[str, Any]] = []
    best_estimator = None

    for fold_idx, (train_idx, val_idx) in enumerate(outer.split(X, y), start=1):
        base_model = build_model(model_name, random_state + fold_idx)
        grid = GridSearchCV(
            estimator=base_model,
            param_grid=model_param_grid(model_name),
            cv=inner_folds,
            scoring="roc_auc",
            n_jobs=-1,
        )
        with warnings_suppressed():
            grid.fit(X[train_idx], y[train_idx])
        best_model = grid.best_estimator_
        probas = best_model.predict_proba(X[val_idx])[:, 1]
        scores.append(roc_auc_score(y[val_idx], probas))
        aps.append(average_precision_score(y[val_idx], probas))
        best_params_list.append(grid.best_params_)
        best_estimator = best_model

    summary = {
        "auc_mean": float(np.mean(scores)),
        "auc_std": float(np.std(scores)),
        "ap_mean": float(np.mean(aps)),
        "ap_std": float(np.std(aps)),
        "best_params": best_params_list,
    }
    return summary["auc_mean"], summary["ap_mean"], summary, best_estimator


def evaluate_holdout(
    model,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    y_test: np.ndarray,
) -> Dict[str, Any]:
    model.fit(X_train, y_train)
    probas = model.predict_proba(X_test)[:, 1]
    preds = (probas >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_test, preds).ravel()
    return {
        "test_auc": float(roc_auc_score(y_test, probas)),
        "test_ap": float(average_precision_score(y_test, probas)),
        "test_accuracy": float(accuracy_score(y_test, preds)),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


def compute_shap(
    model,
    X: np.ndarray,
    feature_names: List[str],
    sample_size: int,
) -> Optional[pd.DataFrame]:
    if shap is None:
        return None
    sampler = min(sample_size, X.shape[0])
    background = X[np.random.choice(X.shape[0], sampler, replace=False)]
    try:
        if isinstance(model, RandomForestClassifier) or model.__class__.__name__.startswith("XGB"):
            explainer = shap.TreeExplainer(model)
        else:
            explainer = shap.LinearExplainer(model, background)
        shap_values = explainer.shap_values(background)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        shap_abs = np.abs(shap_values).mean(axis=0)
        df = pd.DataFrame(
            {"feature": feature_names, "mean_abs_shap": shap_abs}
        ).sort_values("mean_abs_shap", ascending=False)
        return df
    except Exception:  # pragma: no cover - shap edge cases
        return None


def run_survival(
    X_df: pd.DataFrame,
    meta: pd.DataFrame,
    features: List[str],
) -> Optional[Dict[str, Any]]:
    if CoxPHFitter is None:
        return None
    required = {"time_to_event", "event"}
    if not required.issubset(meta.columns):
        return None
    data = meta[list(required)].copy()
    for feature in features:
        data[feature] = X_df[feature]
    cox = CoxPHFitter()
    try:
        cox.fit(data, duration_col="time_to_event", event_col="event")
    except Exception:
        return None
    summary = cox.summary[["coef", "exp(coef)", "p"]].reset_index().rename(
        columns={"index": "feature", "exp(coef)": "hazard_ratio", "p": "p_value"}
    )
    return {
        "concordance": float(cox.concordance_index_),
        "top_features": summary.to_dict(orient="records")[: min(len(features), 15)],
    }


class warnings_suppressed:
    """Context manager to silence convergence warnings for cleaner logs."""

    def __enter__(self):
        import warnings

        warnings.filterwarnings("ignore", category=ConvergenceWarning)
        warnings.filterwarnings("ignore", category=UserWarning)

    def __exit__(self, exc_type, exc_val, exc_tb):
        import warnings

        warnings.resetwarnings()
        return False


def main() -> int:
    ns = parse_args()
    cfg = load_config(ns)
    output_dir = cfg.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    expr_df, meta_df = align_inputs(cfg.expression, cfg.metadata, cfg.label_column, cfg.id_column)
    y_series = meta_df[cfg.label_column]
    expr_df = filter_features(expr_df, cfg.feature_list)

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y_series)
    if len(label_encoder.classes_) != 2:
        raise ValueError("Current implementation supports binary classification only.")

    label_balance = y_series.value_counts().to_dict()
    y_array = y_encoded.astype(int)
    X_array = expr_df.values.astype(float)
    feature_names = expr_df.columns.tolist()

    if cfg.strata_column and cfg.strata_column in meta_df.columns:
        strata = (
            meta_df[cfg.strata_column].astype(str) + "__" + y_series.astype(str)
        ).values
    else:
        strata = y_array

    X_train, X_test, y_train, y_test = train_test_split(
        X_array,
        y_array,
        test_size=cfg.test_size,
        stratify=strata,
        random_state=cfg.random_state,
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    selectors_output: Dict[str, Any] = {}
    feature_tables: List[pd.DataFrame] = []

    selector_funcs = {
        "boruta": lambda: select_boruta(X_train, y_train, feature_names, cfg.random_state),
        "lasso": lambda: select_lasso_stability(
            X_train, y_train, feature_names, cfg.bootstraps, cfg.random_state
        ),
        "mrmr": lambda: select_mrmr(
            pd.DataFrame(X_train, columns=feature_names), y_train, cfg.k_features
        ),
        "mi_topk": lambda: select_mi_topk(X_train, y_train, feature_names, cfg.k_features),
    }

    for selector_name in cfg.selectors:
        if selector_name not in selector_funcs:
            raise ValueError(f"Unknown selector '{selector_name}'.")
        selected, table = selector_funcs[selector_name]()
        selected = ensure_bounds(selected, cfg.min_features, cfg.max_features)
        selectors_output[selector_name] = {
            "n_features": len(selected),
            "features": selected,
        }
        feature_tables.append(table.assign(selector_name=selector_name))

    concatenated = pd.concat(feature_tables, ignore_index=True, sort=False)
    concatenated.to_csv(output_dir / "selected_features.csv", index=False)

    results: Dict[str, Any] = {
        "label_balance": label_balance,
        "selectors": selectors_output,
        "models": {},
        "label_mapping": {int(i): cls for i, cls in enumerate(label_encoder.classes_)},
    }

    for selector_name, selector_info in selectors_output.items():
        cols = selector_info["features"]
        selector_idx = [feature_names.index(f) for f in cols]
        X_train_sel = X_train[:, selector_idx]
        X_test_sel = X_test[:, selector_idx]
        results["models"][selector_name] = {}

        for model_name in cfg.models:
            auc_mean, ap_mean, summary, best_estimator = nested_cv_train(
                X_train_sel,
                y_train,
                model_name,
                cfg.nested_folds,
                cfg.inner_folds,
                cfg.random_state,
            )
            holdout = evaluate_holdout(
                clone(best_estimator),
                X_train_sel,
                y_train,
                X_test_sel,
                y_test,
            )
            shap_df = compute_shap(best_estimator, X_train_sel, cols, cfg.shap_sample_size)
            shap_path = None
            if shap_df is not None:
                shap_path = output_dir / f"shap_{selector_name}_{model_name}.csv"
                shap_df.to_csv(shap_path, index=False)

            survival_stats = None
            if cfg.survival:
                survival_stats = run_survival(expr_df[cols], meta_df, cols)
                if survival_stats:
                    (output_dir / "survival").mkdir(exist_ok=True)
                    surv_file = output_dir / "survival" / f"{selector_name}_{model_name}.json"
                    surv_file.write_text(json.dumps(survival_stats, indent=2))

            results["models"][selector_name][model_name] = {
                "nested_cv": summary,
                "holdout": holdout,
                "shap_file": str(shap_path) if shap_path else None,
                "survival": survival_stats,
            }

    metrics_path = output_dir / "metrics.json"
    metrics_path.write_text(json.dumps(results, indent=2))
    (output_dir / "config_used.json").write_text(json.dumps(asdict(cfg), indent=2))
    print(f"[Biomarker Signature Studio] Finished. Metrics saved to {metrics_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
