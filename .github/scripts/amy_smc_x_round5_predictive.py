from pathlib import Path

p = Path('Amy-SMC-X.pine')
s = p.read_text()


def repl(old: str, new: str, label: str):
    global s
    if old not in s:
        raise SystemExit(f'{label} block not found')
    s = s.replace(old, new, 1)

# 1) Liquidity Sweep / Valid Break predictive qualification.
# Raw sweep/break state and Event History stay untouched; only qualified predictive labels are tuned.
old = """bool amyLiquidityRound4TF = timeframe.period == '15'
bool amySweepBearStructureOK = internalTrend.bias != BULLISH and (swingTrend.bias == BEARISH or amyEventHTFBearOK)
bool amySweepBullStructureOK = internalTrend.bias != BEARISH and (swingTrend.bias == BULLISH or amyEventHTFBullOK)
bool amyQualifiedBSLSweepBase = amyBSLSweep and high >= amyBSL + amyMinSweepExcursion and close >= amyBSL - nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedSSLSweepBase = amySSLSweep and low <= amySSL - amyMinSweepExcursion and close <= amySSL + nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedBSLValidBreakBase = amyBSLValidBreak and amyEventDisplacement and close > open and close >= amyBSL + amyMinBreakExcursion
bool amyQualifiedSSLValidBreakBase = amySSLValidBreak and amyEventDisplacement and close < open and close <= amySSL - amyMinBreakExcursion
bool amyQualifiedBSLSweep = amyQualifiedBSLSweepBase and (not amyLiquidityRound4TF or amySweepBearStructureOK)
bool amyQualifiedSSLSweep = amyQualifiedSSLSweepBase and (not amyLiquidityRound4TF or amySweepBullStructureOK)
bool amyQualifiedBSLValidBreak = amyQualifiedBSLValidBreakBase and (not amyLiquidityRound4TF or (internalTrend.bias == BULLISH and amyEventHTFBullOK))
bool amyQualifiedSSLValidBreak = amyQualifiedSSLValidBreakBase and (not amyLiquidityRound4TF or (internalTrend.bias == BEARISH and amyEventHTFBearOK))
"""
new = """bool amyRound5M5 = timeframe.period == '5'
bool amyRound5M15 = timeframe.period == '15'
bool amyRound5H1 = timeframe.period == '60'
bool amyRound5TestTF = amyRound5M5 or amyRound5M15 or amyRound5H1
bool amyQualifiedBSLSweepBase = amyBSLSweep and high >= amyBSL + amyMinSweepExcursion and close >= amyBSL - nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedSSLSweepBase = amySSLSweep and low <= amySSL - amyMinSweepExcursion and close <= amySSL + nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedBSLValidBreakBase = amyBSLValidBreak and amyEventDisplacement and close > open and close >= amyBSL + amyMinBreakExcursion
bool amyQualifiedSSLValidBreakBase = amySSLValidBreak and amyEventDisplacement and close < open and close <= amySSL - amyMinBreakExcursion
float amyBreakBodyAtr = not na(amyEventAtr) and amyEventAtr > 0 ? amyEventBody / amyEventAtr : 0.0
// On the tested M5/M15/H1 profiles a sweep remains context, not a predictive call, until a stronger confirmation exists.
bool amyQualifiedBSLSweep = amyRound5TestTF ? false : amyQualifiedBSLSweepBase
bool amyQualifiedSSLSweep = amyRound5TestTF ? false : amyQualifiedSSLSweepBase
bool amyQualifiedBSLValidBreak = amyRound5M5 ? (amyQualifiedBSLValidBreakBase and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.65) : amyRound5M15 ? (amyQualifiedBSLValidBreakBase and internalTrend.bias == BULLISH and amyEventHTFBullOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedBSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedBSLValidBreakBase
bool amyQualifiedSSLValidBreak = amyRound5M5 ? (amyQualifiedSSLValidBreakBase and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.65) : amyRound5M15 ? (amyQualifiedSSLValidBreakBase and internalTrend.bias == BEARISH and amyEventHTFBearOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedSSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedSSLValidBreakBase
"""
repl(old, new, 'liquidity qualification')

# 2) BOS / CHoCH predictive layer.
# Base qualification is deliberately untouched because passed OTE/Fib 1.272 consumes it.
old = """// Directional BOS gets one extra confirmation from the accepted HTF Swing. CHoCH keeps the previous rule.
bool amyQualifiedSwingBullBOS = amyBaseQualifiedSwingBullBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH)
bool amyQualifiedSwingBearBOS = amyBaseQualifiedSwingBearBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH)
bool amyQualifiedSwingBullCHoCH = amyBaseQualifiedSwingBullCHoCH
bool amyQualifiedSwingBearCHoCH = amyBaseQualifiedSwingBearCHoCH
"""
new = """// Round 5 predictive structure layer. Raw BOS remains valid descriptive structure, but on tested profiles
// it is not promoted as a forward prediction because its follow-through was weaker than CHoCH.
float amyBullCHoCHExcursionAtr = not na(amyEventAtr) and amyEventAtr > 0 and not na(swingHigh.currentLevel) ? (close - swingHigh.currentLevel) / amyEventAtr : 0.0
float amyBearCHoCHExcursionAtr = not na(amyEventAtr) and amyEventAtr > 0 and not na(swingLow.currentLevel) ? (swingLow.currentLevel - close) / amyEventAtr : 0.0
bool amyQualifiedSwingBullBOS = amyRound5TestTF ? false : amyBaseQualifiedSwingBullBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH)
bool amyQualifiedSwingBearBOS = amyRound5TestTF ? false : amyBaseQualifiedSwingBearBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH)
bool amyQualifiedSwingBullCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BEARISH and amyBullCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBullCHoCH and amyBullCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? amyBaseQualifiedSwingBullCHoCH : amyBaseQualifiedSwingBullCHoCH
bool amyQualifiedSwingBearCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BULLISH and amyBearCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBearCHoCH and amyBearCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? amyBaseQualifiedSwingBearCHoCH : amyBaseQualifiedSwingBearCHoCH
"""
repl(old, new, 'BOS CHoCH qualification')

# 3) Pattern: keep detector and previous context qualification, then suppress only pattern families that reduced follow-through.
old = """amyPatternBiasActive := amyPatternContextQualified ? amyPatternCandidate : 0
"""
new = """bool amyPatternNameAllowed = amyRound5M5 ? (amyLastPattern == 'Morning Star' or amyLastPattern == 'Bullish Pin Bar') : amyRound5M15 ? amyLastPattern != 'Bearish Engulfing' : amyRound5H1 ? (amyLastPattern != 'Bearish Engulfing' and amyLastPattern != 'Evening Star') : true
amyPatternBiasActive := amyPatternContextQualified and amyPatternNameAllowed ? amyPatternCandidate : 0
"""
repl(old, new, 'pattern allowlist')

# 4) Target: preserve anti-leak ladder and candidate; publish only when distance/context quality is strong enough.
old = """float amyTarget = amyNextDirection == BULLISH ? amyNearestAbove(amyBullTargetBase, amyInternalBullTarget, na, na, amyBullTargetRef) : amyNearestBelow(amyBearTargetBase, amyInternalBearTarget, na, na, amyBearTargetRef)
string amyTargetSide = amyNextDirection == BULLISH ? 'BSL' : 'SSL'
"""
new = """float amyTargetCandidate = amyNextDirection == BULLISH ? amyNearestAbove(amyBullTargetBase, amyInternalBullTarget, na, na, amyBullTargetRef) : amyNearestBelow(amyBearTargetBase, amyInternalBearTarget, na, na, amyBearTargetRef)
float amyTargetDistanceRatio = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 ? math.abs(amyTargetCandidate - close) / amyTargetRiskDistance : na
bool amyTargetQualityOK = amyRound5M5 ? (not na(amyTargetDistanceRatio) and amyTargetDistanceRatio <= 0.40) : amyRound5M15 ? (not na(amyTargetDistanceRatio) and amyTargetDistanceRatio <= 1.00 and amyCurrentSwingBias == amyNextDirection) : amyRound5H1 ? (not na(amyTargetDistanceRatio) and amyTargetDistanceRatio <= 1.00) : true
float amyTarget = amyTargetQualityOK ? amyTargetCandidate : na
string amyTargetSide = amyNextDirection == BULLISH ? 'BSL' : 'SSL'
"""
repl(old, new, 'target quality gate')

p.write_text(s)
