from pathlib import Path

p = Path('Amy-SMC-X.pine')
s = p.read_text()

def rep(old: str, new: str, label: str):
    global s
    if old not in s:
        raise SystemExit(f'{label} block not found')
    s = s.replace(old, new, 1)

rep("""bool amyPatternStructureAligned = amyLastPatternDir != 0 and amyLastPatternDir == swingTrend.bias and amyLastPatternDir == internalTrend.bias
int amyPatternBiasActive = amyPatternActive and amyPatternStructureAligned ? amyLastPatternDir : 0
""", """bool amyPatternSwingAligned = amyLastPatternDir != 0 and amyLastPatternDir == swingTrend.bias
bool amyPatternInternalAligned = amyLastPatternDir != 0 and amyLastPatternDir == internalTrend.bias
bool amyPatternStructureAligned = amyPatternSwingAligned or amyPatternInternalAligned
int amyPatternBiasActive = amyPatternActive and amyPatternStructureAligned ? amyLastPatternDir : 0
""", 'pattern structure')

rep("""bool amyQualifiedBSLSweep = amyBSLSweep and high >= amyBSL + amyMinSweepExcursion and close >= amyBSL - nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedSSLSweep = amySSLSweep and low <= amySSL - amyMinSweepExcursion and close <= amySSL + nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedBSLValidBreak = amyBSLValidBreak and amyEventDisplacement and close > open and close >= amyBSL + amyMinBreakExcursion
bool amyQualifiedSSLValidBreak = amySSLValidBreak and amyEventDisplacement and close < open and close <= amySSL - amyMinBreakExcursion

bool amyQualifiedSwingBullBOS = barstate.isconfirmed and currentAlerts.swingBullishBOS and amyEventDisplacement and close > open
bool amyQualifiedSwingBearBOS = barstate.isconfirmed and currentAlerts.swingBearishBOS and amyEventDisplacement and close < open
bool amyQualifiedSwingBullCHoCH = barstate.isconfirmed and currentAlerts.swingBullishCHoCH and amyEventDisplacement and close > open
bool amyQualifiedSwingBearCHoCH = barstate.isconfirmed and currentAlerts.swingBearishCHoCH and amyEventDisplacement and close < open
""", """bool amyBearishRejection = close < open or close <= math.avg(high, low)
bool amyBullishRejection = close > open or close >= math.avg(high, low)
bool amyQualifiedBSLSweep = amyBSLSweep and high >= amyBSL + amyMinSweepExcursion and amyBearishRejection
bool amyQualifiedSSLSweep = amySSLSweep and low <= amySSL - amyMinSweepExcursion and amyBullishRejection
bool amyQualifiedBSLValidBreak = amyBSLValidBreak and amyEventDisplacement and close > open and close >= amyBSL + amyMinBreakExcursion
bool amyQualifiedSSLValidBreak = amySSLValidBreak and amyEventDisplacement and close < open and close <= amySSL - amyMinBreakExcursion

bool amyQualifiedSwingBullBOS = barstate.isconfirmed and currentAlerts.swingBullishBOS and amyEventDisplacement and close > open and close >= swingHigh.currentLevel + amyMinBreakExcursion
bool amyQualifiedSwingBearBOS = barstate.isconfirmed and currentAlerts.swingBearishBOS and amyEventDisplacement and close < open and close <= swingLow.currentLevel - amyMinBreakExcursion
bool amyQualifiedSwingBullCHoCH = barstate.isconfirmed and currentAlerts.swingBullishCHoCH and amyEventDisplacement and close > open and close >= swingHigh.currentLevel + amyMinBreakExcursion
bool amyQualifiedSwingBearCHoCH = barstate.isconfirmed and currentAlerts.swingBearishCHoCH and amyEventDisplacement and close < open and close <= swingLow.currentLevel - amyMinBreakExcursion
""", 'qualified events')

rep("""float amyRangeEQ = amyDRValid ? math.avg(amyRangeTop, amyRangeBottom) : na
float amyEQUpper = amyDRValid ? amyRangeBottom + amyRangeSpan * 0.525 : na
float amyEQLower = amyDRValid ? amyRangeBottom + amyRangeSpan * 0.475 : na
string amyDealingRange = 'EQUILIBRIUM'
int amyDealingBias = 0
if amyDRValid
    if close > amyEQUpper
        amyDealingRange := 'PREMIUM'
        amyDealingBias := amyDRBias == BEARISH ? BEARISH : 0
    else if close < amyEQLower
        amyDealingRange := 'DISCOUNT'
        amyDealingBias := amyDRBias == BULLISH ? BULLISH : 0
""", """float amyRangeEQ = amyDRValid ? math.avg(amyRangeTop, amyRangeBottom) : na
float amyEQUpper = amyDRValid ? amyRangeBottom + amyRangeSpan * 0.525 : na
float amyEQLower = amyDRValid ? amyRangeBottom + amyRangeSpan * 0.475 : na
float amyPremiumGate = amyDRValid ? amyRangeBottom + amyRangeSpan * 0.65 : na
float amyDiscountGate = amyDRValid ? amyRangeBottom + amyRangeSpan * 0.35 : na
bool amyDRBullContext = amyDRBias == BULLISH and swingTrend.bias == BULLISH and internalTrend.bias != BEARISH
bool amyDRBearContext = amyDRBias == BEARISH and swingTrend.bias == BEARISH and internalTrend.bias != BULLISH
string amyDealingRange = 'EQUILIBRIUM'
int amyDealingBias = 0
if amyDRValid
    if close > amyEQUpper
        amyDealingRange := 'PREMIUM'
        amyDealingBias := close >= amyPremiumGate and amyDRBearContext ? BEARISH : 0
    else if close < amyEQLower
        amyDealingRange := 'DISCOUNT'
        amyDealingBias := close <= amyDiscountGate and amyDRBullContext ? BULLISH : 0
""", 'dealing range')

rep("""float amyWeakHigh = swingTrend.bias == BULLISH ? trailing.top : na
float amyWeakLow = swingTrend.bias == BEARISH ? trailing.bottom : na
float amyForwardBSL = amyNearestAbove6(equalHigh.currentLevel, amyWeakHigh, amyPDH, amyPWH, swingHigh.currentLevel, amyRecentHigh, close)
float amyForwardSSL = amyNearestBelow6(equalLow.currentLevel, amyWeakLow, amyPDL, amyPWL, swingLow.currentLevel, amyRecentLow, close)
""", """float amyWeakHigh = swingTrend.bias == BULLISH and trailing.lastTopTime < time ? trailing.top : na
float amyWeakLow = swingTrend.bias == BEARISH and trailing.lastBottomTime < time ? trailing.bottom : na
float amyLiquidityMinDistance = nz(amyAtr14, ta.atr(14)) * 0.35
float amyForwardBSL = amyNearestAbove6(equalHigh.currentLevel, amyWeakHigh, amyPDH, amyPWH, swingHigh.currentLevel, amyRecentHigh, close + amyLiquidityMinDistance)
float amyForwardSSL = amyNearestBelow6(equalLow.currentLevel, amyWeakLow, amyPDL, amyPWL, swingLow.currentLevel, amyRecentLow, close - amyLiquidityMinDistance)
""", 'target ladder base')

rep("""bool amyPatternHTFAligned = amyPatternBiasActive != 0 and (amySafeHTFBias == 0 or amyPatternBiasActive == amySafeHTFBias)
bool amyPatternLocationAligned = amyPatternBiasActive == BULLISH ? amyDealingRange != 'PREMIUM' : amyPatternBiasActive == BEARISH ? amyDealingRange != 'DISCOUNT' : false
amyPatternBiasActive := amyPatternBiasActive != 0 and amyPatternHTFAligned and amyPatternLocationAligned ? amyPatternBiasActive : 0
""", """bool amyPatternHTFConflict = amyPatternBiasActive != 0 and amySafeHTFBias != 0 and amyPatternBiasActive != amySafeHTFBias
bool amyPatternStrongLocal = amyPatternBiasActive != 0 and amyPatternBiasActive == amyCurrentSwingBias and amyPatternBiasActive == amyCurrentInternalBias
bool amyPatternLocationAligned = amyPatternBiasActive == BULLISH ? amyDealingRange != 'PREMIUM' : amyPatternBiasActive == BEARISH ? amyDealingRange != 'DISCOUNT' : false
amyPatternBiasActive := amyPatternBiasActive != 0 and amyPatternLocationAligned and (not amyPatternHTFConflict or amyPatternStrongLocal) ? amyPatternBiasActive : 0
""", 'pattern context')

rep("""string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'
float amyTarget = amyNextDirection == BULLISH ? amyForwardBSL : amyForwardSSL
string amyTargetSide = amyNextDirection == BULLISH ? 'BSL' : 'SSL'
""", """string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'
float amyTargetRiskDistance = not na(amyInvalidation) ? math.abs(close - amyInvalidation) : 0.0
float amyTargetMinDistance = math.max(nz(amyAtr14, ta.atr(14)) * 0.50, amyTargetRiskDistance * 0.75)
float amyTarget = amyNextDirection == BULLISH ? amyNearestAbove6(equalHigh.currentLevel, amyWeakHigh, amyPDH, amyPWH, swingHigh.currentLevel, amyRecentHigh, close + amyTargetMinDistance) : amyNearestBelow6(equalLow.currentLevel, amyWeakLow, amyPDL, amyPWL, swingLow.currentLevel, amyRecentLow, close - amyTargetMinDistance)
string amyTargetSide = amyNextDirection == BULLISH ? 'BSL' : 'SSL'
""", 'risk-aware target')

rep("""bool amyxBullStructureEvent = barstate.isconfirmed and (currentAlerts.swingBullishBOS or currentAlerts.swingBullishCHoCH) and amyxImpulseDisplacement and close > open and close >= high - amyxImpulseRange * 0.25
bool amyxBearStructureEvent = barstate.isconfirmed and (currentAlerts.swingBearishBOS or currentAlerts.swingBearishCHoCH) and amyxImpulseDisplacement and close < open and close <= low + amyxImpulseRange * 0.25
""", """bool amyxBullStructureEvent = (amyQualifiedSwingBullBOS or amyQualifiedSwingBullCHoCH) and (amySafeHTFBias == 0 or amySafeHTFBias == BULLISH) and amyCurrentInternalBias != BEARISH and close >= high - amyxImpulseRange * 0.25
bool amyxBearStructureEvent = (amyQualifiedSwingBearBOS or amyQualifiedSwingBearCHoCH) and (amySafeHTFBias == 0 or amySafeHTFBias == BEARISH) and amyCurrentInternalBias != BULLISH and close <= low + amyxImpulseRange * 0.25
""", 'ote fib impulse')

assert 'float amyFinalScore = amySafeHTFBias * 35 + amyCurrentSwingBias * 30 + amyCurrentInternalBias * 20 + amyLiquidityBiasActive * 15' in s
assert 'float amyContextScore = amySafeHTFBias * 25 + amyCurrentSwingBias * 25 + amyCurrentInternalBias * 15 + amyLiquidityBiasActive * 15' in s
core_window = s[s.index('float amyFinalScore'):s.index('var table amyDashboard')]
assert 'amyDealingBias *' not in core_window
assert 'amyPatternBiasActive *' not in core_window

p.write_text(s)
