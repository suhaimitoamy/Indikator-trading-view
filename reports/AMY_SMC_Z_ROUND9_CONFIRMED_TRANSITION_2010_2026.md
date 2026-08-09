# Amy SMC Z — Round 9 Confirmed Transition Backtest 2010–2026

**Indicator:** `Amy-SMC-Z.pine` on `main`  
**Implementation commit:** `3e5abe8878ac9420dc98e1a3c1927b07a7454bae`  
**Scoring:** 1 Mar 2010–31 Jul 2026; Jan–Feb 2010 warm-up  
**Timeframes:** M5, M15, H1  
**Method:** closed-candle Python/Pine-logic replay; not TradingView Strategy Tester  
**Splits:** Train 2010–2018 · Validation 2019–2023 · Holdout 2024–2026  
**Rule:** keep only improvements that survive the split checks; worse candidates roll back.

## Round 9 objective

Round 8 successfully made M5 selective using the Internal Transition regime. Round 9 tests whether the **entry bar itself** can distinguish stronger transitions without changing Target V1 geometry or using future candles.

The accepted gate requires all Round-8 Internal Transition conditions plus:

1. The entry candle must close in the new Internal Structure direction (`close > open` for bullish, `close < open` for bearish).
2. The protected structural invalidation must be at least **3.0 ATR** away from the entry close.
3. The decision is made only on the confirmed entry candle and then latched for the life of that transition regime.

Target V1 remains unchanged: projected fallback is still `max(0.40 × risk, 0.22 × ATR)` and remains outside the signal candle.

## M5 accepted result

### Directional precision → next swing structure

Using the same entry-state population for Round 8 and Round 9:

| Split | Round 8 | Round 9 | Delta | Round 9 signals |
|---|---:|---:|---:|---:|
| Train | 75.08% | **81.88%** | **+6.80 pp** | 414 |
| Validation | 77.27% | **84.65%** | **+7.37 pp** | 241 |
| Holdout | 75.94% | **82.54%** | **+6.60 pp** | 126 |
| Full | 75.92% | **82.84%** | **+6.92 pp** | 781 |

The previous Round-8 report used a slightly different state-transition counting population and printed 76.13% full directional precision; the apples-to-apples Round-9 evaluator reproduces the retained Round-8 entry population at 75.92%. The candidate comparison above uses exactly the same counting method on both versions.

### Target V1 lifecycle — target before structural invalidation

| Split | Round 8 | Round 9 | Delta | WIN | LOSS | AMBIG | Signals |
|---|---:|---:|---:|---:|---:|---:|---:|
| Train | 69.29% | **70.29%** | **+1.00 pp** | 291 | 123 | 0 | 414 |
| Validation | 70.02% | **71.25%** | **+1.23 pp** | 171 | 69 | 1 | 241 |
| Holdout | 71.32% | **73.81%** | **+2.49 pp** | 93 | 33 | 0 | 126 |
| Full | 69.84% | **71.15%** | **+1.31 pp** | 555 | 225 | 1 | 781 |

**Decision: KEEP.** Both directional precision and realistic Target V1 lifecycle improve in train, validation, holdout and full history.

Round-9 actionable regime occupies about **0.273% of M5 bars** (3,247 active bars), versus roughly 0.662% for the broader Round-8 transition regime. The gain therefore comes from stricter selection, not from shortening targets.

## Intermediate M5 candidate — candle confirmation only

Before applying the 3 ATR structural-room rule, requiring only candle-direction confirmation produced:

| Split | Directional | Target lifecycle | Signals |
|---|---:|---:|---:|
| Train | 76.34% | 69.83% | 727 |
| Validation | 78.92% | 71.93% | 427 |
| Holdout | 77.72% | 73.63% | 202 |
| Full | 77.36% | 71.06% | 1,356 |

This already beat Round 8. The 3 ATR rule was retained because it produced a much larger directional improvement while still improving Target V1 lifecycle in every split.

## Rejected M5 candidate — require Internal to be the component that just flipped

A stricter semantic candidate required the transition to be caused specifically by an Internal Structure flip while HTF, Swing and Liquidity were unchanged.

- Full Target lifecycle: **75.09%** on 546 cases.
- Full directional precision: only **69.05%**.
- Holdout directional precision: **65.85%**.

Although lifecycle improved, directional quality deteriorated materially relative to Round 8.

**Decision: ROLLBACK.** Round 9 does not sacrifice an already-good directional metric to improve only one statistic.

## M15 Round-9 confirmation candidate

Applying the same candle-confirmation concept to the retained M15 directional state produced Target V1 lifecycle:

| Split | Round-7/8 baseline | Candidate |
|---|---:|---:|
| Train | 68.18% | **68.34%** |
| Validation | 67.24% | **66.54%** |
| Holdout | 67.31% | **66.12%** |
| Full | 67.78% | **67.48%** |

**Decision: ROLLBACK.** Validation, holdout and full-history lifecycle worsened. M15 remains unchanged.

## H1 Round-9 confirmation candidate

| Split | Round-7/8 baseline | Candidate |
|---|---:|---:|
| Train | 70.18% | **69.88%** |
| Validation | 67.59% | **66.48%** |
| Holdout | 68.36% | **66.43%** |
| Full | 69.06% | **68.25%** |

**Decision: ROLLBACK.** The candidate worsened every split. H1 remains unchanged.

## Dashboard behavior after Round 9

### M5

- `TRADE • CONFIRMED` → Round-8 Internal Transition + candle direction confirmation + structural room `>= 3 ATR`; Next Move, Target, Invalidation and Confidence are active.
- `WATCH • SWEEP` → strong sweep-continuation context but not a target-backed trade.
- `WATCH • TRANSITION` → Internal Transition exists but failed the Round-9 confirmation/structural-room gate.
- `WAIT` → no accepted execution regime.

### M15 / H1

- `R8 BASELINE` → no Round-9 candidate survived the rollback rule, so prior accepted behavior is retained.

## Components kept unchanged

Round 9 does not rewrite Pattern, CHoCH/BOS, Valid Break, Dealing Range, FVG, Order Blocks, EQH/EQL, previous D/W/M levels, OTE/Fibonacci, invalidation geometry, sweep event logic or Target V1 geometry.

## Final Round 9 decision

- **KEEP:** M5 confirmed-transition execution gate.
- **KEEP:** Round-8 Internal Transition as the parent regime.
- **KEEP AS WATCH:** Sweep continuation and unconfirmed transition states.
- **ROLLBACK:** M5 internal-flip-cause-only candidate because directional quality fell.
- **ROLLBACK:** M15 candle-confirmation candidate.
- **ROLLBACK:** H1 candle-confirmation candidate.
- **KEEP:** all previously strong Round-7/8 modules and realistic target geometry.

Headline M5 Round-9 result: **82.84% directional precision** and **71.15% Target V1 lifecycle** on 781 accepted historical entries, with improvements in train, validation and holdout.
