from pathlib import Path

p = Path('Amy-SMC-Y.pine')
s = p.read_text()

old = """bool amyQualifiedBSLValidBreak = amyRound5M5 ? (amyQualifiedBSLValidBreakBase and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.65) : amyRound5M15 ? (amyQualifiedBSLValidBreakBase and internalTrend.bias == BULLISH and amyEventHTFBullOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedBSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedBSLValidBreakBase
bool amyQualifiedSSLValidBreak = amyRound5M5 ? (amyQualifiedSSLValidBreakBase and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.65) : amyRound5M15 ? (amyQualifiedSSLValidBreakBase and internalTrend.bias == BEARISH and amyEventHTFBearOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedSSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedSSLValidBreakBase
"""
new = """// AMY SMC Y ROUND 4 — M5 Valid Break predictive promotion.
// Raw liquidity events remain unchanged. Only the M5 forward-predictive promotion is made more selective.
bool amyQualifiedBSLValidBreak = amyRound5M5 ? (amyQualifiedBSLValidBreakBase and internalTrend.bias == BULLISH and amyEventHTFBullOK and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.80) : amyRound5M15 ? (amyQualifiedBSLValidBreakBase and internalTrend.bias == BULLISH and amyEventHTFBullOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedBSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedBSLValidBreakBase
bool amyQualifiedSSLValidBreak = amyRound5M5 ? (amyQualifiedSSLValidBreakBase and internalTrend.bias == BEARISH and amyEventHTFBearOK and amyBreakBodyAtr >= 3.0 and amyEventBodyRatio >= 0.80) : amyRound5M15 ? (amyQualifiedSSLValidBreakBase and internalTrend.bias == BEARISH and amyEventHTFBearOK and amyBreakBodyAtr >= 1.0 and amyEventBodyRatio >= 0.65) : amyRound5H1 ? (amyQualifiedSSLValidBreakBase and amyBreakBodyAtr >= 0.50 and amyEventBodyRatio >= 0.70) : amyQualifiedSSLValidBreakBase
"""
if old not in s:
    raise SystemExit('valid-break block not found')
s = s.replace(old, new, 1)

old = """bool amyQualifiedSwingBullCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BEARISH and amyBullCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BULLISH and internalTrend.bias == BULLISH and amyEventBody >= amyEventAtr * 1.00 and amyEventBodyRatio >= 0.70 and amyBullCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? amyBaseQualifiedSwingBullCHoCH : amyBaseQualifiedSwingBullCHoCH
bool amyQualifiedSwingBearCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BULLISH and amyBearCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BEARISH and internalTrend.bias == BEARISH and amyEventBody >= amyEventAtr * 1.00 and amyEventBodyRatio >= 0.70 and amyBearCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? amyBaseQualifiedSwingBearCHoCH : amyBaseQualifiedSwingBearCHoCH
"""
new = """// AMY SMC Y ROUND 4 — M5/H1 CHoCH predictive refinement.
// M15 keeps the Round 3 profile. The base qualifier used by OTE/Fibonacci stays untouched.
bool amyQualifiedSwingBullCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BEARISH and internalTrend.bias == BULLISH and amyEventBody >= amyEventAtr * 0.75 and amyEventBodyRatio >= 0.65 and amyBullCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBullCHoCH and amyHTFSwing == BULLISH and internalTrend.bias == BULLISH and amyEventBody >= amyEventAtr * 1.00 and amyEventBodyRatio >= 0.70 and amyBullCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? (amyBaseQualifiedSwingBullCHoCH and amyEventBodyRatio >= 0.65) : amyBaseQualifiedSwingBullCHoCH
bool amyQualifiedSwingBearCHoCH = amyRound5M5 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BULLISH and internalTrend.bias == BEARISH and amyEventBody >= amyEventAtr * 0.75 and amyEventBodyRatio >= 0.65 and amyBearCHoCHExcursionAtr >= 0.20) : amyRound5M15 ? (amyBaseQualifiedSwingBearCHoCH and amyHTFSwing == BEARISH and internalTrend.bias == BEARISH and amyEventBody >= amyEventAtr * 1.00 and amyEventBodyRatio >= 0.70 and amyBearCHoCHExcursionAtr >= 0.30) : amyRound5H1 ? (amyBaseQualifiedSwingBearCHoCH and amyEventBodyRatio >= 0.65) : amyBaseQualifiedSwingBearCHoCH
"""
if old not in s:
    raise SystemExit('CHoCH block not found')
s = s.replace(old, new, 1)

old = """    else if amyRound5H1
        amyPatternRound3Qualified := (amyLastPattern == 'Bullish Engulfing' and amyPatternVotes == 3 and amyPatternOpposes == 0) or (amyLastPattern == 'Morning Star' and amyPatternVotes == 3 and amyPatternOpposes == 0) or (amyLastPattern == 'Bearish Pin Bar' and amyPatternVotes == 2 and amyPatternOpposes == 1) or (amyLastPattern == 'Hammer' and amyPatternVotes == 2 and amyPatternOpposes == 1 and amyCurrentInternalBias == amyPatternCandidate)
amyPatternBiasActive := amyPatternRound3Qualified ? amyPatternCandidate : 0
"""
new = """    else if amyRound5H1
        amyPatternRound3Qualified := (amyLastPattern == 'Bullish Engulfing' and amyPatternVotes == 3 and amyPatternOpposes == 0) or (amyLastPattern == 'Morning Star' and amyPatternVotes == 3 and amyPatternOpposes == 0) or (amyLastPattern == 'Bearish Pin Bar' and amyPatternVotes == 2 and amyPatternOpposes == 1) or (amyLastPattern == 'Hammer' and amyPatternVotes == 2 and amyPatternOpposes == 1 and amyCurrentInternalBias == amyPatternCandidate)
// AMY SMC Y ROUND 4 — precision refinement on top of the retained Round 3 pattern profile.
// No new pattern detector is added; only forward-predictive promotion is filtered.
bool amyPatternRound4Qualified = amyPatternRound3Qualified
if amyPatternCandidate != 0 and amyPatternRound3Qualified
    if amyRound5M5
        amyPatternRound4Qualified := amyLastPattern == 'Bullish Engulfing' or amyLastPattern == 'Bearish Engulfing'
    else if amyRound5M15
        amyPatternRound4Qualified := (amyLastPattern == 'Bullish Engulfing' or amyLastPattern == 'Morning Star') and amySafeHTFBias == amyPatternCandidate
    else if amyRound5H1
        amyPatternRound4Qualified := amySafeHTFBias == amyPatternCandidate and amyCurrentInternalBias == amyPatternCandidate
amyPatternBiasActive := amyPatternRound4Qualified ? amyPatternCandidate : 0
"""
if old not in s:
    raise SystemExit('pattern block not found')
s = s.replace(old, new, 1)

p.write_text(s)
