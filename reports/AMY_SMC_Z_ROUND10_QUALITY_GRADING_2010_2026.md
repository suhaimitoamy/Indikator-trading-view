# Amy SMC Z — Round 10 Quality Grading Backtest 2010–2026

**Indicator:** `Amy-SMC-Z.pine` on `main`  
**Round-10 implementation commit:** `6057e4909bc1f338a6891d74696f781c60a51efb`  
**Scoring:** 1 Mar 2010–31 Jul 2026; Jan–Feb 2010 warm-up  
**Primary timeframe:** M5  
**Method:** closed-candle Python/Pine-logic replay against the audited/repaired XAUUSD archives; not TradingView Strategy Tester  
**Splits:** Train 2010–2018 · Validation 2019–2023 · Holdout 2024–2026  
**Rule:** keep the best accepted Round-9 core; a Round-10 candidate may replace it only if it does not degrade protected metrics.

## Objective

Round 9 already produced a strong selective M5 execution regime. Round 10 tests whether entry-bar quality can identify a higher-quality subgroup **without shortening Target V1 and without weakening the already-good Round-9 population**.

The search was performed on train first, then validation. The selected rule was locked before inspecting holdout.

## Replay calibration

The reconstructed event replay was checked against the accepted Round-9 report before Round-10 selection.

| Metric | Official Round 9 | Reproduced Round 9 |
|---|---:|---:|
| Full accepted entries | 781 | 767 |
| Full directional precision | 82.84% | 82.79% |
| Full Target V1 lifecycle | 71.15% | 71.71% |

The directional difference is about **0.05 pp** and lifecycle difference about **0.56 pp**. Signal-count difference is 14 entries (~1.8%). Round-10 candidate comparisons below use the same reconstructed evaluator for both baseline and candidate, so deltas remain apples-to-apples inside this round.

## Locked Round-10 A+ rule

A trade is graded **A+** only when the already-accepted Round-9 entry also has:

- Entry body `>= 0.50 ATR`.
- Entry body `< 2.50 ATR`.
- Body / candle range `>= 0.30`.
- Structural invalidation room remains `>= 3 ATR` from Round 9.
- Structural invalidation room is `< 8 ATR`.

No future candle is used. Target V1 is unchanged.

## Round-9 baseline on the calibrated evaluator

| Split | Entries | Directional | Target lifecycle |
|---|---:|---:|---:|
| Train | 405 | 81.48% | 70.62% |
| Validation | 239 | 84.94% | 71.97% |
| Holdout | 123 | 82.93% | 74.80% |
| Full | 767 | 82.79% | 71.71% |

## Round-10 A+ subgroup

| Split | A+ entries | Directional | Target lifecycle | WIN / LOSS |
|---|---:|---:|---:|---:|
| Train | 209 | **83.73%** | **73.68%** | 154 / 55 |
| Validation | 117 | **87.18%** | **75.21%** | 88 / 29 |
| Holdout | 58 | **82.76%** | **79.31%** | 46 / 12 |
| Full | 384 | **84.64%** | **75.00%** | 288 / 96 |

### What improved

Compared with the same-evaluator Round-9 population:

- Full directional: **82.79% → 84.64%** for A+.
- Full Target V1 lifecycle: **71.71% → 75.00%** for A+.
- Train lifecycle: **70.62% → 73.68%**.
- Validation lifecycle: **71.97% → 75.21%**.
- Holdout lifecycle: **74.80% → 79.31%**.

### Why A+ did not replace the Round-9 core

Holdout directional precision was **82.76%** for A+ versus **82.93%** for the full Round-9 baseline on the same evaluator. That difference corresponds to roughly one historical directional hit.

Under the standing best-of rule, a stricter Round-10 filter is **not allowed to discard the accepted Round-9 trades** when a protected holdout metric is lower, even if lifecycle improves strongly.

**Decision: ROLLBACK as a replacement filter. KEEP as a quality grade.**

## Implemented behavior

### M5

- `TRADE • A+` — accepted Round-9 Confirmed Transition and the Round-10 body/risk quality rule passes.
- `TRADE • A` — accepted Round-9 Confirmed Transition but not A+.
- `WATCH • SWEEP` — retained high-precision sweep context, not a target-backed trade.
- `WATCH • TRANSITION` — transition exists but does not pass the accepted Round-9 execution gate.
- `WAIT` — no accepted execution regime.

**A and A+ use the exact same Round-9 Next Move, Target V1, invalidation and confidence machinery.** Round 10 changes classification only; it does not delete an already-good A trade or manufacture a shorter target.

### M15 / H1

No Round-10 core change. Their previously accepted baselines remain untouched. Round 9 had already shown that simple confirmation gates worsened their validation/holdout lifecycle, so Round 10 does not retune them on the same history.

## Candidate-selection discipline

The A+ thresholds were selected from train and validation. Holdout was checked only after the rule was locked. When the holdout directional metric failed to exceed the protected Round-9 baseline, the replacement-filter idea was rejected instead of retuned on holdout.

## Final Round-10 decision

- **KEEP:** all Round-9 M5 execution signals.
- **ADD:** A+ quality grading for the cleaner historical subgroup.
- **KEEP:** A grade for every other already-valid Round-9 trade.
- **ROLLBACK:** using A+ as the only M5 trade filter.
- **KEEP:** Round-9 Target V1 geometry; no target compression.
- **KEEP:** M15/H1 and all strong descriptive modules unchanged.

Round 10 therefore improves the indicator's decision hierarchy without sacrificing an accepted signal family: the user can distinguish the historically cleaner **A+** setups, while the robust **A** baseline remains available.