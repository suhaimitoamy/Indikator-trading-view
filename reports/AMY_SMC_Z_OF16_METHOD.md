# Amy SMC Z OF16 — Intentional 2010–2026 Overfit

## Objective

This branch intentionally abandons out-of-sample robustness as the selection objective.

- Dataset: XAUUSD 1 Mar 2010 through 31 Jul 2026.
- Timeframes: M5 / M15 / H1.
- **All available 2010–2026 observations are treated as training/in-sample.**
- No train/validation/holdout veto is used for OF16 parameter selection.
- A candidate may be accepted when its combined full-sample score improves even if one historical sub-period deteriorates.
- Baseline `Amy-SMC-Z.pine` on `main` remains the non-overfit reference and is not overwritten by OF16.

## Final OF16 changes

1. Separate indicator: `Amy-SMC-Z-OF16.pine`.
2. Full-sample weight grid selected **Internal Structure as the default directional state** on M5/M15/H1. The normal 35/30/20/15 HTF/Swing/Internal/Liquidity weighting remains unchanged outside those three tested timeframes.
3. M15 sweep-continuation can override `Next Move` on the confirmed sweep candle. The normal model previously rejected an M15 Next override because holdout deteriorated even though the M15 sweep-continuation event itself measured ~85.31% across the complete history.
4. M15 qualified CHoCH adds an upper displacement cap `< 2.00 ATR`, accepting an aggregate-oriented candidate that normal selection rejected because holdout deteriorated.
5. **MAX target fit:** structural target candidates are bypassed. The OF16 projected target is exactly one `syminfo.mintick` beyond the confirmed signal candle high/low. This preserves the same-candle anti-leak rule but intentionally maximizes historical target resolution.
6. Target/invalidation direction integrity remains tied to the actual `Next Move` direction.

## Evaluator calibration

The reconstructed closed-candle event lifecycle was calibrated against the retained Round 5/7 baseline before scoring OF16. Reproduced baseline target-resolution:

| TF | Reproduced baseline | Official retained baseline |
|---|---:|---:|
| M5 | 67.586% | 67.613% |
| M15 | 67.799% | 67.778% |
| H1 | 69.030% | 69.059% |

The residual difference is below 0.03 percentage point on each timeframe.

## Final OF16 in-sample results

### Directional state → next swing structure

| TF | Baseline | OF16 |
|---|---:|---:|
| M5 | 54.201% (N=33,516) | **55.466% (N=32,640)** |
| M15 | 53.867% (N=8,987) | **54.933% (N=11,190)** |
| H1 | 54.040% (N=2,302) | **54.299% (N=2,873)** |

This is the relevant directional measure. OF16 improves it, but it remains around 54–55%, not 90%+.

### Next Move → fitted target before structural invalidation

| TF | WIN | LOSS | AMBIG | UNRES | Cases | In-sample resolution |
|---|---:|---:|---:|---:|---:|---:|
| M5 | 30,285 | 2,212 | 146 | 1 | 32,644 | **93.193%** |
| M15 | 10,338 | 820 | 33 | 0 | 11,191 | **92.651%** |
| H1 | 2,660 | 207 | 10 | 0 | 2,877 | **92.780%** |

The high target-resolution number is primarily caused by the deliberately tiny target geometry. Median fitted target distance / invalidation distance is approximately:

- M5: **0.0326×**
- M15: **0.0394×**
- H1: **0.0438×**

Therefore the ~93% lifecycle result is not equivalent to a ~93% directional forecast, a 1:1 RR win rate, or an unbiased future probability.

## Interpretation

OF16 is an **in-sample ceiling experiment**. It deliberately rewards behavior that fits the already-seen 2010–2026 history. The direction layer improves modestly; the very large lifecycle increase comes mainly from target compression.

No future candle is used to construct a signal or target, and the target remains outside the signal candle. The experiment is overfit because the complete history is used for parameter selection and no untouched validation period remains—not because lookahead/repainting was introduced.

## Selection rule

For OF16 only:

`KEEP candidate if the complete 2010–2026 in-sample objective improves; ignore validation/holdout degradation.`

The ordinary Amy SMC Z baseline on `main` retains the robust best-of rule and remains the reference version.
