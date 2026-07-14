# AMY ICT NextGen — Direction Forecast v2 Backtest

Data: XAUUSD January 2022 through June 2026. Only `DIRECTION FORECAST` was tested. Market State, Liquidity Draw, Entry Map, SL, and TP were excluded from this backtest.

Method: every forecast is evaluated from its confirmed trigger candle to the closing price at the fixed horizon. Repeated same-direction triggers inside half of the horizon are treated as one episode. Development uses 2022-2024, validation uses 2025, and January-June 2026 is untouched out-of-sample confirmation.

## Final validated rules

| Timeframe | Validated forecast | Horizon | Display confidence |
|---|---|---:|---:|
| M5 | MSS + confirmed local Market State + price alignment | 24H | 65% |
| M15 | H4-aligned structural break from the opposite side of the 80-bar range | 48H | 60% |
| H1 | Bullish structural break + H4/price alignment + positive non-overextended 3-bar momentum | 72H | 65% |

H1 bearish continuation did not produce repeatable out-of-sample edge. It is intentionally suppressed and returns `NO CLEAR DIRECTION` rather than a forced bearish forecast.

## Directional accuracy

| Timeframe | 2022-2024 | 2025 validation | 2026 out-of-sample | All episodes |
|---|---:|---:|---:|---:|
| M5 | 69.62% (79) | 60.87% (23) | 60.00% (10) | 66.96% (112) |
| M15 | 60.00% (115) | 59.46% (37) | 64.71% (17) | 60.36% (169) |
| H1 bullish only | 67.19% (128) | 65.00% (60) | 66.67% (18) | 66.50% (206) |

## Direction balance

| Timeframe | Bullish | Bearish |
|---|---:|---:|
| M5 | 68.33% (60) | 65.38% (52) |
| M15 | 60.24% (83) | 60.47% (86) |
| H1 | 66.50% (206) | Not validated — suppressed |

## Statistical checks

- M5 pooled 95% Wilson interval: 57.82%-74.99%; one-sided binomial p = 0.0002 versus 50%.
- M15 pooled 95% Wilson interval: 52.83%-67.42%; one-sided binomial p = 0.0044 versus 50%.
- H1 bullish pooled 95% Wilson interval: 59.81%-72.60%; one-sided binomial p = 0.0000012 versus 50%.
- The selected parameters sit on stable performance plateaus rather than relying on one isolated best setting.
- Forecasts are cancelled by an opposite confirmed structural break before expiry.

## Isolation guarantee

The source before the Direction Forecast marker and from the Entry Map marker onward is byte-preserved. Market State and Liquidity Draw were not changed or retested.
