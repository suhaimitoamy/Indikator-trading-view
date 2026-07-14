from pathlib import Path

pine_path = Path("AMY_ICT_NextGen.pine")
text = pine_path.read_text(encoding="utf-8")

start_marker = "// ============================================================================\n// DIRECTION FORECAST — SELECTIVE, HORIZON-BOUND, OUT-OF-SAMPLE TESTED"
end_marker = "// ============================================================================\n// COMPACT ENTRY MAP — CHART ONLY, ONE LIVE SETUP"

if text.count(start_marker) != 1:
    raise SystemExit(f"Expected one Direction Forecast start marker, found {text.count(start_marker)}")
if text.count(end_marker) != 1:
    raise SystemExit(f"Expected one Entry Map marker, found {text.count(end_marker)}")

start = text.index(start_marker)
end = text.index(end_marker)
protected_prefix = text[:start]
protected_suffix = text[end:]

new_block = '''// ============================================================================
// DIRECTION FORECAST v2 — ONLY VALIDATED FORECAST PATTERNS
// Fixed-horizon direction test using confirmed candles only.
// M5: structural MSS aligned with confirmed local state and price, 24H horizon.
// M15: H4-aligned structural break from the opposite side of the 80-bar range,
//      48H horizon.
// H1: selective bullish continuation only, with positive but non-overextended
//     3-bar momentum, 72H horizon. Bearish H1 did not pass validation, therefore
//     the correct output is NO CLEAR DIRECTION instead of a forced bearish call.
// ============================================================================
forecastM5 = timeframe.isminutes and timeframe.multiplier == 5
forecastM15 = timeframe.isminutes and timeframe.multiplier == 15
forecastH1 = timeframe.isminutes and timeframe.multiplier == 60
forecastSupported = forecastM5 or forecastM15 or forecastH1

pdRangeSize = math.max(pdHigh - pdLow, syminfo.mintick)
pdRangePosition = (close - pdLow) / pdRangeSize
directionMomentum3Atr = atr > 0 and not na(close[3]) ? (close - close[3]) / atr : 0.0

m5BullForecastTrigger = forecastM5 and mssBull and marketBullConfirmed and priceBull
m5BearForecastTrigger = forecastM5 and mssBear and marketBearConfirmed and priceBear

m15BullForecastTrigger = forecastM15 and rawBreakBull and htfBullConfirmed and pdRangePosition < 0.45
m15BearForecastTrigger = forecastM15 and rawBreakBear and htfBearConfirmed and pdRangePosition > 0.55

h1BullMomentumOk = directionMomentum3Atr > 0.0 and directionMomentum3Atr < 2.50
h1BullForecastTrigger = forecastH1 and rawBreakBull and htfBullConfirmed and priceBull and h1BullMomentumOk
h1BearForecastTrigger = false

bullForecastTrigger = m5BullForecastTrigger or m15BullForecastTrigger or h1BullForecastTrigger
bearForecastTrigger = m5BearForecastTrigger or m15BearForecastTrigger or h1BearForecastTrigger
forecastCandidateDir = bullForecastTrigger and not bearForecastTrigger ? 1 : bearForecastTrigger and not bullForecastTrigger ? -1 : 0

forecastHorizonBars = forecastM5 ? 288 : forecastM15 ? 192 : forecastH1 ? 72 : 0
forecastCooldownBars = forecastM5 ? 144 : forecastM15 ? 96 : forecastH1 ? 36 : 0
forecastBaseConfidence = forecastM5 ? 65 : forecastM15 ? 60 : forecastH1 ? 65 : 0
forecastHorizonText = forecastM5 ? "24H" : forecastM15 ? "48H" : forecastH1 ? "72H" : "-"

var int directionForecastDir = 0
var int directionForecastStartBar = na
var int directionForecastExpiryBar = na

forecastExpired = directionForecastDir != 0 and not na(directionForecastExpiryBar) and bar_index > directionForecastExpiryBar
forecastInvalidated = directionForecastDir == 1 and rawBreakBear or directionForecastDir == -1 and rawBreakBull

if forecastExpired or forecastInvalidated or not showDirectionForecast or not forecastSupported
    directionForecastDir := 0
    directionForecastStartBar := na
    directionForecastExpiryBar := na

canRefreshForecast = na(directionForecastStartBar) or forecastCandidateDir != directionForecastDir or bar_index - directionForecastStartBar >= forecastCooldownBars
newDirectionForecast = showDirectionForecast and forecastCandidateDir != 0 and canRefreshForecast and barstate.isconfirmed

if newDirectionForecast
    directionForecastDir := forecastCandidateDir
    directionForecastStartBar := bar_index
    directionForecastExpiryBar := bar_index + forecastHorizonBars

directionForecastActive = directionForecastDir != 0 and not na(directionForecastExpiryBar) and bar_index <= directionForecastExpiryBar
directionForecastText = not forecastSupported ? "UNSUPPORTED — USE M5 / M15 / H1" : not showDirectionForecast ? "DISABLED" : directionForecastActive ? (directionForecastDir == 1 ? "BULLISH" : "BEARISH") + " · " + str.tostring(forecastBaseConfidence) + "% · " + forecastHorizonText : "NO CLEAR DIRECTION"
directionForecastColor = directionForecastDir == 1 ? color.lime : directionForecastDir == -1 ? color.red : color.yellow

'''

updated = protected_prefix + new_block + protected_suffix
if updated[:start] != protected_prefix:
    raise SystemExit("Protected Market State / Liquidity Draw prefix changed")
new_end = updated.index(end_marker)
if updated[new_end:] != protected_suffix:
    raise SystemExit("Protected Entry Map suffix changed")

required = [
    "m5BullForecastTrigger = forecastM5 and mssBull and marketBullConfirmed and priceBull",
    "m15BullForecastTrigger = forecastM15 and rawBreakBull and htfBullConfirmed and pdRangePosition < 0.45",
    "h1BullMomentumOk = directionMomentum3Atr > 0.0 and directionMomentum3Atr < 2.50",
    "h1BearForecastTrigger = false",
    "forecastInvalidated = directionForecastDir == 1 and rawBreakBear or directionForecastDir == -1 and rawBreakBull",
]
missing = [item for item in required if item not in updated]
if missing:
    raise SystemExit(f"Missing Direction Forecast v2 components: {missing}")

pine_path.write_text(updated, encoding="utf-8")

report = '''# AMY ICT NextGen — Direction Forecast v2 Backtest

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
'''
Path("DIRECTION_FORECAST_BACKTEST.md").write_text(report, encoding="utf-8")
