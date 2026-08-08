from pathlib import Path
import re

p = Path('Amy-SMC-Y.pine')
s = p.read_text()

liq_pat = re.compile(r"// AMY SMC Y ROUND 5 CANDIDATE — regime-aware liquidity prediction\.[\s\S]*?bool amyQualifiedSSLValidBreak = .*?\n\n// Base structure qualification is frozen", re.M)
liq_new = """// AMY SMC Y ROUND 5 — 16-YEAR CONDITIONAL LIQUIDITY PROFILE.
// Raw Sweep / Valid Break semantics are untouched. The 2010–2026 replay showed that a raw sweep is usually
// followed by the next swing structure in the OPPOSITE direction of the raw sweep bias when Internal Structure
// already points that way. This is used only as a forward-predictive continuation cue; the descriptive liquidity
// event, Event History, labels, and non-predictive modules keep their original meaning.
bool amyQualifiedBSLSweep = amyRound5TestTF ? false : amyQualifiedBSLSweepBase
bool amyQualifiedSSLSweep = amyRound5TestTF ? false : amyQualifiedSSLSweepBase
int amySweepContinuationBias = amyRound5TestTF ? (amyBSLSweep and internalTrend.bias == BULLISH ? BULLISH : amySSLSweep and internalTrend.bias == BEARISH ? BEARISH : 0) : 0
bool amySweepContinuationQualified = amySweepContinuationBias != 0
// Valid Break keeps the best pre-Round-5 profiles. It remains an independent confirmation/label layer and is not
// allowed to replace the much stronger sweep-continuation evidence in the Round 5 Next Move override.
bool amyQualifiedBSLValidBreak = amyRound5M5 ? (amyQualifiedBSLValidBreakBase and internalTrend.bias == BULLISH and amyEventHTFBullOK and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.80) : amyRound5M15 ? (amyQualifiedBSLValidBreakBase and internalTrend.bias == BULLISH and amyEventHTFBullOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedBSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedBSLValidBreakBase
bool amyQualifiedSSLValidBreak = amyRound5M5 ? (amyQualifiedSSLValidBreakBase and internalTrend.bias == BEARISH and amyEventHTFBearOK and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.80) : amyRound5M15 ? (amyQualifiedSSLValidBreakBase and internalTrend.bias == BEARISH and amyEventHTFBearOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedSSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedSSLValidBreakBase

// Base structure qualification is frozen"""
s, n = liq_pat.subn(liq_new, s, count=1)
if n != 1:
    raise SystemExit(f'liquidity replacement count={n}')

struct_pat = re.compile(r"float amyBullBOSExcursionAtr = .*?\nfloat amyBearBOSExcursionAtr = .*?\n// AMY SMC Y ROUND 5 CANDIDATE — BOS is evaluated as continuation, separately from CHoCH reversal\.[\s\S]*?bool amyQualifiedSwingBearBOS = .*?\n", re.M)
struct_new = """// ROUND 5 BEST-OF ROLLBACK — BOS continuation candidate did not beat the retained CHoCH profiles over 2010–2026.
// Raw BOS remains descriptive structure and the base BOS/CHoCH qualifier used by OTE/Fibonacci stays untouched.
bool amyQualifiedSwingBullBOS = amyRound5TestTF ? false : amyBaseQualifiedSwingBullBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH)
bool amyQualifiedSwingBearBOS = amyRound5TestTF ? false : amyBaseQualifiedSwingBearBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH)
"""
s, n = struct_pat.subn(struct_new, s, count=1)
if n != 1:
    raise SystemExit(f'structure replacement count={n}')

pattern_pat = re.compile(r"// AMY SMC Y ROUND 5 CANDIDATE — add regime consistency without adding new pattern detectors\.[\s\S]*?amyPatternBiasActive := amyPatternRound5Qualified \? amyPatternCandidate : 0", re.M)
pattern_new = """// AMY SMC Y ROUND 5 — 16-YEAR CONDITIONAL PATTERN PROFILE.
// No detector is added. M5 keeps only the Round-4-qualified Bearish Engulfing forward call because that family
// remained above 70% in train (2010–2018), validation (2019–2023), and holdout (2024–2026). M15/H1 retain
// their Round 4 profiles because extra Round 5 filtering did not improve them robustly.
bool amyPatternRound5Qualified = amyPatternRound4Qualified
if amyRound5M5
    amyPatternRound5Qualified := amyPatternRound4Qualified and amyLastPattern == 'Bearish Engulfing'
amyPatternBiasActive := amyPatternRound5Qualified ? amyPatternCandidate : 0"""
s, n = pattern_pat.subn(pattern_new, s, count=1)
if n != 1:
    raise SystemExit(f'pattern replacement count={n}')

next_pat = re.compile(r"// AMY SMC Y ROUND 5 CANDIDATE — selective predictor corroboration, still ALWAYS UP/DOWN\.[\s\S]*?int amyNextDirection = amyPredictiveOverride \? amyPredictiveConsensus : amyFinalBias", re.M)
next_new = """// AMY SMC Y ROUND 5 — 16-YEAR CONDITIONAL NEXT MOVE.
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
    amyNextDirection := amySweepContinuationBias"""
s, n = next_pat.subn(next_new, s, count=1)
if n != 1:
    raise SystemExit(f'next replacement count={n}')

needle = "string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'\n// AMY SMC Y TARGET V1"
replacement = "string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'\n// Keep the accepted invalidation geometry unchanged, but select the already-computed bullish/bearish side from the\n// actual Next Move direction so a Round-5 override cannot pair an UP target with a bearish-side invalidation (or vice versa).\nfloat amyExecutionInvalidation = amyNextDirection == BULLISH ? amyBullInvalidation : amyBearInvalidation\n// AMY SMC Y TARGET V1"
if needle not in s:
    raise SystemExit('next/target insertion point not found')
s = s.replace(needle, replacement, 1)

old = "float amyTargetRiskDistance = not na(amyInvalidation) ? math.abs(close - amyInvalidation) : amyTargetAtr"
new = "float amyTargetRiskDistance = not na(amyExecutionInvalidation) ? math.abs(close - amyExecutionInvalidation) : amyTargetAtr"
if old not in s:
    raise SystemExit('target risk line not found')
s = s.replace(old, new, 1)

old = "table.cell(amyDashboard, 1, 7, amyPrice(amyInvalidation), text_color = color.white, text_size = size.tiny)"
new = "table.cell(amyDashboard, 1, 7, amyPrice(amyExecutionInvalidation), text_color = color.white, text_size = size.tiny)"
if old not in s:
    raise SystemExit('dashboard invalidation line not found')
s = s.replace(old, new, 1)

# Safety assertions for the user's fixed rules.
if "string amyNextMove = amyNextDirection == BULLISH ? 'UP' : 'DOWN'" not in s:
    raise SystemExit('Next Move is no longer strictly UP/DOWN')
if "float amyTarget = amyTargetQualityOK ? amyTargetCandidate : amyNextDirection == BULLISH ? amyBullProjectedTarget : amyBearProjectedTarget" not in s:
    raise SystemExit('always-available Target fallback missing')
if 'AMY SMC Y ROUND 5 CANDIDATE' in s:
    raise SystemExit('stale Round 5 candidate marker remains')

p.write_text(s)
