# AMY ICT NextGen — Market State Structural Validation

Data: XAUUSD January 2022 through June 2026 on M5, M15, and H1.

Purpose: validate the current-condition classifier only. This is not a future-price test. The independent audit reference is a volatility-normalized 2 ATR swing structure. The production classifier uses confirmed fast and slow fractal structures plus the existing confirmed BOS/MSS direction. No future candle is read by the production classifier.

## Confirmed-state agreement with independent structural audit

| Timeframe | 2022-2024 | 2025 validation | 2026 out-of-sample | All data |
|---|---:|---:|---:|---:|
| M5 | 69.99% | 72.31% | 79.51% | 71.86% |
| M15 | 71.18% | 74.95% | 79.19% | 73.19% |
| H1 | 71.52% | 74.09% | 85.35% | 73.86% |

Confirmed-state coverage is 26.86% on M5, 26.17% on M15, and 30.60% on H1. Ambiguous structure is deliberately labeled transition or range instead of being forced into a confirmed trend.

## Structural invariants

- Every `UPTREND CONFIRMED` and `BULLISH PULLBACK` has fast HH/HL, slow HH/HL, bullish confirmed break state, and an intact latest swing low.
- Every `DOWNTREND CONFIRMED` and `BEARISH PULLBACK` has fast LH/LL, slow LH/LL, bearish confirmed break state, and an intact latest swing high.
- Every pullback label remains inside its trend invalidation level and occurs on the counter-trend swing phase.
- Invariant pass rate across all tested bars: 100%.

## Isolation guarantee

The source suffix beginning at the Liquidity Draw block was byte-compared before and after the Market State update. Liquidity Draw and Direction Forecast were not modified.
