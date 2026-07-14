# AMY ICT NextGen — Direction Forecast Backtest

Data: XAUUSD January 2022 through June 2026. Forecasts are evaluated from the confirmed trigger candle to the closing price at the fixed horizon. Repeated same-direction signals inside half of the forecast horizon are treated as one episode.

| Timeframe | Forecast pattern | Horizon | 2022-2024 | 2025 validation | 2026 out-of-sample | Pooled |
|---|---|---:|---:|---:|---:|---:|
| M5 | MSS + aligned H4 bias + EMA stack + nearby same-side POI | 24H | 53.6% (550) | 56.0% (184) | 55.9% (93) | 54.4% (827) |
| M15 | New EMA stack + aligned H4 bias + nearby same-side POI | 24H | 57.3% (260) | 61.5% (91) | 59.6% (52) | 58.5% (403) |
| H1 | Confirmed structural break + aligned H4 bias + price alignment | 48H | 55.2% (310) | 57.1% (112) | 61.7% (60) | 56.5% (482) |

The dashboard confidence values are rounded pooled hit rates, not guaranteed probabilities. When no tested trigger is active, the indicator returns `NO CLEAR DIRECTION` instead of forcing bullish or bearish output.
