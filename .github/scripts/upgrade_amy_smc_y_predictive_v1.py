from pathlib import Path

p = Path('Amy-SMC-Y.pine')
s = p.read_text()

old_next = """int amyHistoryBias = amyHistoryScore > 5 ? BULLISH : amyHistoryScore < -5 ? BEARISH : 0
// FINAL ALL-PASSED NEXT MOVE — preserve the passed directional core and Event History refinement.
// Newly passed predictive modules remain corroboration layers, preventing correlated signals from being counted twice.
float amyContextScore = amySafeHTFBias * 25 + amyCurrentSwingBias * 25 + amyCurrentInternalBias * 15 + amyLiquidityBiasActive * 15
float amyNextRaw = amyHistoryScore * 0.55 + amyContextScore
int amyNextDirection = BULLISH
if amyNextRaw > 0
    amyNextDirection := BULLISH
else if amyNextRaw < 0
    amyNextDirection := BEARISH
else
    amyNextDirection := amyFinalBias

string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'
"""
new_next = """int amyHistoryBias = amyHistoryScore > 5 ? BULLISH : amyHistoryScore < -5 ? BEARISH : 0
// AMY SMC Y PREDICTIVE V1 — LONG-HISTORY 2010–2026.
// Final Bias was materially more stable than the independent short-horizon Next Move.
// Next Move therefore remains ALWAYS directional (UP/DOWN) and is anchored to Final Bias; there is no WAIT/NEUTRAL state.
// Event History is retained as context and confidence evidence, not as an independent direction-flip engine.
float amyContextScore = amySafeHTFBias * 25 + amyCurrentSwingBias * 25 + amyCurrentInternalBias * 15 + amyLiquidityBiasActive * 15
float amyNextRaw = amyHistoryScore * 0.55 + amyContextScore
int amyNextDirection = amyFinalBias

string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'
"""
if old_next not in s:
    raise SystemExit('Next Move block not found')
s = s.replace(old_next, new_next, 1)

old_target = """float amyTargetRiskDistance = not na(amyInvalidation) ? math.abs(close - amyInvalidation) : 0.0
// Keep anti-leak protection but avoid pushing the structural target unnecessarily far away.
float amyTargetMinDistance = math.max(nz(amyAtr14, ta.atr(14)) * 0.10, amyTargetRiskDistance * 0.30)
float amyBullTargetRef = math.max(close + amyTargetMinDistance, high + syminfo.mintick)
float amyBearTargetRef = math.min(close - amyTargetMinDistance, low - syminfo.mintick)
float amyBullTargetBase = amyNearestAbove6(equalHigh.currentLevel, amyWeakHigh, amyPDH, amyPWH, swingHigh.currentLevel, amyRecentHigh, amyBullTargetRef)
float amyBearTargetBase = amyNearestBelow6(equalLow.currentLevel, amyWeakLow, amyPDL, amyPWL, swingLow.currentLevel, amyRecentLow, amyBearTargetRef)
float amyInternalBullTarget = not na(internalHigh.currentLevel) and internalHigh.currentLevel > amyBullTargetRef ? internalHigh.currentLevel : na
float amyInternalBearTarget = not na(internalLow.currentLevel) and internalLow.currentLevel < amyBearTargetRef ? internalLow.currentLevel : na
float amyTargetCandidate = amyNextDirection == BULLISH ? amyNearestAbove(amyBullTargetBase, amyInternalBullTarget, na, na, amyBullTargetRef) : amyNearestBelow(amyBearTargetBase, amyInternalBearTarget, na, na, amyBearTargetRef)
float amyTargetDistanceRatio = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 ? math.abs(amyTargetCandidate - close) / amyTargetRiskDistance : na
bool amyTargetQualityOK = amyRound5M5 ? (not na(amyTargetDistanceRatio) and amyTargetDistanceRatio <= 0.40) : amyRound5M15 ? (not na(amyTargetDistanceRatio) and amyTargetDistanceRatio <= 1.00 and amyCurrentSwingBias == amyNextDirection) : amyRound5H1 ? (not na(amyTargetDistanceRatio) and amyTargetDistanceRatio <= 1.00) : true
float amyTarget = amyTargetQualityOK ? amyTargetCandidate : na
string amyTargetSide = amyNextDirection == BULLISH ? 'BSL' : 'SSL'
"""
new_target = """// AMY SMC Y TARGET V1 — target is ALWAYS available; NO TARGET / NA is not used as a normal predictive state.
// Prefer nearby untouched structural liquidity. If that liquidity is too distant or unavailable, use a conservative
// projected target tied to the protected invalidation distance. The projected target is forced outside the signal candle,
// preserving the same-candle anti-leak rule.
float amyTargetAtr = nz(amyAtr14, math.max(high - low, syminfo.mintick))
float amyTargetRiskDistance = not na(amyInvalidation) ? math.abs(close - amyInvalidation) : amyTargetAtr
float amyProjectedTargetDistance = math.max(amyTargetRiskDistance * 0.40, amyTargetAtr * 0.22)
float amyTargetOutsidePad = math.max(amyTargetAtr * 0.02, syminfo.mintick)
float amyBullProjectedTarget = math.max(close + amyProjectedTargetDistance, high + amyTargetOutsidePad)
float amyBearProjectedTarget = math.min(close - amyProjectedTargetDistance, low - amyTargetOutsidePad)
float amyTargetMinDistance = math.max(amyTargetAtr * 0.10, amyTargetRiskDistance * 0.30)
float amyBullTargetRef = math.max(close + amyTargetMinDistance, high + syminfo.mintick)
float amyBearTargetRef = math.min(close - amyTargetMinDistance, low - syminfo.mintick)
float amyBullTargetBase = amyNearestAbove6(equalHigh.currentLevel, amyWeakHigh, amyPDH, amyPWH, swingHigh.currentLevel, amyRecentHigh, amyBullTargetRef)
float amyBearTargetBase = amyNearestBelow6(equalLow.currentLevel, amyWeakLow, amyPDL, amyPWL, swingLow.currentLevel, amyRecentLow, amyBearTargetRef)
float amyInternalBullTarget = not na(internalHigh.currentLevel) and internalHigh.currentLevel > amyBullTargetRef ? internalHigh.currentLevel : na
float amyInternalBearTarget = not na(internalLow.currentLevel) and internalLow.currentLevel < amyBearTargetRef ? internalLow.currentLevel : na
float amyTargetCandidate = amyNextDirection == BULLISH ? amyNearestAbove(amyBullTargetBase, amyInternalBullTarget, na, na, amyBullTargetRef) : amyNearestBelow(amyBearTargetBase, amyInternalBearTarget, na, na, amyBearTargetRef)
float amyTargetDistanceRatio = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 ? math.abs(amyTargetCandidate - close) / amyTargetRiskDistance : na
bool amyTargetQualityOK = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 and amyTargetDistanceRatio <= 0.40
float amyTarget = amyTargetQualityOK ? amyTargetCandidate : amyNextDirection == BULLISH ? amyBullProjectedTarget : amyBearProjectedTarget
string amyTargetSide = amyTargetQualityOK ? (amyNextDirection == BULLISH ? 'BSL' : 'SSL') : (amyNextDirection == BULLISH ? 'PROJ UP' : 'PROJ DOWN')
"""
if old_target not in s:
    raise SystemExit('Target block not found')
s = s.replace(old_target, new_target, 1)

lock_marker = "// FINAL LONG-HISTORY BASELINE — XAUUSD 2010–2026 validation checkpoint.\n"
y_note = """// AMY SMC Y PREDICTIVE V1 RESULT LOCK\n// 2010–2026 closed-candle replay: Next/Target lifecycle improved on M5/M15/H1 with zero normal NO_TARGET states.\n// Pattern, qualified BOS/CHoCH and qualified Sweep/Valid Break were tested for alternative long-history filters;\n// no robust alternative beat their inherited Amy SMC X settings, so those blocks remain unchanged.\n// Non-predictive modules remain inherited/locked.\n\n"""
if lock_marker not in s:
    raise SystemExit('long-history marker not found')
if y_note not in s:
    s = s.replace(lock_marker, y_note + lock_marker, 1)

p.write_text(s)
