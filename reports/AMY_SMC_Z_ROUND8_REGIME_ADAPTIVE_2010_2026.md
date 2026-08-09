# Amy SMC Z — Round 8 Regime-Adaptive Backtest 2010–2026

**Indicator:** `Amy-SMC-Z.pine` on `main`  
**Scoring:** 1 Mar 2010–31 Jul 2026; Jan–Feb 2010 warm-up  
**Timeframes:** M5, M15, H1  
**Method:** closed-candle Python/Pine-logic replay; not TradingView Strategy Tester  
**Splits:** Train 2010–2018 · Validation 2019–2023 · Holdout 2024–2026  
**Standing rule:** retain only robust improvement; weaker/fragile candidates roll back to Round 7.

## Round 8 objective

Round 8 changes the objective from “force a direction on every M5 candle” to “only issue an actionable M5 prediction when a regime has enough historical evidence.” Descriptive modules remain unchanged. Target V1 geometry also remains unchanged, so the result is not produced by shortening the target.

## Accepted M5 regime — Internal Transition

Definition:

- HTF bias is non-zero.
- HTF = Swing Structure = active Liquidity bias.
- Internal Structure has already flipped to the opposite side.
- Prediction follows Internal Structure only while this transition regime is active.
- Outside the regime M5 `Next Move = WAIT`, target/invalidation are blank.

### Directional precision → next swing structure

| Split | Signals | Accuracy |
|---|---:|---:|
| Train 2010–2018 | 901 | **75.36%** |
| Validation 2019–2023 | 554 | **77.44%** |
| Holdout 2024–2026 | 267 | **76.03%** |
| Full 2010–2026 | 1,722 | **76.13%** |

Actionable bar coverage is approximately **0.658%**. The purpose is selective precision, not maximum signal frequency.

### Target V1 lifecycle — target before structural invalidation

| Split | Round 7 | Round 8 | Delta | Round 8 cases |
|---|---:|---:|---:|---:|
| Train | 67.02% | **69.29%** | **+2.27 pp** | 891 |
| Validation | 68.07% | **70.02%** | **+1.94 pp** | 550 |
| Holdout | 68.90% | **71.32%** | **+2.42 pp** | 266 |
| Full | 67.61% | **69.84%** | **+2.23 pp** | 1,707 |

Full lifecycle detail: **1,188 WIN / 513 LOSS / 6 ambiguous / 0 unresolved**.

**Decision: KEEP.** The candidate improves train, validation, holdout and full-history lifecycle while maintaining >75% directional precision in every split.

## Sweep continuation — retained as WATCH, not M5 execution trigger

Sweep continuation remains one of the strongest directional event families from prior rounds (~86.49% M5 full-history event accuracy). Round 8 tested combining it with Internal Transition as an actionable M5 trigger.

| Split | Directional precision | Target V1 lifecycle |
|---|---:|---:|
| Train | 81.81% | 67.12% |
| Validation | 84.06% | 68.81% |
| Holdout | 82.66% | 68.92% |
| Full | **82.64%** | **67.93%** |

The combined trigger produces 4,677 directional episodes, but its target lifecycle is materially below the Internal-Transition-only candidate. Holdout improvement versus Round 7 is only ~+0.01 pp.

**Decision: keep Sweep as `WATCH • SWEEP`, not a target-backed M5 `TRADE` regime.** This preserves its strong directional information without pretending it has the same execution quality.

## M15 regime candidates

The strongest discovered M15 selective state was:

- Swing = Internal.
- HTF = Liquidity on the opposite side.

It scored:

| Split | Directional | N | Target lifecycle |
|---|---:|---:|---:|
| Train | 81.93% | 83 | 79.52% |
| Validation | 79.31% | 29 | 78.57% |
| Holdout | 100.00% | **8** | 75.00% |
| Full | 82.50% | 120 | 78.99% |

Despite the attractive percentages, the holdout contains only **8 signals**. That is too small to treat as a robust replacement after the OF16 overfitting experiment.

**Decision: ROLLBACK / DO NOT PROMOTE. M15 keeps Round 7.** The state can be revisited with genuinely new data rather than being tuned further on the same history.

## H1 regime candidates

No tested H1 selective gate improved the retained Round-7 target lifecycle across all splits. Example: H1 Sweep remained excellent directionally (**88.10% full**, 252 signals) but Target V1 lifecycle fell to **66.96% train / 63.10% validation / 73.58% holdout / 67.06% full**, versus Round-7 full lifecycle **69.06%**.

**Decision: ROLLBACK. H1 keeps Round 7**, including its previously accepted confirmed-sweep override.

## Round 8 dashboard behavior

### M5

- `TRADE • TRANSITION` → `Next Move = UP/DOWN`; Target, Invalidation and Confidence are available.
- `WATCH • SWEEP` → strong directional context only; `Next Move = WAIT`, no synthetic Target/Invalidation.
- `WAIT` → no validated execution regime; no forced prediction.

### M15 / H1

- `R7 BASELINE` → accepted Round-7 behavior remains unchanged because Round-8 candidates were either fragile or worse on lifecycle.

## Components intentionally unchanged

Pattern detector/promotion, CHoCH/BOS descriptive structure, Valid Break, Dealing Range, FVG, Order Blocks, EQH/EQL, previous D/W/M levels, OTE/Fibonacci and Round-7 target geometry are not rewritten by Round 8. The rule remains: a weak module is not allowed to contaminate a stronger predictor.

## Final Round 8 decision

- **ACCEPT:** M5 selective Internal-Transition execution regime.
- **KEEP AS WATCH:** M5 Sweep continuation.
- **ROLLBACK:** M15 rare high-accuracy regime due inadequate holdout sample.
- **ROLLBACK:** H1 regime-gating candidates because lifecycle robustness worsened.
- **KEEP:** Round-7 target geometry and all previously strong descriptive modules.

Round 8 therefore improves M5 quality by reducing coverage rather than manufacturing accuracy with a tiny target. The headline M5 actionable metrics are **76.13% directional precision** and **69.84% Target V1 lifecycle**, with both validation and holdout improvements over Round 7.
