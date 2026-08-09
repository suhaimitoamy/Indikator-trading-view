from pathlib import Path

p = Path('Amy-SMC-Z.pine')
s = p.read_text()

old = """bool amyRound9M5TradeRegime = amyRound8M5TradeRegime and amyRound9M5TradeDirection != 0
bool amyRound9M5SweepWatch = amyRound5M5 and not amyRound9M5TradeRegime and amySweepContinuationQualified
bool amyRound9M5TransitionWatch = amyRound5M5 and amyRound8M5TradeRegime and not amyRound9M5TradeRegime
string amyRound9Regime = amyRound5M5 ? (amyRound9M5TradeRegime ? 'TRADE • CONFIRMED' : amyRound9M5SweepWatch ? 'WATCH • SWEEP' : amyRound9M5TransitionWatch ? 'WATCH • TRANSITION' : 'WAIT') : 'R8 BASELINE'
int amyNextDirection = amyRound5M5 ? (amyRound9M5TradeRegime ? amyRound9M5TradeDirection : 0) : amyFinalBias
"""
new = """bool amyRound9M5TradeRegime = amyRound8M5TradeRegime and amyRound9M5TradeDirection != 0

// AMY SMC Z ROUND 10 — QUALITY GRADE, NOT A CORE FILTER.
// Train + validation selected a cleaner confirmed-transition subset: entry body 0.50–2.50 ATR,
// body/range >= 0.30 and structural room < 8 ATR (Round 9 already enforces >= 3 ATR).
// Its Target V1 lifecycle improved strongly, but holdout directional precision was lower by one historical hit.
// Therefore Round 10 does NOT discard the retained Round-9 trades. It grades the cleaner subset A+ and keeps
// the remaining already-valid Round-9 trades as A. Next Move, Target V1 and invalidation logic stay unchanged.
float amyRound10EntryBodyAtr = not na(amyEventAtr) and amyEventAtr > 0 ? amyEventBody / amyEventAtr : na
bool amyRound10EntryAPlusQualified = amyRound9EntryConfirmed and not na(amyRound10EntryBodyAtr) and amyRound10EntryBodyAtr >= 0.50 and amyRound10EntryBodyAtr < 2.50 and amyEventBodyRatio >= 0.30 and amyRound9EntryRiskAtr < 8.0
var bool amyRound10M5APlus = false
if barstate.isconfirmed
    if not amyRound9M5TradeRegime
        amyRound10M5APlus := false
    else if amyRound9M5RegimeEntry
        amyRound10M5APlus := amyRound10EntryAPlusQualified

bool amyRound9M5SweepWatch = amyRound5M5 and not amyRound9M5TradeRegime and amySweepContinuationQualified
bool amyRound9M5TransitionWatch = amyRound5M5 and amyRound8M5TradeRegime and not amyRound9M5TradeRegime
string amyRound10Regime = amyRound5M5 ? (amyRound9M5TradeRegime ? (amyRound10M5APlus ? 'TRADE • A+' : 'TRADE • A') : amyRound9M5SweepWatch ? 'WATCH • SWEEP' : amyRound9M5TransitionWatch ? 'WATCH • TRANSITION' : 'WAIT') : 'R9 BASELINE'
int amyNextDirection = amyRound5M5 ? (amyRound9M5TradeRegime ? amyRound9M5TradeDirection : 0) : amyFinalBias
"""
if old not in s:
    raise SystemExit('Round 9 regime anchor not found')
s = s.replace(old, new, 1)

old_dash = "table.cell(amyDashboard, 1, 10, amyRound9Regime, text_color = amyRound9M5TradeRegime ? amyNextColor : (amyRound9M5SweepWatch or amyRound9M5TransitionWatch) ? color.orange : color.silver, text_size = size.tiny)"
new_dash = "table.cell(amyDashboard, 1, 10, amyRound10Regime, text_color = amyRound9M5TradeRegime ? amyNextColor : (amyRound9M5SweepWatch or amyRound9M5TransitionWatch) ? color.orange : color.silver, text_size = size.tiny)"
if old_dash not in s:
    raise SystemExit('dashboard regime anchor not found')
s = s.replace(old_dash, new_dash, 1)

old_lock = """// AMY SMC Z ROUND 9 RESULT LOCK
// M5 execution now requires a confirmed Internal Transition entry candle plus >=3 ATR structural room to invalidation.
// Rejected Round-8 transition entries remain WATCH/WAIT rather than forced predictions; Sweep remains WATCH context.
// M15/H1 keep their retained baseline because Round-9 candle-confirmation gates worsened validation/holdout lifecycle.
// Pattern, CHoCH, Valid Break and descriptive modules keep their accepted independent roles and are not double-counted.
"""
new_lock = """// AMY SMC Z ROUND 10 RESULT LOCK
// Round 9 remains the execution baseline: confirmed Internal Transition + >=3 ATR structural room.
// Round 10 adds only evidence-backed quality grading: A+ is the cleaner body/risk subset; A keeps every other
// already-valid Round-9 trade. The A+ subset was NOT allowed to replace A because holdout directional precision
// was lower by one historical hit despite materially better Target V1 lifecycle. This preserves the best-of rule.
// M15/H1 and all previously strong descriptive modules remain unchanged.
"""
if old_lock not in s:
    raise SystemExit('Round 9 result lock anchor not found')
s = s.replace(old_lock, new_lock, 1)

assert "TRADE • A+" in s
assert "TRADE • A" in s
assert "amyRound10EntryBodyAtr >= 0.50" in s
assert "amyRound10EntryBodyAtr < 2.50" in s
assert "amyEventBodyRatio >= 0.30" in s
assert "amyRound9EntryRiskAtr < 8.0" in s
assert "int amyNextDirection = amyRound5M5 ? (amyRound9M5TradeRegime ? amyRound9M5TradeDirection : 0) : amyFinalBias" in s
assert "float amyProjectedTargetDistance = math.max(amyTargetRiskDistance * 0.40, amyTargetAtr * 0.22)" in s

p.write_text(s)
