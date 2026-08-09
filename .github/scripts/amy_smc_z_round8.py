from pathlib import Path

p = Path('Amy-SMC-Z.pine')
s = p.read_text()

old_next = """// AMY SMC Y ROUND 5 — 16-YEAR CONDITIONAL NEXT MOVE.
// Next Move remains ALWAYS UP/DOWN. Final Bias is still the default anchor. Overrides are allowed only for
// conditional states that improved the 2010–2026 apples-to-apples replay and all train/validation/holdout partitions.
// M5 transition regime: HTF + Swing + active Liquidity still agree, but Internal has already flipped. Across 16 years
// this state resolved toward Internal often enough to beat the linear Final Bias, so M5 follows Internal here.
bool amyM5InternalTransitionRegime = amyRound5M5 and amySafeHTFBias != 0 and amySafeHTFBias == amyCurrentSwingBias and amyLiquidityBiasActive == amyCurrentSwingBias and amyCurrentInternalBias == -amyCurrentSwingBias
int amyNextDirection = amyM5InternalTransitionRegime ? amyCurrentInternalBias : amyFinalBias
// M5 Round-5 Bearish Engulfing is a high-reliability conditional reversal family; when it is promoted, it wins priority.
if amyRound5M5 and amyPatternRound5Qualified and amyPatternCandidate == BEARISH
    amyNextDirection := BEARISH
// H1 uses a qualifying raw sweep only on the confirmed sweep candle. The forward direction is the continuation side
// discovered in the long-history replay (opposite the raw sweep bias) and Internal Structure must already agree.
if amyRound5H1 and amySweepContinuationQualified
    amyNextDirection := amySweepContinuationBias

string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'
// Keep the accepted invalidation geometry unchanged, but select the already-computed bullish/bearish side from the
// actual Next Move direction so a Round-5 override cannot pair an UP target with a bearish-side invalidation (or vice versa).
float amyExecutionInvalidation = amyNextDirection == BULLISH ? amyBullInvalidation : amyBearInvalidation
"""
new_next = """// AMY SMC Z ROUND 8 — REGIME-ADAPTIVE NEXT MOVE.
// The 2010–2026 replay found that M5 Internal Transition is the only selective execution regime that improved
// train, validation, holdout and full-history Target V1 lifecycle together. M5 therefore predicts only when that
// regime is active; outside it the dashboard explicitly waits instead of forcing a low-quality UP/DOWN call.
// Sweep continuation remains a high-precision directional WATCH context, but it is not promoted to a target-backed
// M5 execution call because adding it produced only a marginal lifecycle gain. M15/H1 regime-gating candidates were
// rolled back, so those timeframes retain the accepted Round-7 behavior.
bool amyM5InternalTransitionRegime = amyRound5M5 and amySafeHTFBias != 0 and amySafeHTFBias == amyCurrentSwingBias and amyLiquidityBiasActive == amyCurrentSwingBias and amyCurrentInternalBias == -amyCurrentSwingBias
bool amyRound8M5TradeRegime = amyM5InternalTransitionRegime
bool amyRound8M5SweepWatch = amyRound5M5 and not amyRound8M5TradeRegime and amySweepContinuationQualified
string amyRound8Regime = amyRound5M5 ? (amyRound8M5TradeRegime ? 'TRADE • TRANSITION' : amyRound8M5SweepWatch ? 'WATCH • SWEEP' : 'WAIT') : 'R7 BASELINE'
int amyNextDirection = amyRound5M5 ? (amyRound8M5TradeRegime ? amyCurrentInternalBias : 0) : amyFinalBias
// H1 keeps the previously accepted confirmed-sweep-candle override. M15 remains the Round-7 baseline.
if amyRound5H1 and amySweepContinuationQualified
    amyNextDirection := amySweepContinuationBias

bool amyHasExecutionSignal = amyNextDirection != 0
string amyNextMove = amyNextDirection == BULLISH ? 'UP' : amyNextDirection == BEARISH ? 'DOWN' : 'WAIT'
// Select invalidation from the actual execution direction. WAIT has no synthetic invalidation/target.
float amyExecutionInvalidation = amyNextDirection == BULLISH ? amyBullInvalidation : amyNextDirection == BEARISH ? amyBearInvalidation : na
"""
if old_next not in s:
    raise SystemExit('Round 7 Next block not found')
s = s.replace(old_next, new_next, 1)

old_target = """float amyTargetCandidate = amyNextDirection == BULLISH ? amyNearestAbove(amyBullTargetBase, amyInternalBullTarget, na, na, amyBullTargetRef) : amyNearestBelow(amyBearTargetBase, amyInternalBearTarget, na, na, amyBearTargetRef)
float amyTargetDistanceRatio = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 ? math.abs(amyTargetCandidate - close) / amyTargetRiskDistance : na
bool amyTargetQualityOK = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 and amyTargetDistanceRatio <= 0.40
float amyTarget = amyTargetQualityOK ? amyTargetCandidate : amyNextDirection == BULLISH ? amyBullProjectedTarget : amyBearProjectedTarget
string amyTargetSide = amyTargetQualityOK ? (amyNextDirection == BULLISH ? 'BSL' : 'SSL') : (amyNextDirection == BULLISH ? 'PROJ UP' : 'PROJ DOWN')
"""
new_target = """float amyTargetCandidate = not amyHasExecutionSignal ? na : amyNextDirection == BULLISH ? amyNearestAbove(amyBullTargetBase, amyInternalBullTarget, na, na, amyBullTargetRef) : amyNearestBelow(amyBearTargetBase, amyInternalBearTarget, na, na, amyBearTargetRef)
float amyTargetDistanceRatio = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 ? math.abs(amyTargetCandidate - close) / amyTargetRiskDistance : na
bool amyTargetQualityOK = amyHasExecutionSignal and not na(amyTargetCandidate) and amyTargetRiskDistance > 0 and amyTargetDistanceRatio <= 0.40
float amyTarget = not amyHasExecutionSignal ? na : amyTargetQualityOK ? amyTargetCandidate : amyNextDirection == BULLISH ? amyBullProjectedTarget : amyBearProjectedTarget
string amyTargetSide = not amyHasExecutionSignal ? 'WAIT' : amyTargetQualityOK ? (amyNextDirection == BULLISH ? 'BSL' : 'SSL') : (amyNextDirection == BULLISH ? 'PROJ UP' : 'PROJ DOWN')
"""
if old_target not in s:
    raise SystemExit('Target block not found')
s = s.replace(old_target, new_target, 1)

old_conf = """// Confidence measures agreement across accepted components only.
float amyConfidenceRaw = 50.0
if amySafeHTFBias != 0
    amyConfidenceRaw += amySafeHTFBias == amyNextDirection ? 8 : -8
if amyCurrentSwingBias != 0
    amyConfidenceRaw += amyCurrentSwingBias == amyNextDirection ? 10 : -10
if amyCurrentInternalBias != 0
    amyConfidenceRaw += amyCurrentInternalBias == amyNextDirection ? 6 : -6
if amyLiquidityBiasActive != 0
    amyConfidenceRaw += amyLiquidityBiasActive == amyNextDirection ? 6 : -6
if amyHistoryBias != 0
    amyConfidenceRaw += amyHistoryBias == amyNextDirection ? 5 : -5
if math.abs(amyNextRaw) < 18
    amyConfidenceRaw -= 5
int amyConfidence = int(math.round(math.max(35.0, math.min(85.0, amyConfidenceRaw))))
"""
new_conf = """// Confidence measures agreement only when an actionable prediction exists.
float amyConfidenceRaw = amyHasExecutionSignal ? 50.0 : 0.0
if amyHasExecutionSignal and amySafeHTFBias != 0
    amyConfidenceRaw += amySafeHTFBias == amyNextDirection ? 8 : -8
if amyHasExecutionSignal and amyCurrentSwingBias != 0
    amyConfidenceRaw += amyCurrentSwingBias == amyNextDirection ? 10 : -10
if amyHasExecutionSignal and amyCurrentInternalBias != 0
    amyConfidenceRaw += amyCurrentInternalBias == amyNextDirection ? 6 : -6
if amyHasExecutionSignal and amyLiquidityBiasActive != 0
    amyConfidenceRaw += amyLiquidityBiasActive == amyNextDirection ? 6 : -6
if amyHasExecutionSignal and amyHistoryBias != 0
    amyConfidenceRaw += amyHistoryBias == amyNextDirection ? 5 : -5
if amyHasExecutionSignal and math.abs(amyNextRaw) < 18
    amyConfidenceRaw -= 5
int amyConfidence = amyHasExecutionSignal ? int(math.round(math.max(35.0, math.min(85.0, amyConfidenceRaw)))) : 0
"""
if old_conf not in s:
    raise SystemExit('Confidence block not found')
s = s.replace(old_conf, new_conf, 1)

s = s.replace("table.merge_cells(amyDashboard, 0, 11, 1, 11)", "table.merge_cells(amyDashboard, 0, 12, 1, 12)", 1)
s = s.replace("color amyNextColor = amyNextDirection == BULLISH ? amyBullColor : amyBearColor", "color amyNextColor = amyNextDirection == BULLISH ? amyBullColor : amyNextDirection == BEARISH ? amyBearColor : GRAY", 1)

old_rows = """        table.cell(amyDashboard, 0, 9, 'Target', text_color = color.silver, text_size = size.tiny)
        table.cell(amyDashboard, 1, 9, amyTargetSide + ' ' + amyPrice(amyTarget), text_color = color.white, text_size = size.tiny)
        table.cell(amyDashboard, 0, 10, 'Confidence', text_color = color.silver, text_size = size.tiny)
        table.cell(amyDashboard, 1, 10, str.tostring(amyConfidence) + '%', text_color = amyNextColor, text_size = size.tiny)
        table.cell(amyDashboard, 0, 11, 'EVENT HISTORY', bgcolor = color.new(GRAY, 82), text_color = color.white, text_size = size.tiny)
        for historyIndex = 0 to 3
            int historyRow = 12 + historyIndex
"""
new_rows = """        table.cell(amyDashboard, 0, 9, 'Target', text_color = color.silver, text_size = size.tiny)
        table.cell(amyDashboard, 1, 9, amyHasExecutionSignal ? amyTargetSide + ' ' + amyPrice(amyTarget) : '-', text_color = color.white, text_size = size.tiny)
        table.cell(amyDashboard, 0, 10, 'Regime', text_color = color.silver, text_size = size.tiny)
        table.cell(amyDashboard, 1, 10, amyRound8Regime, text_color = amyRound8M5TradeRegime ? amyNextColor : amyRound8M5SweepWatch ? color.orange : color.silver, text_size = size.tiny)
        table.cell(amyDashboard, 0, 11, 'Confidence', text_color = color.silver, text_size = size.tiny)
        table.cell(amyDashboard, 1, 11, amyHasExecutionSignal ? str.tostring(amyConfidence) + '%' : '-', text_color = amyNextColor, text_size = size.tiny)
        table.cell(amyDashboard, 0, 12, 'EVENT HISTORY', bgcolor = color.new(GRAY, 82), text_color = color.white, text_size = size.tiny)
        for historyIndex = 0 to 2
            int historyRow = 13 + historyIndex
"""
if old_rows not in s:
    raise SystemExit('Dashboard row block not found')
s = s.replace(old_rows, new_rows, 1)

old_lock = """// AMY SMC Y PREDICTIVE V1 RESULT LOCK
// 2010–2026 closed-candle replay: Next/Target lifecycle improved on M5/M15/H1 with zero normal NO_TARGET states.
// Pattern, qualified BOS/CHoCH and qualified Sweep/Valid Break were tested for alternative long-history filters;
// no robust alternative beat their inherited Amy SMC X settings, so those blocks remain unchanged.
// Non-predictive modules remain inherited/locked.
"""
new_lock = """// AMY SMC Z ROUND 8 RESULT LOCK
// M5 is selectively actionable only in the validated Internal Transition regime; otherwise it may show WATCH/WAIT.
// M15/H1 retain their Round-7 Next/Target logic because tested regime gates did not improve robust lifecycle evidence.
// Pattern, CHoCH, Valid Break and descriptive modules keep their accepted independent roles and are not double-counted.
"""
if old_lock not in s:
    raise SystemExit('Result lock block not found')
s = s.replace(old_lock, new_lock, 1)

alert_anchor = "alertcondition(barstate.isconfirmed and amyPatternBiasActive != 0, 'Candlestick Pattern', 'Context-qualified candlestick pattern detected')"
if alert_anchor not in s:
    raise SystemExit('Alert anchor not found')
s = s.replace(alert_anchor, alert_anchor + "\nalertcondition(barstate.isconfirmed and amyRound5M5 and amyRound8M5TradeRegime, 'Round 8 Regime Signal', 'Amy SMC Z Round 8 M5 Internal Transition regime is actionable')", 1)

# Guardrails: only Z is written by this script; Round 7 target geometry is retained; no lookahead added.
assert "TRADE • TRANSITION" in s
assert "WATCH • SWEEP" in s
assert "amyRound5M5 ? (amyRound8M5TradeRegime ? amyCurrentInternalBias : 0) : amyFinalBias" in s
assert "string amyNextMove = amyNextDirection == BULLISH ? 'UP' : amyNextDirection == BEARISH ? 'DOWN' : 'WAIT'" in s
assert "float amyProjectedTargetDistance = math.max(amyTargetRiskDistance * 0.40, amyTargetAtr * 0.22)" in s
assert "float amyTargetMinDistance = math.max(amyTargetAtr * 0.10, amyTargetRiskDistance * 0.30)" in s
assert "amyTargetDistanceRatio <= 0.40" in s
assert "for historyIndex = 0 to 2" in s
assert "table.merge_cells(amyDashboard, 0, 12, 1, 12)" in s

p.write_text(s)
