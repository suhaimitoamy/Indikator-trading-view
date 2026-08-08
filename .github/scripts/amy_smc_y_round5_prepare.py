from pathlib import Path

p = Path('Amy-SMC-Y.pine')
s = p.read_text()

old_liq = """float amyBreakBodyAtr = not na(amyEventAtr) and amyEventAtr > 0 ? amyEventBody / amyEventAtr : 0.0
// On the tested M5/M15/H1 profiles a sweep remains context, not a predictive call, until a stronger confirmation exists.
bool amyQualifiedBSLSweep = amyRound5TestTF ? false : amyQualifiedBSLSweepBase
bool amyQualifiedSSLSweep = amyRound5TestTF ? false : amyQualifiedSSLSweepBase
// AMY SMC Y ROUND 4 — M5 Valid Break predictive promotion.
// Raw liquidity events remain unchanged. Only the M5 forward-predictive promotion is made more selective.
bool amyQualifiedBSLValidBreak = amyRound5M5 ? (amyQualifiedBSLValidBreakBase and internalTrend.bias == BULLISH and amyEventHTFBullOK and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.80) : amyRound5M15 ? (amyQualifiedBSLValidBreakBase and internalTrend.bias == BULLISH and amyEventHTFBullOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedBSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedBSLValidBreakBase
bool amyQualifiedSSLValidBreak = amyRound5M5 ? (amyQualifiedSSLValidBreakBase and internalTrend.bias == BEARISH and amyEventHTFBearOK and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.80) : amyRound5M15 ? (amyQualifiedSSLValidBreakBase and internalTrend.bias == BEARISH and amyEventHTFBearOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedSSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedSSLValidBreakBase
"""
new_liq = """float amyBreakBodyAtr = not na(amyEventAtr) and amyEventAtr > 0 ? amyEventBody / amyEventAtr : 0.0
// AMY SMC Y ROUND 5 CANDIDATE — regime-aware liquidity prediction.
// Raw Sweep / Valid Break events are untouched. Predictive promotion is split by task:
// Sweep = reversal/reclaim hypothesis, Valid Break = continuation hypothesis.
float amyUpperWick = high - math.max(open, close)
float amyLowerWick = math.min(open, close) - low
float amyUpperWickRatio = amyEventRange > 0 ? amyUpperWick / amyEventRange : 0.0
float amyLowerWickRatio = amyEventRange > 0 ? amyLowerWick / amyEventRange : 0.0
bool amyBullTrendRegime = swingTrend.bias == BULLISH and internalTrend.bias == BULLISH and amyEventHTFBullOK
bool amyBearTrendRegime = swingTrend.bias == BEARISH and internalTrend.bias == BEARISH and amyEventHTFBearOK
bool amyBullSweepReclaim = close > open and amyLowerWickRatio >= 0.30 and amyEventRange > 0 and (close - low) / amyEventRange >= 0.70
bool amyBearSweepReclaim = close < open and amyUpperWickRatio >= 0.30 and amyEventRange > 0 and (high - close) / amyEventRange >= 0.70
bool amyQualifiedBSLSweep = amyRound5M5 ? (amyQualifiedBSLSweepBase and amyBearSweepReclaim and internalTrend.bias == BEARISH and amyEventHTFBearOK) : amyRound5M15 ? (amyQualifiedBSLSweepBase and amyBearSweepReclaim and internalTrend.bias == BEARISH) : amyRound5H1 ? (amyQualifiedBSLSweepBase and amyBearSweepReclaim and internalTrend.bias == BEARISH) : amyQualifiedBSLSweepBase
bool amyQualifiedSSLSweep = amyRound5M5 ? (amyQualifiedSSLSweepBase and amyBullSweepReclaim and internalTrend.bias == BULLISH and amyEventHTFBullOK) : amyRound5M15 ? (amyQualifiedSSLSweepBase and amyBullSweepReclaim and internalTrend.bias == BULLISH) : amyRound5H1 ? (amyQualifiedSSLSweepBase and amyBullSweepReclaim and internalTrend.bias == BULLISH) : amyQualifiedSSLSweepBase
// Keep the accepted M5 Round 4 profile. Round 5 only prepares stronger continuation profiles for M15/H1.
bool amyQualifiedBSLValidBreak = amyRound5M5 ? (amyQualifiedBSLValidBreakBase and internalTrend.bias == BULLISH and amyEventHTFBullOK and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.80) : amyRound5M15 ? (amyQualifiedBSLValidBreakBase and amyBullTrendRegime and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.70) : amyRound5H1 ? (amyQualifiedBSLValidBreakBase and amyBullTrendRegime and amyBreakBodyAtr >= 0.75 and amyEventBodyRatio >= 0.72) : amyQualifiedBSLValidBreakBase
bool amyQualifiedSSLValidBreak = amyRound5M5 ? (amyQualifiedSSLValidBreakBase and internalTrend.bias == BEARISH and amyEventHTFBearOK and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.80) : amyRound5M15 ? (amyQualifiedSSLValidBreakBase and amyBearTrendRegime and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.70) : amyRound5H1 ? (amyQualifiedSSLValidBreakBase and amyBearTrendRegime and amyBreakBodyAtr >= 0.75 and amyEventBodyRatio >= 0.72) : amyQualifiedSSLValidBreakBase
"""
if old_liq not in s:
    raise SystemExit('liquidity block not found')
s = s.replace(old_liq, new_liq, 1)

old_struct = """float amyBullCHoCHExcursionAtr = not na(amyEventAtr) and amyEventAtr > 0 and not na(swingHigh.currentLevel) ? (close - swingHigh.currentLevel) / amyEventAtr : 0.0
float amyBearCHoCHExcursionAtr = not na(amyEventAtr) and amyEventAtr > 0 and not na(swingLow.currentLevel) ? (swingLow.currentLevel - close) / amyEventAtr : 0.0
bool amyQualifiedSwingBullBOS = amyRound5TestTF ? false : amyBaseQualifiedSwingBullBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH)
bool amyQualifiedSwingBearBOS = amyRound5TestTF ? false : amyBaseQualifiedSwingBearBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH)
"""
new_struct = """float amyBullCHoCHExcursionAtr = not na(amyEventAtr) and amyEventAtr > 0 and not na(swingHigh.currentLevel) ? (close - swingHigh.currentLevel) / amyEventAtr : 0.0
float amyBearCHoCHExcursionAtr = not na(amyEventAtr) and amyEventAtr > 0 and not na(swingLow.currentLevel) ? (swingLow.currentLevel - close) / amyEventAtr : 0.0
float amyBullBOSExcursionAtr = not na(amyEventAtr) and amyEventAtr > 0 and not na(swingHigh.currentLevel) ? (close - swingHigh.currentLevel) / amyEventAtr : 0.0
float amyBearBOSExcursionAtr = not na(amyEventAtr) and amyEventAtr > 0 and not na(swingLow.currentLevel) ? (swingLow.currentLevel - close) / amyEventAtr : 0.0
// AMY SMC Y ROUND 5 CANDIDATE — BOS is evaluated as continuation, separately from CHoCH reversal.
// Base BOS/CHoCH remains frozen for OTE/Fibonacci; only forward-predictive promotion changes here.
bool amyQualifiedSwingBullBOS = amyRound5M5 ? (amyBaseQualifiedSwingBullBOS and amyBullTrendRegime and amyBreakBodyAtr >= 1.25 and amyEventBodyRatio >= 0.70 and amyBullBOSExcursionAtr >= 0.15) : amyRound5M15 ? (amyBaseQualifiedSwingBullBOS and amyBullTrendRegime and amyBreakBodyAtr >= 1.00 and amyEventBodyRatio >= 0.70 and amyBullBOSExcursionAtr >= 0.15) : amyRound5H1 ? (amyBaseQualifiedSwingBullBOS and amyBullTrendRegime and amyBreakBodyAtr >= 0.70 and amyEventBodyRatio >= 0.68 and amyBullBOSExcursionAtr >= 0.10) : amyBaseQualifiedSwingBullBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH)
bool amyQualifiedSwingBearBOS = amyRound5M5 ? (amyBaseQualifiedSwingBearBOS and amyBearTrendRegime and amyBreakBodyAtr >= 1.25 and amyEventBodyRatio >= 0.70 and amyBearBOSExcursionAtr >= 0.15) : amyRound5M15 ? (amyBaseQualifiedSwingBearBOS and amyBearTrendRegime and amyBreakBodyAtr >= 1.00 and amyEventBodyRatio >= 0.70 and amyBearBOSExcursionAtr >= 0.15) : amyRound5H1 ? (amyBaseQualifiedSwingBearBOS and amyBearTrendRegime and amyBreakBodyAtr >= 0.70 and amyEventBodyRatio >= 0.68 and amyBearBOSExcursionAtr >= 0.10) : amyBaseQualifiedSwingBearBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH)
"""
if old_struct not in s:
    raise SystemExit('structure block not found')
s = s.replace(old_struct, new_struct, 1)

old_pattern = """amyPatternBiasActive := amyPatternRound4Qualified ? amyPatternCandidate : 0

// FINAL ALL-PASSED CHECKPOINT — all accepted Amy SMC X modules are consolidated in this file.
"""
new_pattern = """// AMY SMC Y ROUND 5 CANDIDATE — add regime consistency without adding new pattern detectors.
bool amyPatternRound5Qualified = amyPatternRound4Qualified
if amyPatternCandidate != 0 and amyPatternRound4Qualified
    if amyRound5M5
        amyPatternRound5Qualified := (amyCurrentInternalBias == amyPatternCandidate or amyPatternLiquidityConfirm) and amyPatternOpposes <= 2
    else if amyRound5M15
        amyPatternRound5Qualified := amyCurrentInternalBias == amyPatternCandidate
    else if amyRound5H1
        amyPatternRound5Qualified := amyCurrentSwingBias != -amyPatternCandidate
amyPatternBiasActive := amyPatternRound5Qualified ? amyPatternCandidate : 0

// FINAL ALL-PASSED CHECKPOINT — all accepted Amy SMC X modules are consolidated in this file.
"""
if old_pattern not in s:
    raise SystemExit('pattern block not found')
s = s.replace(old_pattern, new_pattern, 1)

old_next = """float amyContextScore = amySafeHTFBias * 25 + amyCurrentSwingBias * 25 + amyCurrentInternalBias * 15 + amyLiquidityBiasActive * 15
float amyNextRaw = amyHistoryScore * 0.55 + amyContextScore
int amyNextDirection = amyFinalBias

string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'
"""
new_next = """float amyContextScore = amySafeHTFBias * 25 + amyCurrentSwingBias * 25 + amyCurrentInternalBias * 15 + amyLiquidityBiasActive * 15
float amyNextRaw = amyHistoryScore * 0.55 + amyContextScore
// AMY SMC Y ROUND 5 CANDIDATE — selective predictor corroboration, still ALWAYS UP/DOWN.
// Final Bias remains the anchor. A flip is allowed only when the core score is weak and at least two independent
// predictive layers agree against the anchor. There is no WAIT/NEUTRAL state.
int amyPatternPredictiveBias = amyPatternBiasActive
int amyStructurePredictiveBias = (amyQualifiedSwingBullBOS or amyQualifiedSwingBullCHoCH) ? BULLISH : (amyQualifiedSwingBearBOS or amyQualifiedSwingBearCHoCH) ? BEARISH : 0
int amyLiquidityPredictiveBias = (amyQualifiedSSLSweep or amyQualifiedBSLValidBreak) ? BULLISH : (amyQualifiedBSLSweep or amyQualifiedSSLValidBreak) ? BEARISH : 0
int amyPredictiveBullVotes = (amyPatternPredictiveBias == BULLISH ? 1 : 0) + (amyStructurePredictiveBias == BULLISH ? 1 : 0) + (amyLiquidityPredictiveBias == BULLISH ? 1 : 0)
int amyPredictiveBearVotes = (amyPatternPredictiveBias == BEARISH ? 1 : 0) + (amyStructurePredictiveBias == BEARISH ? 1 : 0) + (amyLiquidityPredictiveBias == BEARISH ? 1 : 0)
int amyPredictiveConsensus = amyPredictiveBullVotes >= 2 and amyPredictiveBullVotes > amyPredictiveBearVotes ? BULLISH : amyPredictiveBearVotes >= 2 and amyPredictiveBearVotes > amyPredictiveBullVotes ? BEARISH : 0
bool amyCorePredictionWeak = math.abs(amyFinalScore) <= 25
bool amyPredictiveOverride = amyCorePredictionWeak and amyPredictiveConsensus != 0 and amyPredictiveConsensus != amyFinalBias
int amyNextDirection = amyPredictiveOverride ? amyPredictiveConsensus : amyFinalBias

string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'
"""
if old_next not in s:
    raise SystemExit('next block not found')
s = s.replace(old_next, new_next, 1)

p.write_text(s)
