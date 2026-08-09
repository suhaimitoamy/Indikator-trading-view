from pathlib import Path

src = Path('Amy-SMC-Z.pine')
out = Path('Amy-SMC-Z-OF16.pine')
s = src.read_text()

# Experimental copy only. Main Amy SMC Z remains untouched.
s = s.replace("indicator('Amy SMC Z', 'Amy SMC Z', overlay = true", "indicator('Amy SMC Z OF16', 'Amy SMC Z OF16', overlay = true", 1)

# Header marker.
anchor = "//@version=5\nindicator('Amy SMC Z OF16', 'Amy SMC Z OF16', overlay = true"
marker = "//@version=5\n// OF16 EXPERIMENT — intentionally optimized on the complete 2010–2026 sample.\n// This file is an in-sample ceiling experiment, not an out-of-sample/generalization claim.\nindicator('Amy SMC Z OF16', 'Amy SMC Z OF16', overlay = true"
if anchor not in s:
    raise SystemExit('indicator anchor not found')
s = s.replace(anchor, marker, 1)

# OF16: accept the M15 CHoCH displacement-cap candidate that was previously rejected
# only because holdout deteriorated. The full-sample objective intentionally ignores that guardrail.
old_bull = "amyRound5M15 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BULLISH and internalTrend.bias == BULLISH and amyEventBody >= amyEventAtr * 1.00 and amyEventBodyRatio >= 0.70 and amyBullCHoCHExcursionAtr >= 0.30)"
new_bull = "amyRound5M15 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BULLISH and internalTrend.bias == BULLISH and amyEventBody >= amyEventAtr * 1.00 and amyBreakBodyAtr < 2.00 and amyEventBodyRatio >= 0.70 and amyBullCHoCHExcursionAtr >= 0.30)"
old_bear = "amyRound5M15 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BEARISH and internalTrend.bias == BEARISH and amyEventBody >= amyEventAtr * 1.00 and amyEventBodyRatio >= 0.70 and amyBearCHoCHExcursionAtr >= 0.30)"
new_bear = "amyRound5M15 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BEARISH and internalTrend.bias == BEARISH and amyEventBody >= amyEventAtr * 1.00 and amyBreakBodyAtr < 2.00 and amyEventBodyRatio >= 0.70 and amyBearCHoCHExcursionAtr >= 0.30)"
if old_bull not in s or old_bear not in s:
    raise SystemExit('M15 CHoCH anchors not found')
s = s.replace(old_bull, new_bull, 1)
s = s.replace(old_bear, new_bear, 1)

# OF16: promote the high-aggregate M15 sweep-continuation event into Next Move.
# This is exactly the kind of change previously blocked by holdout robustness rules.
h1_override = "// H1 uses a qualifying raw sweep only on the confirmed sweep candle. The forward direction is the continuation side\n// discovered in the long-history replay (opposite the raw sweep bias) and Internal Structure must already agree.\nif amyRound5H1 and amySweepContinuationQualified\n    amyNextDirection := amySweepContinuationBias"
of16_override = "// OF16 FULL-SAMPLE OVERRIDE — intentionally promote M15 sweep-continuation as well.\n// Round 5/7 evidence showed the M15 sweep-continuation event itself at ~85% full-history accuracy,\n// but the normal model rejected an M15 Next override when holdout worsened. OF16 intentionally accepts it.\nif amyRound5M15 and amySweepContinuationQualified\n    amyNextDirection := amySweepContinuationBias\n\n" + h1_override
if h1_override not in s:
    raise SystemExit('H1 sweep override anchor not found')
s = s.replace(h1_override, of16_override, 1)

# OF16 target fitting: deliberately shrink target geometry to optimize historical target-resolution.
# This is NOT RR-neutral and must never be confused with the baseline Z target profile.
repls = {
    "float amyProjectedTargetDistance = math.max(amyTargetRiskDistance * 0.40, amyTargetAtr * 0.22)":
        "float amyProjectedTargetDistance = math.max(amyTargetRiskDistance * 0.28, amyTargetAtr * 0.16)",
    "float amyTargetMinDistance = math.max(amyTargetAtr * 0.10, amyTargetRiskDistance * 0.30)":
        "float amyTargetMinDistance = math.max(amyTargetAtr * 0.06, amyTargetRiskDistance * 0.18)",
    "bool amyTargetQualityOK = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 and amyTargetDistanceRatio <= 0.40":
        "bool amyTargetQualityOK = not na(amyTargetCandidate) and amyTargetRiskDistance > 0 and amyTargetDistanceRatio <= 0.28",
}
for old, new in repls.items():
    if old not in s:
        raise SystemExit(f'target anchor not found: {old}')
    s = s.replace(old, new, 1)

# Label the target block so the experiment is impossible to mistake for baseline Z.
target_comment = "// AMY SMC Y TARGET V1 — target is ALWAYS available; NO TARGET / NA is not used as a normal predictive state."
if target_comment not in s:
    raise SystemExit('target comment anchor not found')
s = s.replace(target_comment,
              "// AMY SMC Z OF16 TARGET FIT — intentionally shorter full-sample target geometry.\n" + target_comment,
              1)

# Guardrails: baseline file is only read; output is a separate indicator.
assert src.read_text().startswith('// This work is licensed')
assert "Amy SMC Z OF16" in s
assert "amyRound5M15 and amySweepContinuationQualified" in s
assert "amyBreakBodyAtr < 2.00" in s
assert "amyTargetRiskDistance * 0.28" in s
assert "amyTargetDistanceRatio <= 0.28" in s
assert "string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'" in s

out.write_text(s)
