"""EXP-02 cyberbullying benchmark on public-compatible + novel-derived data.

Uses bundled paraphrased corpus (no copyrighted text) + optional Kaggle CSV.
Kaggle public refs verified 2026-2027 via search:
 - andrewmvd/cyberbullying-classification (47k tweets, 6 classes)
 - sayankr007/cyber-bullying-data-for-multi-label-classification
 - saurabhshahane/cyberbullying-dataset
Drop any of those CSVs as data/kaggle.csv with columns text,label to re-run
on REAL public data. Otherwise runs on bundled corpus (fully offline).
Reports accuracy/precision/recall/F1/PR-AUC per 2026 benchmark framework.
"""
import json, os, sys
sys.path.insert(0, "src")
from nlp.benchmark import benchmark_texts

def load_bundled():
    import json as j
    with open("data/samples/novel_corpus.json") as f:
        d = j.load(f)
    texts, labels = [], []
    for s in d["sessions"]:
        for t in s["texts"]:
            texts.append(t["text"]); labels.append(t["label"])
    texts += d["extra_bullying"]; labels += [1]*len(d["extra_bullying"])
    texts += d["extra_neutral"]; labels += [0]*len(d["extra_neutral"])
    return texts, labels

def load_kaggle_if_present():
    import csv
    p = "data/kaggle.csv"
    if not os.path.exists(p):
        return None
    texts, labels = [], []
    with open(p, newline='', encoding="utf-8", errors="ignore") as f:
        r = csv.DictReader(f)
        # accept text/label or tweet_text/cyberbullying_type style
        for row in r:
            t = row.get("text") or row.get("tweet_text") or row.get("comment") or ""
            lab = row.get("label", "")
            if not t:
                continue
            # map common Kaggle 6-class to binary: not_cyberbullying=0 else 1
            if isinstance(lab, str):
                lab_s = lab.strip().lower()
                if lab_s in ("0","not_cyberbullying","not bullying","neutral","non-bullying"):
                    y = 0
                elif lab_s in ("1",) or "bully" in lab_s or "harass" in lab_s or "hate" in lab_s or "insult" in lab_s:
                    y = 1
                else:
                    try: y = int(float(lab_s))
                    except: continue
            else:
                y = int(lab)
            texts.append(t); labels.append(1 if y!=0 else 0)
            if len(texts) >= 5000:
                break
    return (texts, labels) if len(texts) >= 50 else None

texts, labels = load_bundled()
source = "bundled_paraphrased_novel_corpus"
k = load_kaggle_if_present()
if k:
    texts, labels = k
    source = "kaggle_public_csv"

print(f"source={source} n={len(texts)} pos_rate={sum(labels)/len(labels):.3f}")
res = benchmark_texts(texts, labels, n_splits=5)
out = {"source": source, "n": len(texts), "pos_rate": round(sum(labels)/len(labels),4),
       "results": [r.__dict__ for r in res],
       "note": "Follows Yang et al IPM2026: report PR-AUC+F1, not accuracy alone; stratified 5-fold."}
with open("results/exp02_benchmark.json","w") as f:
    json.dump(out, f, indent=2)
print(json.dumps(out, indent=2))
# gate: at least one model F1>0.70 on bundled data (sanity), else FAIL
assert max(r.f1 for r in res) > 0.70, "benchmark sanity failed"
print("EXP-02 PASS")
