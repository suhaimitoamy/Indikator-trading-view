# Amy SMC Z OF16 — Intentional 2010–2026 Overfit

## Objective

This branch intentionally abandons out-of-sample robustness as the selection objective.

- Dataset: XAUUSD 1 Mar 2010 through 31 Jul 2026.
- M5 / M15 / H1.
- **All available 2010–2026 observations are treated as training/in-sample.**
- No train/validation/holdout veto is used for OF16 parameter selection.
- A candidate may be accepted when its combined full-sample score improves even if one historical sub-period deteriorates.
- Baseline `Amy-SMC-Z.pine` on `main` remains the non-overfit reference and must not be overwritten by OF16.

## Initial OF16 changes

1. Created separate indicator: `Amy-SMC-Z-OF16.pine`.
2. M15 sweep-continuation can override `Next Move` on the confirmed sweep candle. This was deliberately excluded from the normal model when robustness/holdout behavior was considered, despite the M15 sweep-continuation event having ~85.31% full-history event-layer accuracy.
3. M15 qualified CHoCH adds an upper displacement cap `< 2.00 ATR`, accepting the aggregate-oriented candidate that normal best-of selection rejected when holdout deteriorated.
4. OF16 target geometry is intentionally shorter:
   - projected target: `max(0.28 × invalidation distance, 0.16 × ATR)`;
   - target minimum distance: `max(0.18 × invalidation distance, 0.06 × ATR)`;
   - structural target accepted only when target/invalidation distance ratio `<= 0.28`.
5. Target/invalidation direction integrity and same-candle anti-leak construction remain intact.

## Interpretation

OF16 is an **in-sample ceiling experiment**. A higher historical lifecycle score is expected to come partly from memorizing/rewarding regimes already present in 2010–2026 and, for the target layer, from deliberately shorter target geometry. Its result must not be presented as an unbiased probability for unseen future data.

## Selection rule going forward

For OF16 only:

`KEEP candidate if full-2010–2026 objective improves; ignore validation/holdout degradation.`

The ordinary Amy SMC Z baseline keeps the opposite rule: robustness and anti-overfit checks remain required.
