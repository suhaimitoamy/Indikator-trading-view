from pathlib import Path

p = Path('Amy-SMC-Z.pine')
s = p.read_text()

old_predictive = """// AMY SMC Y PREDICTIVE V1 — LONG-HISTORY 2010–2026.
// Final Bias was materially more stable than the independent short-horizon Next Move.
// Next Move therefore remains ALWAYS directional (UP/DOWN) and is anchored to Final Bias; there is no WAIT/NEUTRAL state.
// Event History is retained as context and confidence evidence, not as an independent direction-flip engine.
"""
new_predictive = """// AMY SMC Z ROUND 8 — LONG-HISTORY CONTEXT.
// Final Bias remains a continuous descriptive bias, while M5 Next Move is now selective and may WAIT outside
// the validated execution regime. M15/H1 retain the accepted Round-7 directional behavior.
// Event History stays context/confidence evidence and is not an independent direction-flip engine.
"""
if old_predictive not in s:
    raise SystemExit('stale predictive comment not found')
s = s.replace(old_predictive, new_predictive, 1)

old_target_comment = """// AMY SMC Y TARGET V1 — target is ALWAYS available; NO TARGET / NA is not used as a normal predictive state.
// Prefer nearby untouched structural liquidity. If that liquidity is too distant or unavailable, use a conservative
// projected target tied to the protected invalidation distance. The projected target is forced outside the signal candle,
// preserving the same-candle anti-leak rule.
"""
new_target_comment = """// AMY SMC Z ROUND 8 TARGET V1 — target is available whenever Next Move is actionable.
// M5 WAIT/WATCH intentionally has no synthetic target. For actionable calls, prefer nearby untouched structural liquidity;
// if that liquidity is too distant or unavailable, use the retained conservative projected fallback. The projected target
// is forced outside the signal candle, preserving the same-candle anti-leak rule.
"""
if old_target_comment not in s:
    raise SystemExit('stale target comment not found')
s = s.replace(old_target_comment, new_target_comment, 1)

assert "M5 Next Move is now selective and may WAIT" in s
assert "M5 WAIT/WATCH intentionally has no synthetic target" in s
assert "TRADE • TRANSITION" in s
assert "WATCH • SWEEP" in s
assert "float amyProjectedTargetDistance = math.max(amyTargetRiskDistance * 0.40, amyTargetAtr * 0.22)" in s

p.write_text(s)
