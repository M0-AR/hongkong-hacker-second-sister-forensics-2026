# PAPER.md — Journal-ready draft (to be expanded to 8–10k words)

## Title
Verifying N: A Reproducible Forensic and NLP Benchmark Grounded in Chan Ho-Kei's *Second Sister*

## Authors
Independent reproducibility study · contact: repo issues

## Abstract
[See README Abstract — 250 words.]

## 1 Introduction
Hong Kong working-class precarity + hyperconnectivity; why fiction is a valid test-bed when treated as hypotheses, not evidence.

## 2 Background
2.1 Novel synopsis (own words, no verbatim). 2.2 Hong Kong social context (housing, MTR crowding, Occupy reverberations as depicted). 2.3 Threat model: False-Nephew, Rata/Siete split, predator subplot.

## 3 Related work
Full table from README §2 with DOIs. Emphasis: 2026 consensus that accuracy-alone is misleading on 100:1 imbalance; session > single-text; incident > comment.

## 4 Method
4.1 Forensic grammars (regexes, IP/MAC validation). 4.2 Benchmark protocol (stratified 5-fold, PR-AUC). 4.3 Stylometry + burst detectors. 4.4 Live anchor. 4.5 Ethics.

## 5 Results
Tables auto-generated from `results/*.json` — DO NOT hand-edit; re-run `make all`.
- Table 1: EXP-01 six gates (all PASS).
- Table 2: EXP-02 F1/PR-AUC (LogReg 0.800/0.928).
- Table 3: EXP-03 H1–H3.
- Table 4: Live snapshot + G-dollar volatility.

## 6 Discussion
What N gets right (headers, EXIF, session thinking) vs wrong (MAC identity, Stingray routine, revenge ethics). Negative results.

## 7 Limitations & threats to validity
n=27 demo; paraphrase gap; canonical fixtures; no human evaluation; translation effects untested.

## 8 Conclusion
Fiction verifiable where it narrows; dangerous where it identifies. Benchmark + harness released for PhD extension.

## References
- Full citations for all works in README §10 with URLs/DOIs.
- Data: Kaggle andrewmvd/cyberbullying-classification; sayankr007 multi-label; saurabhshahane dataset.
- Code: this repo, MIT.

## Appendix A: Search log
Sequential (one-at-a-time): websearch ×2 (novel analysis; benchmark best practice), duckduckgo (IP/Tor/EXIF), openresearch web (Stingray/MITM), paper-search unified (15 papers), kaggle search_everything, agent-reach web (reproducibility), gitmcp docs, hacker-news (0 hits), openalex (session survey). Fallback: DuckDuckGo Lite via webfetch (documented, not needed — no 429 encountered).

## Appendix B: Reproduction checklist
- [x] `make all` PASS on Python 3.12, sklearn 1.9, pandas 2.2
- [x] `docker compose config` valid; `research` service runs `make all`
- [x] `pytest -q` 4 passed
- [x] Live snapshot recorded with tool provenance
- [ ] Kaggle-scale rerun (future work — insert PR-AUC table when done)
