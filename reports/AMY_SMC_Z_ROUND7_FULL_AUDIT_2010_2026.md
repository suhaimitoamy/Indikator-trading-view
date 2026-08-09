# Amy SMC Z — Round 7 Full Audit 2010–2026

**Indicator:** `Amy-SMC-Z.pine` (logic copy of accepted Amy SMC Y Round 6; title/name only changed to Z before Round 7).
**Method:** closed-candle Python/Pine-logic evidence replay/audit; not TradingView Strategy Tester.
**Scoring:** 1 Mar 2010–31 Jul 2026. Jan–Feb 2010 warm-up. 2026 ends Jul.
**Split:** Train 2010–2018 · Validation 2019–2023 · Holdout 2024–2026.
**Decision rule:** keep the better profile; any new candidate that worsens validation/holdout is rolled back. Descriptive modules are judged by their actual lifecycle/function, not forced directional accuracy.

## 1. Predictive modules

| Module | TF | Train | Validation | Holdout | Full | Decision |
|---|---|---:|---:|---:|---:|---|
| Pattern | M5 | 74.51% (N=102) | 78.67% (N=75) | 85.00% (N=40) | 77.88% (N=217) | KEEP |
| Pattern | M15 | 59.52% | 64.25% | 66.22% | 62.33% (N=3504) | KEEP R6 |
| Pattern | H1 | 67.11% | 68.20% | 72.87% | 68.61% (N=924) | KEEP R6 |
| CHoCH predictive | M5 | 43.12% (N=436) | 46.05% (N=215) | 49.49% (N=99) | 44.80% (N=750) | KEEP inherited best |
| CHoCH predictive | M15 | 53.81% (N=197) | 60.38% (N=106) | 57.97% (N=69) | 56.45% (N=372) | KEEP inherited best |
| CHoCH predictive | H1 | 60.71% | 70.00% | 73.33% | 66.67% (N=63) | KEEP R6 |
| Valid Break | M5 | 45.03% (N=191) | 58.46% (N=65) | 55.56% (N=36) | 49.32% (N=292) | KEEP label only |
| Valid Break | M15 | 45.44% (N=559) | 48.73% (N=314) | 53.33% (N=150) | 47.61% (N=1023) | KEEP label only |
| Valid Break | H1 | 52.35% (N=170) | 56.82% (N=88) | 32.00% (N=50) | 50.32% (N=308) | KEEP label only |
| Sweep continuation | M5 | 85.44% (N=2061) | 88.06% (N=1173) | 87.01% (N=608) | 86.49% (N=3842) | **LOCK / KEEP** |
| Sweep continuation | M15 | 85.01% (N=694) | 85.50% (N=393) | 86.02% (N=186) | 85.31% (N=1273) | **LOCK / KEEP** |
| Sweep continuation | H1 | 85.22% (N=115) | 89.29% (N=84) | 92.31% (N=52) | 88.05% (N=251) | **LOCK / KEEP** |
| Internal-transition regime | M5 | 72.22% (N=4003) | 74.91% (N=2419) | 73.05% (N=1065) | 73.21% (N=7487) | **LOCK / KEEP** |
| Next Move → Target | M5 | 67.02% | 68.07% | 68.90% | 67.61% (23135W/11082L) | KEEP core |
| Next Move → Target | M15 | 68.18% | 67.24% | 67.31% | 67.78% (6161W/2929L) | KEEP core |
| Next Move → Target | H1 | 70.18% | 67.59% | 68.36% | 69.06% (1607W/720L) | KEEP core |

### Direction/context checks

| Module | TF | Train | Validation | Holdout | Full | Round 7 use |
|---|---|---:|---:|---:|---:|---|
| Final Bias → next swing | M5 | 53.18% (N=17895) | 53.42% (N=9657) | 53.50% (N=4974) | 53.30% (N=32526) | Context only; not standalone probability |
| Final Bias → next swing | M15 | 53.69% (N=5038) | 54.36% (N=2605) | 53.57% (N=1344) | 53.87% (N=8987) | Context only; not standalone probability |
| Final Bias → next swing | H1 | 53.85% (N=1168) | 53.30% (N=696) | 54.76% (N=378) | 53.84% (N=2242) | Context only; not standalone probability |
| Dealing Range → direction | M5 | 38.94% (N=1071) | 38.53% (N=641) | 38.99% (N=277) | 38.81% (N=1989) | **DESCRIPTIVE ONLY; no predictor promotion** |
| Dealing Range → direction | M15 | 42.70% (N=466) | 32.09% (N=296) | 32.94% (N=170) | 37.55% (N=932) | **DESCRIPTIVE ONLY; no predictor promotion** |
| Dealing Range → direction | H1 | 44.19% (N=86) | 23.91% (N=46) | 39.47% (N=38) | 37.65% (N=170) | **DESCRIPTIVE ONLY; no predictor promotion** |

## 2. Descriptive / functional modules

### Invalidation geometry

| TF | Train | Validation | Holdout | Full | Decision |
|---|---:|---:|---:|---:|---|
| M5 | 100.00% | 100.00% | 100.00% | 100.00% | **LOCK / KEEP** |
| M15 | 100.00% | 100.00% | 100.00% | 100.00% | **LOCK / KEEP** |
| H1 | 100.00% | 100.00% | 100.00% | 100.00% | **LOCK / KEEP** |

### Liquidity levels: eventually taken

| Level | TF | Train | Validation | Holdout | Full | Decision |
|---|---|---:|---:|---:|---:|---|
| EQH | M5 | 76.79% (N=4636) | 77.84% (N=2468) | 78.83% (N=1285) | 77.41% (N=8389) | **KEEP** |
| EQH | M15 | 78.24% (N=1599) | 81.30% (N=845) | 83.22% (N=435) | 79.89% (N=2879) | **KEEP** |
| EQH | H1 | 80.86% (N=350) | 86.13% (N=173) | 87.78% (N=90) | 83.36% (N=613) | **KEEP** |
| EQL | M5 | 75.59% (N=4208) | 78.12% (N=2285) | 77.43% (N=1143) | 76.62% (N=7636) | **KEEP** |
| EQL | M15 | 78.07% (N=1482) | 78.60% (N=785) | 78.36% (N=342) | 78.27% (N=2609) | **KEEP** |
| EQL | H1 | 78.88% (N=303) | 82.72% (N=162) | 75.34% (N=73) | 79.55% (N=538) | **KEEP** |

### M15 area lifecycle

| Component | Train | Validation | Holdout | Full | Decision |
|---|---:|---:|---:|---:|---|
| FVG full fill | 98.53% (N=14392) | 98.51% (N=7999) | 97.06% (N=5206) | 98.25% (N=27597) | **LOCK / KEEP** |
| Internal OB mitigation | 97.16% (N=11096) | 98.00% (N=6046) | 94.00% (N=3099) | 96.93% (N=20241) | **LOCK / KEEP** |
| Swing OB mitigation | 92.89% (N=1532) | 93.20% (N=823) | 80.52% (N=426) | 91.08% (N=2781) | **LOCK / KEEP** |

### Previous period liquidity (M15): at least one side taken

| Level | Train | Validation | Holdout | Full | Decision |
|---|---:|---:|---:|---:|---|
| Previous Daily H/L | 80.60% (N=2752) | 80.67% (N=1552) | 79.93% (N=837) | 80.51% (N=5141) | KEEP |
| Previous Weekly H/L | 88.53% (N=462) | 84.23% (N=260) | 88.89% (N=135) | 87.28% (N=857) | KEEP |
| Previous Monthly H/L | 83.96% (N=106) | 88.33% (N=60) | 70.97% (N=31) | 83.25% (N=197) | KEEP, holdout sample small |

### OTE / Fibonacci

| Module | TF | Train | Validation | Holdout | Full | Round 7 interpretation |
|---|---|---:|---:|---:|---:|---|
| Fib 1.272 hit | M5 | 69.92% (N=1775) | 68.26% (N=983) | 71.34% (N=506) | 69.64% (N=3264) | Target reference; not universal 70% predictor |
| Fib 1.272 hit | M15 | 72.17% (N=557) | 65.19% (N=362) | 73.91% (N=184) | 70.17% (N=1103) | Target reference; not universal 70% predictor |
| Fib 1.272 hit | H1 | 72.66% (N=139) | 61.11% (N=72) | 60.47% (N=43) | 67.32% (N=254) | Target reference; not universal 70% predictor |
| OTE touch → 1.272 | M5 | 29.40% (N=1034) | 27.24% (N=580) | 30.00% (N=290) | 28.83% (N=1904) | Entry-location context only; weak standalone prediction |
| OTE touch → 1.272 | M15 | 31.53% (N=295) | 25.40% (N=189) | 39.36% (N=94) | 30.80% (N=578) | Entry-location context only; weak standalone prediction |
| OTE touch → 1.272 | H1 | 23.08% (N=65) | 24.32% (N=37) | 13.04% (N=23) | 21.60% (N=125) | Entry-location context only; weak standalone prediction |

## 3. End-to-end consistency

- `Next Move` remains binary: **UP/DOWN only**.
- `Target` remains available through structural candidate or projected fallback; no normal `NO TARGET` state.
- Target side and invalidation side are selected from the **actual Next Move direction**, preventing a directional override from pairing with the wrong-side invalidation.
- Projected fallback is forced outside the signal candle; target construction does not require a future candle.
- Dealing Range, Pattern, CHoCH and Valid Break remain independent evidence layers unless an override was already accepted by prior split testing; Round 7 does not double-count weak evidence into Final Bias.

## 4. Round 7 decisions

- KEEP Pattern M5 Round5 profile.
- KEEP Pattern M15/H1 Round6 liquidity-conflict profiles; both improved train, validation, holdout.
- KEEP H1 CHoCH Round6 cap; M5/M15 CHoCH remain inherited best-of and are not promoted further.
- KEEP inverse-sweep continuation predictor on M5/M15/H1.
- KEEP M5 internal-transition override.
- KEEP Next Move/Target core from Round5; Round7 found no evidence requiring rollback.
- KEEP invalidation, EQH/EQL, FVG/OB lifecycle, D/W/M levels as functional/descriptive modules.
- Dealing Range remains descriptive only; do not feed it into Final Bias/Next Move.
- Valid Break remains independent confirmation/label only; do not use as Next Move override.
- OTE remains visualization/entry-location context, not a high-confidence predictor on full history.
- Fib 1.272 remains a target reference; 1.618/2.000 should not be interpreted as comparable-probability targets.
- Confidence remains a heuristic score, not a calibrated probability; no Round7 confidence rewrite accepted.
- No Amy-SMC-Z logic patch accepted in Round7 baseline audit; preserving Z avoids regression.

## 5. Round 7 code decision

**No new Amy-SMC-Z logic patch is accepted in this baseline full audit.** This is intentional: the standing best-of rule forbids changing a retained profile merely because another component is weak. Weak modules remain descriptive/independent until a candidate beats the current baseline in train, validation, and holdout. Therefore Amy SMC Z stays identical to the Round 6 baseline logic at the end of this audit.

### Important interpretation

These percentages are structural/event lifecycle statistics, not account-level trading win rate. Overlapping modules must not be averaged into one artificial 'overall accuracy'.