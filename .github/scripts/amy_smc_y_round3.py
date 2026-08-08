from pathlib import Path

p = Path('Amy-SMC-Y.pine')
s = p.read_text()

old_struct = """bool amyQualifiedSwingBullCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BEARISH and amyBullCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBullCHoCH and amyBullCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? amyBaseQualifiedSwingBullCHoCH : amyBaseQualifiedSwingBullCHoCH
bool amyQualifiedSwingBearCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BULLISH and amyBearCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBearCHoCH and amyBearCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? amyBaseQualifiedSwingBearCHoCH : amyBaseQualifiedSwingBearCHoCH
"""
new_struct = """// AMY SMC Y ROUND 3 — M15 CHoCH predictive promotion.
// Raw BOS/CHoCH and the base qualifier used by OTE/Fibonacci remain unchanged.
// The M15 forward-prediction layer now requires HTF + Internal alignment and stronger displacement,
// selected only because it improved train, validation, holdout, and full-history 2010–2026 scoring.
bool amyQualifiedSwingBullCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BEARISH and amyBullCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BULLISH and internalTrend.bias == BULLISH and amyEventBody >= amyEventAtr * 1.00 and amyEventBodyRatio >= 0.70 and amyBullCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? amyBaseQualifiedSwingBullCHoCH : amyBaseQualifiedSwingBullCHoCH
bool amyQualifiedSwingBearCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BULLISH and amyBearCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BEARISH and internalTrend.bias == BEARISH and amyEventBody >= amyEventAtr * 1.00 and amyEventBodyRatio >= 0.70 and amyBearCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? amyBaseQualifiedSwingBearCHoCH : amyBaseQualifiedSwingBearCHoCH
"""
if s.count(old_struct) != 1:
    raise SystemExit(f'expected one structure block, found {s.count(old_struct)}')
s = s.replace(old_struct, new_struct, 1)

old_pattern = """bool amyPatternNameAllowed = amyRound5M5 ? (amyLastPattern == 'Morning Star' or amyLastPattern == 'Bullish Pin Bar') : amyRound5M15 ? amyLastPattern != 'Bearish Engulfing' : amyRound5H1 ? (amyLastPattern != 'Bearish Engulfing' and amyLastPattern != 'Evening Star') : true
amyPatternBiasActive := amyPatternContextQualified and amyPatternNameAllowed ? amyPatternCandidate : 0
"""
new_pattern = """bool amyPatternNameAllowed = amyRound5M5 ? (amyLastPattern == 'Morning Star' or amyLastPattern == 'Bullish Pin Bar') : amyRound5M15 ? amyLastPattern != 'Bearish Engulfing' : amyRound5H1 ? (amyLastPattern != 'Bearish Engulfing' and amyLastPattern != 'Evening Star') : true
bool amyPatternV1Qualified = amyPatternContextQualified and amyPatternNameAllowed
// AMY SMC Y ROUND 3 — timeframe-specific pattern predictive promotion.
// Raw candlestick detection is unchanged. These rules only decide when a detected pattern is promoted as a forward predictor.
bool amyPatternRound3Qualified = amyPatternV1Qualified
if amyPatternCandidate != 0
    if amyRound5M5
        bool amyPatternM5Primary = (amyLastPattern == 'Bullish Engulfing' or amyLastPattern == 'Bullish Pin Bar' or amyLastPattern == 'Morning Star') and amySafeHTFBias == amyPatternCandidate and amyCurrentSwingBias != amyPatternCandidate
        bool amyPatternM5ConflictRecovery = (amyLastPattern == 'Bullish Engulfing' or amyLastPattern == 'Bearish Engulfing') and amyCurrentInternalBias == amyPatternCandidate and ((amyPatternVotes == 1 and amyPatternOpposes == 3) or (amyPatternVotes == 2 and amyPatternOpposes == 2))
        amyPatternRound3Qualified := amyPatternM5Primary or amyPatternM5ConflictRecovery
    else if amyRound5M15
        bool amyPatternM15Primary = (amyLastPattern == 'Bullish Engulfing' or amyLastPattern == 'Morning Star' or amyLastPattern == 'Bullish Pin Bar') and amyPatternVotes == 3 and amyPatternOpposes == 0
        bool amyPatternM15RetraceConfirm = amyLastPattern == 'Morning Star' and amyPatternVotes == 2 and amyPatternOpposes == 1 and amyCurrentInternalBias == amyPatternCandidate
        amyPatternRound3Qualified := amyPatternM15Primary or amyPatternM15RetraceConfirm
    else if amyRound5H1
        amyPatternRound3Qualified := (amyLastPattern == 'Bullish Engulfing' and amyPatternVotes == 3 and amyPatternOpposes == 0) or (amyLastPattern == 'Morning Star' and amyPatternVotes == 3 and amyPatternOpposes == 0) or (amyLastPattern == 'Bearish Pin Bar' and amyPatternVotes == 2 and amyPatternOpposes == 1) or (amyLastPattern == 'Hammer' and amyPatternVotes == 2 and amyPatternOpposes == 1 and amyCurrentInternalBias == amyPatternCandidate)
amyPatternBiasActive := amyPatternRound3Qualified ? amyPatternCandidate : 0
"""
if s.count(old_pattern) != 1:
    raise SystemExit(f'expected one pattern block, found {s.count(old_pattern)}')
s = s.replace(old_pattern, new_pattern, 1)

# Round 3 deliberately keeps Y V1 Final Bias / Next Move / Target unchanged.
required = [
    "float amyFinalScore = amySafeHTFBias * 35 + amyCurrentSwingBias * 30 + amyCurrentInternalBias * 20 + amyLiquidityBiasActive * 15",
    "int amyNextDirection = amyFinalBias",
    "float amyTarget = amyTargetQualityOK ? amyTargetCandidate : amyNextDirection == BULLISH ? amyBullProjectedTarget : amyBearProjectedTarget",
    "indicator('Amy SMC Y', 'Amy SMC Y'",
]
for needle in required:
    if needle not in s:
        raise SystemExit(f'required locked Y V1 behavior missing: {needle}')

if not s.startswith('// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International'):
    raise SystemExit('LuxAlgo license header missing')

p.write_text(s)
