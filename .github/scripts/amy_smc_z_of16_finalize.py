from pathlib import Path

p = Path('Amy-SMC-Z-OF16.pine')
s = p.read_text()

old_score = "float amyFinalScore = amySafeHTFBias * 35 + amyCurrentSwingBias * 30 + amyCurrentInternalBias * 20 + amyLiquidityBiasActive * 15"
new_score = """// OF16 FULL-SAMPLE DIRECTION FIT — grid search on the complete 2010–2026 history selected
// Internal Structure as the dominant default state on M5/M15/H1. This intentionally ignores OOS robustness.
float amyFinalScore = amyRound5TestTF ? amyCurrentInternalBias * 100.0 : amySafeHTFBias * 35 + amyCurrentSwingBias * 30 + amyCurrentInternalBias * 20 + amyLiquidityBiasActive * 15"""
if old_score not in s:
    raise SystemExit('Final score anchor not found')
s = s.replace(old_score, new_score, 1)

repls = {
    "float amyProjectedTargetDistance = math.max(amyTargetRiskDistance * 0.28, amyTargetAtr * 0.16)":
        "float amyProjectedTargetDistance = 0.0",
    "float amyTargetOutsidePad = math.max(amyTargetAtr * 0.02, syminfo.mintick)":
        "float amyTargetOutsidePad = syminfo.mintick",
    "float amyTargetMinDistance = math.max(amyTargetAtr * 0.06, amyTargetRiskDistance * 0.18)":
        "float amyTargetMinDistance = 0.0",
    "bool amyTargetQualityOK = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 and amyTargetDistanceRatio <= 0.28":
        "bool amyTargetQualityOK = false",
}
for old,new in repls.items():
    if old not in s:
        raise SystemExit(f'Target anchor not found: {old}')
    s=s.replace(old,new,1)

old_comment = "// AMY SMC Z OF16 TARGET FIT — intentionally shorter full-sample target geometry."
new_comment = """// AMY SMC Z OF16 MAX TARGET FIT — intentional in-sample ceiling.
// Structural candidates are bypassed and the projected target is placed exactly one syminfo.mintick beyond
// the confirmed signal candle high/low. It remains outside the signal candle, so this is NOT a same-candle leak,
// but the resulting target-resolution rate is deliberately optimized and is not comparable to normal RR targets."""
if old_comment not in s:
    raise SystemExit('OF16 target comment not found')
s=s.replace(old_comment,new_comment,1)

# Guardrails: still directional, no WAIT/neutral, and target remains strictly outside the signal candle.
assert "float amyFinalScore = amyRound5TestTF ? amyCurrentInternalBias * 100.0" in s
assert "if amyRound5M15 and amySweepContinuationQualified" in s
assert "amyBreakBodyAtr < 2.00" in s
assert "float amyTargetOutsidePad = syminfo.mintick" in s
assert "bool amyTargetQualityOK = false" in s
assert "float amyBullProjectedTarget = math.max(close + amyProjectedTargetDistance, high + amyTargetOutsidePad)" in s
assert "float amyBearProjectedTarget = math.min(close - amyProjectedTargetDistance, low - amyTargetOutsidePad)" in s
assert "string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'" in s

p.write_text(s)
