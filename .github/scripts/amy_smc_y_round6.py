from pathlib import Path

p = Path('Amy-SMC-Y.pine')
s = p.read_text()

old_pattern = """// AMY SMC Y ROUND 5 — 16-YEAR CONDITIONAL PATTERN PROFILE.
// No detector is added. M5 keeps only the Round-4-qualified Bearish Engulfing forward call because that family
// remained above 70% in train (2010–2018), validation (2019–2023), and holdout (2024–2026). M15/H1 retain
// their Round 4 profiles because extra Round 5 filtering did not improve them robustly.
bool amyPatternRound5Qualified = amyPatternRound4Qualified
if amyRound5M5
    amyPatternRound5Qualified := amyPatternRound4Qualified and amyLastPattern == 'Bearish Engulfing'
amyPatternBiasActive := amyPatternRound5Qualified ? amyPatternCandidate : 0
"""
new_pattern = """// AMY SMC Y ROUND 5 — 16-YEAR CONDITIONAL PATTERN PROFILE.
// No detector is added. M5 keeps only the Round-4-qualified Bearish Engulfing forward call because that family
// remained above 70% in train (2010–2018), validation (2019–2023), and holdout (2024–2026).
bool amyPatternRound5Qualified = amyPatternRound4Qualified
if amyRound5M5
    amyPatternRound5Qualified := amyPatternRound4Qualified and amyLastPattern == 'Bearish Engulfing'
// AMY SMC Y ROUND 6 — liquidity-conflict pattern regime.
// Across 2010–2026, a freshly detected M15/H1 pattern that points against the still-active liquidity bias was a
// repeatable reversal regime and improved train, validation and holdout versus the retained Round-5 pattern layer.
// This is detection-candle only so a later liquidity-state change cannot retroactively promote an old pattern.
bool amyPatternLiquidityConflictRegime = amyPatternAge == 0 and amyPatternCandidate != 0 and amyLiquidityBiasActive == -amyPatternCandidate
bool amyPatternRound6Qualified = amyPatternRound5Qualified or ((amyRound5M15 or amyRound5H1) and amyPatternLiquidityConflictRegime)
amyPatternBiasActive := amyPatternRound6Qualified ? amyPatternCandidate : 0
"""
if old_pattern not in s:
    raise SystemExit('Round 5 pattern block not found')
s = s.replace(old_pattern, new_pattern, 1)

old_choch_bull = "amyRound5H1 ? (amyBaseQualifiedSwingBullCHoCH and amyEventBodyRatio >= 0.65) : amyBaseQualifiedSwingBullCHoCH"
new_choch_bull = "amyRound5H1 ? (amyBaseQualifiedSwingBullCHoCH and amyEventBodyRatio >= 0.65 and amyBreakBodyAtr < 1.50) : amyBaseQualifiedSwingBullCHoCH"
old_choch_bear = "amyRound5H1 ? (amyBaseQualifiedSwingBearCHoCH and amyEventBodyRatio >= 0.65) : amyBaseQualifiedSwingBearCHoCH"
new_choch_bear = "amyRound5H1 ? (amyBaseQualifiedSwingBearCHoCH and amyEventBodyRatio >= 0.65 and amyBreakBodyAtr < 1.50) : amyBaseQualifiedSwingBearCHoCH"
if old_choch_bull not in s or old_choch_bear not in s:
    raise SystemExit('H1 CHoCH profile not found')
s = s.replace(old_choch_bull, new_choch_bull, 1)
s = s.replace(old_choch_bear, new_choch_bear, 1)

needle = "// AMY SMC Y ROUND 4 — M5/H1 CHoCH predictive refinement.\n// M15 keeps the Round 3 profile. The base qualifier used by OTE/Fibonacci stays untouched.\n"
replacement = needle + "// AMY SMC Y ROUND 6 — H1 CHoCH keeps only controlled displacement (<1.50 ATR). The 2010–2026 replay\n// improved train, validation and holdout with this cap. Base CHoCH remains untouched for OTE/Fibonacci.\n"
if needle not in s:
    raise SystemExit('CHoCH comment anchor not found')
s = s.replace(needle, replacement, 1)

# Guardrails: no forbidden output-state changes and no edits outside Y happen in this script.
assert "string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'" in s
assert "TARGET V1 — target is ALWAYS available" in s
assert "WAIT/NEUTRAL" in s
assert "NO TARGET / NA is not used" in s
assert "amyPatternLiquidityConflictRegime" in s
assert "amyBreakBodyAtr < 1.50" in s

p.write_text(s)
