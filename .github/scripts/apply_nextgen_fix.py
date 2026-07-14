from pathlib import Path

pine_path = Path("AMY_ICT_NextGen.pine")
text = pine_path.read_text(encoding="utf-8")


def replace_once(old: str, new: str, label: str) -> None:
    global text
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    text = text.replace(old, new, 1)


replace_once(
    '''if newTradingDay
    pdhConsumed := false
    pdlConsumed := false

if not na(pdh) and high >= pdh
    pdhConsumed := true
if not na(pdl) and low <= pdl
    pdlConsumed := true''',
    '''if newTradingDay
    pdhConsumed := false
    pdlConsumed := false

newPdhSweep = not pdhConsumed and not na(pdh) and high > pdh and close < pdh and barstate.isconfirmed
newPdlSweep = not pdlConsumed and not na(pdl) and low < pdl and close > pdl and barstate.isconfirmed
pdhReached = not pdhConsumed and not na(pdh) and high >= pdh and barstate.isconfirmed
pdlReached = not pdlConsumed and not na(pdl) and low <= pdl and barstate.isconfirmed

if pdhReached
    pdhConsumed := true
if pdlReached
    pdlConsumed := true''',
    "previous-day liquidity state",
)

replace_once(
    '''if newTradingWeek
    pwhConsumed := false
    pwlConsumed := false

if not na(pwh) and high >= pwh
    pwhConsumed := true
if not na(pwl) and low <= pwl
    pwlConsumed := true''',
    '''if newTradingWeek
    pwhConsumed := false
    pwlConsumed := false

newPwhSweep = not pwhConsumed and not na(pwh) and high > pwh and close < pwh and barstate.isconfirmed
newPwlSweep = not pwlConsumed and not na(pwl) and low < pwl and close > pwl and barstate.isconfirmed
pwhReached = not pwhConsumed and not na(pwh) and high >= pwh and barstate.isconfirmed
pwlReached = not pwlConsumed and not na(pwl) and low <= pwl and barstate.isconfirmed

if pwhReached
    pwhConsumed := true
if pwlReached
    pwlConsumed := true''',
    "previous-week liquidity state",
)

replace_once(
    '''var int lastBuySweepBar = na
var int lastSellSweepBar = na
if newBslSweep
    bslConsumed := true
    lastBuySweepBar := bar_index
if newSslSweep
    sslConsumed := true
    lastSellSweepBar := bar_index
if asiaHighReached
    asiaHighConsumed := true
if asiaLowReached
    asiaLowConsumed := true
if newAsiaHighSweep
    lastBuySweepBar := bar_index
if newAsiaLowSweep
    lastSellSweepBar := bar_index

recentBuySweep = not na(lastBuySweepBar) and bar_index - lastBuySweepBar <= entrySweepMemoryBars
recentSellSweep = not na(lastSellSweepBar) and bar_index - lastSellSweepBar <= entrySweepMemoryBars
liqText = recentSellSweep and recentBuySweep ? "BOTH SIDES SWEPT" : recentSellSweep ? "SELLSIDE SWEPT" : recentBuySweep ? "BUYSIDE SWEPT" : "WAITING"''',
    '''var int lastBuySweepBar = na
var int lastSellSweepBar = na
var string lastBuySweepName = "BUYSIDE"
var string lastSellSweepName = "SELLSIDE"
if newBslSweep
    bslConsumed := true
    lastBuySweepBar := bar_index
    lastBuySweepName := "INTERNAL BSL SWEPT"
if newSslSweep
    sslConsumed := true
    lastSellSweepBar := bar_index
    lastSellSweepName := "INTERNAL SSL SWEPT"
if asiaHighReached
    asiaHighConsumed := true
if asiaLowReached
    asiaLowConsumed := true
if newAsiaHighSweep
    lastBuySweepBar := bar_index
    lastBuySweepName := "ASIA HIGH SWEPT"
if newAsiaLowSweep
    lastSellSweepBar := bar_index
    lastSellSweepName := "ASIA LOW SWEPT"
if newPdhSweep
    lastBuySweepBar := bar_index
    lastBuySweepName := "PDH SWEPT"
if newPdlSweep
    lastSellSweepBar := bar_index
    lastSellSweepName := "PDL SWEPT"
if newPwhSweep
    lastBuySweepBar := bar_index
    lastBuySweepName := "PWH SWEPT"
if newPwlSweep
    lastSellSweepBar := bar_index
    lastSellSweepName := "PWL SWEPT"

recentBuySweep = not na(lastBuySweepBar) and bar_index - lastBuySweepBar <= entrySweepMemoryBars
recentSellSweep = not na(lastSellSweepBar) and bar_index - lastSellSweepBar <= entrySweepMemoryBars
liqText = recentSellSweep and recentBuySweep ? "BOTH SIDES SWEPT" : recentSellSweep ? lastSellSweepName : recentBuySweep ? lastBuySweepName : "WAITING"''',
    "sweep memory and labels",
)

replace_once(
    '''if not pwlConsumed and not na(pwl) and pwl < close and (na(nearestSslTarget) or pwl > nearestSslTarget)
    nearestSslTarget := pwl
    nearestSslName := "PWL"

bslDistance =''',
    '''if not pwlConsumed and not na(pwl) and pwl < close and (na(nearestSslTarget) or pwl > nearestSslTarget)
    nearestSslTarget := pwl
    nearestSslName := "PWL"

upperWick = high - math.max(open, close)
lowerWick = math.min(open, close) - low
upperRejectionCandle = upperWick >= math.max(body * 0.75, atr * 0.10) and close <= high - barRange * 0.35
lowerRejectionCandle = lowerWick >= math.max(body * 0.75, atr * 0.10) and close >= low + barRange * 0.35
upperLiquidityRejection = upperRejectionCandle and not na(nearestBslTarget) and high >= nearestBslTarget - atr * 0.25 and close < nearestBslTarget
lowerLiquidityRejection = lowerRejectionCandle and not na(nearestSslTarget) and low <= nearestSslTarget + atr * 0.25 and close > nearestSslTarget
rejectionDirection = (lowerLiquidityRejection ? 1.0 : 0.0) - (upperLiquidityRejection ? 1.0 : 0.0)

bslDistance =''',
    "liquidity rejection context",
)

replace_once(
    '''predictionLogit = 5.0 * (distanceLocation - 0.50) + 0.40 * htfDirection + 0.50 * structureDirection + 0.40 * emaDirection + 0.20 * priceDirection + 0.60 * sweepDirection + 0.25 * rangeDirection + 0.30 * eventDirection + 0.25 * emaSlopeAtr + 0.15 * bodyAtr''',
    '''predictionLogit = 5.0 * (distanceLocation - 0.50) + 0.40 * htfDirection + 0.50 * structureDirection + 0.40 * emaDirection + 0.20 * priceDirection + 0.60 * sweepDirection + 0.25 * rangeDirection + 0.30 * eventDirection + 0.25 * emaSlopeAtr + 0.15 * bodyAtr + 0.40 * rejectionDirection''',
    "prediction rejection weight",
)

replace_once(
    '''bslHighConfidence = predictionSupported and not inAsia and hasTwoSidedLiquidity and bslDrawPercent >= liquidityDirectionThreshold
sslHighConfidence = predictionSupported and not inAsia and hasTwoSidedLiquidity and sslDrawPercent >= liquidityDirectionThreshold
liquidityDominance = not predictionSupported ? "PREDICTION UNSUPPORTED" : inAsia ? "ASIA RANGE BUILDING" : bslHighConfidence ? "PREDICT BSL FIRST" : sslHighConfidence ? "PREDICT SSL FIRST" : hasTwoSidedLiquidity ? "WAIT - LOW CONFIDENCE" : "WAIT - LEVELS INCOMPLETE"''',
    '''bslHighConfidence = predictionSupported and not inAsia and hasTwoSidedLiquidity and bslDrawPercent >= liquidityDirectionThreshold and not upperLiquidityRejection
sslHighConfidence = predictionSupported and not inAsia and hasTwoSidedLiquidity and sslDrawPercent >= liquidityDirectionThreshold and not lowerLiquidityRejection
predictionTextColor = bslHighConfidence ? color.lime : sslHighConfidence ? color.red : color.yellow
liquidityDominance = not predictionSupported ? "PREDICTION UNSUPPORTED" : inAsia ? "ASIA RANGE BUILDING" : upperLiquidityRejection and bslDrawPercent > sslDrawPercent ? "WAIT - UPPER REJECTION" : lowerLiquidityRejection and sslDrawPercent > bslDrawPercent ? "WAIT - LOWER REJECTION" : bslHighConfidence ? "PREDICT BSL FIRST" : sslHighConfidence ? "PREDICT SSL FIRST" : hasTwoSidedLiquidity ? "WAIT - LOW CONFIDENCE" : "WAIT - LEVELS INCOMPLETE"''',
    "prediction status gating",
)

replace_once(
    '''else if bosBear
    eventName := "BOS BEAR"
    eventPrice := lastLow
else if newBslSweep
    eventName := "BSL SWEEP"
    eventPrice := lastHigh''',
    '''else if bosBear
    eventName := "BOS BEAR"
    eventPrice := lastLow
else if newPwhSweep
    eventName := "PWH SWEEP"
    eventPrice := pwh
else if newPwlSweep
    eventName := "PWL SWEEP"
    eventPrice := pwl
else if newPdhSweep
    eventName := "PDH SWEEP"
    eventPrice := pdh
else if newPdlSweep
    eventName := "PDL SWEEP"
    eventPrice := pdl
else if newBslSweep
    eventName := "BSL SWEEP"
    eventPrice := lastHigh''',
    "external liquidity event history",
)

replace_once(
    '''event0 = eventLog.size() > 0 ? eventLog.get(0) : "No confirmed event"
event1 = eventLog.size() > 1 ? eventLog.get(1) : "-"
event2 = eventLog.size() > 2 ? eventLog.get(2) : "-"''',
    '''event0 = eventLog.size() > 0 ? eventLog.get(0) : "No confirmed event"
event1 = eventLog.size() > 1 ? eventLog.get(1) : "-"
event2 = eventLog.size() > 2 ? eventLog.get(2) : "-"
bslTargetDashboard = na(nearestBslTarget) ? "NONE" : nearestBslName + " " + f_price(nearestBslTarget) + (hasTwoSidedLiquidity ? " · " + str.tostring(bslDrawPercent) + "%" : " · -")
sslTargetDashboard = na(nearestSslTarget) ? "NONE" : nearestSslName + " " + f_price(nearestSslTarget) + (hasTwoSidedLiquidity ? " · " + str.tostring(sslDrawPercent) + "%" : " · -")''',
    "dashboard target text",
)

replace_once(
    '''table.cell(dashboard, 1, 2, liquidityDominance, text_color=bslDrawPercent > sslDrawPercent ? color.lime : sslDrawPercent > bslDrawPercent ? color.red : color.silver, text_size=size.small, text_halign=text.align_left, bgcolor=dashBg)

    table.cell(dashboard, 0, 3, "BSL", text_color=color.white, text_size=size.small, bgcolor=dashAlt)
    table.cell(dashboard, 1, 3, f_meter(bslDrawPercent) + "  " + str.tostring(bslDrawPercent) + "%", text_color=color.lime, text_size=size.tiny, text_halign=text.align_left, bgcolor=dashAlt)

    table.cell(dashboard, 0, 4, "SSL", text_color=color.white, text_size=size.small, bgcolor=dashBg)
    table.cell(dashboard, 1, 4, f_meter(sslDrawPercent) + "  " + str.tostring(sslDrawPercent) + "%", text_color=color.red, text_size=size.tiny, text_halign=text.align_left, bgcolor=dashBg)''',
    '''table.cell(dashboard, 1, 2, liquidityDominance, text_color=predictionTextColor, text_size=size.small, text_halign=text.align_left, bgcolor=dashBg)

    table.cell(dashboard, 0, 3, "BSL TARGET", text_color=color.white, text_size=size.small, bgcolor=dashAlt)
    table.cell(dashboard, 1, 3, bslTargetDashboard, text_color=color.lime, text_size=size.tiny, text_halign=text.align_left, bgcolor=dashAlt)

    table.cell(dashboard, 0, 4, "SSL TARGET", text_color=color.white, text_size=size.small, bgcolor=dashBg)
    table.cell(dashboard, 1, 4, sslTargetDashboard, text_color=color.red, text_size=size.tiny, text_halign=text.align_left, bgcolor=dashBg)''',
    "dashboard probability and target rows",
)

required = [
    "newPdhSweep =",
    "newPwhSweep =",
    'lastBuySweepName := "PWH SWEPT"',
    "upperLiquidityRejection =",
    "0.40 * rejectionDirection",
    'eventName := "PWH SWEEP"',
    'table.cell(dashboard, 0, 3, "BSL TARGET"',
    "bslTargetDashboard =",
]
missing = [item for item in required if item not in text]
if missing:
    raise RuntimeError(f"Missing required updates: {missing}")

pine_path.write_text(text, encoding="utf-8")

readme_path = Path("README.md")
readme = readme_path.read_text(encoding="utf-8")
if "`AMY_ICT_NextGen.pine`" not in readme:
    readme = readme.replace(
        "| `README.md` | Dokumentasi | Aktif | Dokumentasi utama dan index seluruh isi repo. |\n",
        "| `README.md` | Dokumentasi | Aktif | Dokumentasi utama dan index seluruh isi repo. |\n| `AMY_ICT_NextGen.pine` | Indicator Pine v5 | Aktif | Market mapping utama dengan session, BOS/MSS, BSL/SSL, PDH/PDL, PWH/PWL, OB/FVG, liquidity draw, rejection context, entry map, dan dashboard. |\n",
        1,
    )
    marker = "### `indikator-v1.pine`\n"
    detail = '''### `AMY_ICT_NextGen.pine`

Indikator market mapping utama dengan pembacaan struktur dan liquidity terintegrasi.

Fitur utama:

- Asia High/Low.
- PDH/PDL dan PWH/PWL.
- BOS/MSS dan structural invalidation.
- BSL/SSL dengan riwayat sweep spesifik.
- HTF bias dan EMA stack.
- Order Block dan Fair Value Gap.
- Premium/Discount.
- Predicted liquidity draw dengan rejection filter.
- Target liquidity terdekat pada dashboard.
- Compact entry map M5, M15, dan H1.

'''
    if marker not in readme:
        raise RuntimeError("README detail marker not found")
    readme = readme.replace(marker, detail + marker, 1)
    readme_path.write_text(readme, encoding="utf-8")
