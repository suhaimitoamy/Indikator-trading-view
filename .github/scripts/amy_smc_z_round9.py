from pathlib import Path

p = Path('Amy-SMC-Z.pine')
s = p.read_text()

old = """bool amyM5InternalTransitionRegime = amyRound5M5 and amySafeHTFBias != 0 and amySafeHTFBias == amyCurrentSwingBias and amyLiquidityBiasActive == amyCurrentSwingBias and amyCurrentInternalBias == -amyCurrentSwingBias
bool amyRound8M5TradeRegime = amyM5InternalTransitionRegime
bool amyRound8M5SweepWatch = amyRound5M5 and not amyRound8M5TradeRegime and amySweepContinuationQualified
string amyRound8Regime = amyRound5M5 ? (amyRound8M5TradeRegime ? 'TRADE • TRANSITION' : amyRound8M5SweepWatch ? 'WATCH • SWEEP' : 'WAIT') : 'R7 BASELINE'
int amyNextDirection = amyRound5M5 ? (amyRound8M5TradeRegime ? amyCurrentInternalBias : 0) : amyFinalBias
// H1 keeps the previously accepted confirmed-sweep-candle override. M15 remains the Round-7 baseline.
if amyRound5H1 and amySweepContinuationQualified
    amyNextDirection := amySweepContinuationBias
"""

new = """bool amyM5InternalTransitionRegime = amyRound5M5 and amySafeHTFBias != 0 and amySafeHTFBias == amyCurrentSwingBias and amyLiquidityBiasActive == amyCurrentSwingBias and amyCurrentInternalBias == -amyCurrentSwingBias
bool amyRound8M5TradeRegime = amyM5InternalTransitionRegime

// AMY SMC Z ROUND 9 — CONFIRMED TRANSITION EXECUTION GATE.
// Round 8 proved the Internal Transition regime robustly, but not every transition entry had equal execution quality.
// Round 9 keeps the regime only when the ENTRY candle closes in the new Internal direction and the protected
// structural invalidation is at least 3 ATR away. This 3 ATR structural-room gate improved directional precision
// and Target V1 lifecycle in train, validation and holdout; it does not shorten the target or use future candles.
bool amyRound9M5RegimeEntry = amyRound8M5TradeRegime and not amyRound8M5TradeRegime[1]
float amyRound9EntryInvalidation = amyCurrentInternalBias == BULLISH ? amyBullInvalidation : amyCurrentInternalBias == BEARISH ? amyBearInvalidation : na
float amyRound9EntryRiskAtr = not na(amyRound9EntryInvalidation) and not na(amyEventAtr) and amyEventAtr > 0 ? math.abs(close - amyRound9EntryInvalidation) / amyEventAtr : na
bool amyRound9CandleConfirm = amyCurrentInternalBias == BULLISH ? close > open : amyCurrentInternalBias == BEARISH ? close < open : false
bool amyRound9EntryConfirmed = amyRound9CandleConfirm and not na(amyRound9EntryRiskAtr) and amyRound9EntryRiskAtr >= 3.0
var int amyRound9M5TradeDirection = 0
if barstate.isconfirmed
    if not amyRound8M5TradeRegime
        amyRound9M5TradeDirection := 0
    else if amyRound9M5RegimeEntry
        amyRound9M5TradeDirection := amyRound9EntryConfirmed ? amyCurrentInternalBias : 0

bool amyRound9M5TradeRegime = amyRound8M5TradeRegime and amyRound9M5TradeDirection != 0
bool amyRound9M5SweepWatch = amyRound5M5 and not amyRound9M5TradeRegime and amySweepContinuationQualified
bool amyRound9M5TransitionWatch = amyRound5M5 and amyRound8M5TradeRegime and not amyRound9M5TradeRegime
string amyRound9Regime = amyRound5M5 ? (amyRound9M5TradeRegime ? 'TRADE • CONFIRMED' : amyRound9M5SweepWatch ? 'WATCH • SWEEP' : amyRound9M5TransitionWatch ? 'WATCH • TRANSITION' : 'WAIT') : 'R8 BASELINE'
int amyNextDirection = amyRound5M5 ? (amyRound9M5TradeRegime ? amyRound9M5TradeDirection : 0) : amyFinalBias
// H1 keeps the previously accepted confirmed-sweep-candle override. M15 remains the retained baseline.
if amyRound5H1 and amySweepContinuationQualified
    amyNextDirection := amySweepContinuationBias
"""

if old not in s:
    raise SystemExit('Round 8 regime block not found')
s = s.replace(old, new, 1)

s = s.replace("table.cell(amyDashboard, 1, 10, amyRound8Regime, text_color = amyRound8M5TradeRegime ? amyNextColor : amyRound8M5SweepWatch ? color.orange : color.silver, text_size = size.tiny)",
              "table.cell(amyDashboard, 1, 10, amyRound9Regime, text_color = amyRound9M5TradeRegime ? amyNextColor : (amyRound9M5SweepWatch or amyRound9M5TransitionWatch) ? color.orange : color.silver, text_size = size.tiny)", 1)

old_lock = """// AMY SMC Z ROUND 8 RESULT LOCK
// M5 is selectively actionable only in the validated Internal Transition regime; otherwise it may show WATCH/WAIT.
// M15/H1 retain their Round-7 Next/Target logic because tested regime gates did not improve robust lifecycle evidence.
// Pattern, CHoCH, Valid Break and descriptive modules keep their accepted independent roles and are not double-counted.
"""
new_lock = """// AMY SMC Z ROUND 9 RESULT LOCK
// M5 execution now requires a confirmed Internal Transition entry candle plus >=3 ATR structural room to invalidation.
// Rejected Round-8 transition entries remain WATCH/WAIT rather than forced predictions; Sweep remains WATCH context.
// M15/H1 keep their retained baseline because Round-9 candle-confirmation gates worsened validation/holdout lifecycle.
// Pattern, CHoCH, Valid Break and descriptive modules keep their accepted independent roles and are not double-counted.
"""
if old_lock not in s:
    raise SystemExit('Round 8 lock comment not found')
s = s.replace(old_lock, new_lock, 1)

# Guardrails.
assert "amyRound9EntryRiskAtr >= 3.0" in s
assert "amyRound9CandleConfirm" in s
assert "amyRound9M5TradeDirection" in s
assert "TRADE • CONFIRMED" in s
assert "WATCH • TRANSITION" in s
assert "amyRound9Regime" in s
assert "float amyProjectedTargetDistance = math.max(amyTargetRiskDistance * 0.40, amyTargetAtr * 0.22)" in s
assert "Amy SMC Z OF16" not in s
p.write_text(s)
