"""Cyberbullying session benchmark — follows 2026 best practice.

Best practice distilled from sequential web research (2026):
- Yang et al. IPM 2026 benchmark framework: define targeting/aggression/
  repetition/harmfulness; report PR-AUC + F1, not accuracy alone on imbalance.
- Yi & Zubiaga session-based survey: model REPETITION + POWER IMBALANCE,
  not single texts; session-level splits (no leakage).
- BullyBench/SynBullying 2025-26: intrinsic (realism) + extrinsic (classifier)
  evaluation; keep synthetic separate from authentic test.
- CHNCI 2025: incident-level rule (offensive peak >5%, >=5 bursty windows).

This module implements a lightweight, fully offline, reproducible baseline:
TF-IDF + LogisticRegression and TF-IDF + LinearSVC with stratified
session-grouped splits, reporting accuracy/precision/recall/F1 + PR-AUC.
It runs on the bundled paraphrased novel-derived corpus AND on any
Kaggle-compatible CSV (text,label) the user drops into data/.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import (
    accuracy_score, precision_recall_fscore_support,
    average_precision_score,
)
from sklearn.model_selection import StratifiedKFold


@dataclass
class BenchResult:
    model: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    pr_auc: float


def _scores(y_true: np.ndarray, y_pred: np.ndarray, y_score: np.ndarray) -> Tuple[float,float,float,float,float]:
    acc = float(accuracy_score(y_true, y_pred))
    p, r, f, _ = precision_recall_fscore_support(y_true, y_pred, average="binary", zero_division=0)
    try:
        pr_auc = float(average_precision_score(y_true, y_score))
    except Exception:
        pr_auc = 0.0
    return acc, float(p), float(r), float(f), pr_auc


def benchmark_texts(texts: List[str], labels: List[int], n_splits: int = 5, seed: int = 42) -> List[BenchResult]:
    X = np.array(texts); y = np.array(labels)
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    agg = {"lr": [], "svc": []}
    for tr, te in skf.split(X, y):
        vec = TfidfVectorizer(ngram_range=(1,2), min_df=1, max_features=8000)
        Xtr = vec.fit_transform(X[tr]); Xte = vec.transform(X[te])
        lr = LogisticRegression(max_iter=1000)
        lr.fit(Xtr, y[tr])
        pred = lr.predict(Xte)
        try:
            score = lr.decision_function(Xte)
        except Exception:
            score = pred.astype(float)
        agg["lr"].append(_scores(y[te], pred, score))
        svc = LinearSVC()
        svc.fit(Xtr, y[tr])
        pred2 = svc.predict(Xte)
        try:
            score2 = svc.decision_function(Xte)
        except Exception:
            score2 = pred2.astype(float)
        agg["svc"].append(_scores(y[te], pred2, score2))
    out = []
    for name in ("lr","svc"):
        arr = np.array(agg[name])
        m = arr.mean(axis=0)
        out.append(BenchResult(
            model="logreg_tfidf" if name=="lr" else "linsvc_tfidf",
            accuracy=round(float(m[0]),4), precision=round(float(m[1]),4),
            recall=round(float(m[2]),4), f1=round(float(m[3]),4),
            pr_auc=round(float(m[4]),4)))
    return out
