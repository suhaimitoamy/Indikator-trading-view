# AMY Adaptive Regime Compass 2019–2026

## Purpose

This indicator was built from the audited XAUUSD candle archive in Google Drive to read:

- **Past:** historical direction and regime changes without future leakage.
- **Present:** current closed-candle direction, regime, confidence, and higher-timeframe conflict.
- **Future:** a selective directional forecast with target and invalidation, or **WAIT** when the evidence is weak.

It is a context and forecast engine, not an automatic entry strategy.

## Dataset read

The analysis loaded all available monthly archives from **January 2019 through July 2026**.

| Timeframe | Rows loaded |
|---|---:|
| M5 | 548,000 |
| M15 | 182,680 |
| H1 | 45,690 |
| H4 | 12,421 |
| D1 | 2,389 |

### Data integrity

- **2019–2025:** repaired/audited BID data. The source clock is fixed UTC-05:00. Upstream gaps were retained; no synthetic candles were inserted.
- **2020–2024:** provenance was verified against HistData.com.
- **2019 and 2025:** lineage is consistent but provenance remains inferred.
- **2026:** January–July replacement data from Dukascopy BID UTC. It passed timestamp, OHLC, aggregation, and archive validation.
- 2026 is **year-to-date through July 31**, not a full calendar year.

## Market behavior found

The data does not support one permanent market model.

- Strong continuation phases appeared in 2019–2020 and especially 2024–2025.
- 2021–2023 repeatedly punished fixed trend-following assumptions through rotation, failed continuation, and deeper drawdowns.
- 2026 showed a different volatility profile and more directional persistence at H1, while also producing the largest median daily ATR percentage in the sample.
- H1 regime composition changed continuously: roughly 36–41% trend, 37–45% range, and 17–25% transition depending on year.

This is why the indicator does **not** force a single trend rule across all years.

## Architecture

### 1. Scale-independent features

All directional components are normalized by ATR or bounded to `[-1, +1]`:

- EMA 21/55/200 relationship
- EMA slope
- 20-bar structural position and breakout
- 12-bar momentum
- Kaufman-style efficiency ratio
- DMI/ADX regime strength
- distance from the medium EMA

The engine is therefore not tied to XAUUSD price level changes from 1,200 to above 4,000.

### 2. Two competing models

The indicator calculates:

1. **Continuation model** — follows aligned trend, slope, structure, momentum, and efficiency.
2. **Mean-reversion model** — fades excessive distance, momentum extension, and failed structural pressure.

### 3. Past-only adaptive memory

For each model, the script evaluates the outcome of the prediction made `forecastHorizon` bars earlier. The current model weight is based only on already-realized historical outcomes.

- Positive continuation edge gives weight to continuation.
- Positive reversion edge gives weight to mean reversion.
- If neither model has positive edge, the forecast loses confidence and normally becomes **WAIT**.

This is adaptation, not future leakage.

### 4. Confirmed multi-timeframe context

Default context:

- chart timeframe
- H1
- H4
- D1

Higher-timeframe requests use the confirmed-bar offset pattern. The user must keep each configured context timeframe strictly higher than the previous one. Otherwise, the dashboard returns **SET HIGHER TFs** and the decision remains **WAIT**.

### 5. Conservative decision gate

A BUY or SELL focus requires all of the following:

- composite score exceeds the threshold;
- confidence exceeds the threshold;
- multi-timeframe alignment exceeds the threshold;
- H1/H4 do not have a strong opposite-direction conflict;
- context timeframe configuration is valid.

Any failure produces **WAIT** with a reason.

## Default interpretation

- **BUY FOCUS:** directional evidence favors bullish continuation or bullish mean reversion.
- **SELL FOCUS:** directional evidence favors bearish continuation or bearish mean reversion.
- **WAIT:** score, confidence, alignment, model edge, or higher-timeframe context is insufficient.

The projected target is ATR-adaptive. Mean-reversion forecasts prefer the medium EMA when it lies in the forecast direction. Invalidation uses the medium EMA, recent structural extreme, and an ATR buffer.

## Non-repainting safeguards

- Local decisions use the last closed chart candle on realtime bars.
- Higher-timeframe values are offset by one HTF bar and requested with `barmerge.lookahead_on`.
- Alerts trigger only on confirmed local bars.
- No pivots or historical values are moved after confirmation.

## Files

- `AMY_Adaptive_Regime_Compass_2019_2026.pine`
- `AMY_Adaptive_Regime_Compass_2019_2026_Annual_Research.csv`
- `AMY_Adaptive_Regime_Compass_2019_2026_RESEARCH.md`

## Limitations

- No indicator can be accurate in every future market condition.
- Different broker feeds and daily boundaries can change individual candles.
- The 2019 and 2025 source provenance is inferred, and upstream gaps remain.
- 2026 covers January–July only and uses a different provider/timezone from 2019–2025.
- The indicator should be validated manually on TradingView before being used in live execution.
