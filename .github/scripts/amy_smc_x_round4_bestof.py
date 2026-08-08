from pathlib import Path

p = Path('Amy-SMC-X.pine')
s = p.read_text()

def repl(old: str, new: str, label: str):
    global s
    if old not in s:
        raise SystemExit(f'{label} block not found')
    s = s.replace(old, new, 1)

# Apply after reverting Round 4 commit 0672d691.

# 1) Liquidity Sweep / Valid Break: Round 4 improved M15 only.
old = """bool amyQualifiedBSLSweep = amyBSLSweep and high >= amyBSL + amyMinSweepExcursion and close >= amyBSL - nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedSSLSweep = amySSLSweep and low <= amySSL - amyMinSweepExcursion and close <= amySSL + nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedBSLValidBreak = amyBSLValidBreak and amyEventDisplacement and close > open and close >= amyBSL + amyMinBreakExcursion
bool amyQualifiedSSLValidBreak = amySSLValidBreak and amyEventDisplacement and close < open and close <= amySSL - amyMinBreakExcursion
"""
new = """bool amyEventHTFBullOK = na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH
bool amyEventHTFBearOK = na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH
bool amyLiquidityRound4TF = timeframe.period == '15'
bool amySweepBearStructureOK = internalTrend.bias != BULLISH and (swingTrend.bias == BEARISH or amyEventHTFBearOK)
bool amySweepBullStructureOK = internalTrend.bias != BEARISH and (swingTrend.bias == BULLISH or amyEventHTFBullOK)
bool amyQualifiedBSLSweepBase = amyBSLSweep and high >= amyBSL + amyMinSweepExcursion and close >= amyBSL - nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedSSLSweepBase = amySSLSweep and low <= amySSL - amyMinSweepExcursion and close <= amySSL + nz(amyEventAtr, 0.0) * 0.20
bool amyQualifiedBSLValidBreakBase = amyBSLValidBreak and amyEventDisplacement and close > open and close >= amyBSL + amyMinBreakExcursion
bool amyQualifiedSSLValidBreakBase = amySSLValidBreak and amyEventDisplacement and close < open and close <= amySSL - amyMinBreakExcursion
bool amyQualifiedBSLSweep = amyQualifiedBSLSweepBase and (not amyLiquidityRound4TF or amySweepBearStructureOK)
bool amyQualifiedSSLSweep = amyQualifiedSSLSweepBase and (not amyLiquidityRound4TF or amySweepBullStructureOK)
bool amyQualifiedBSLValidBreak = amyQualifiedBSLValidBreakBase and (not amyLiquidityRound4TF or (internalTrend.bias == BULLISH and amyEventHTFBullOK))
bool amyQualifiedSSLValidBreak = amyQualifiedSSLValidBreakBase and (not amyLiquidityRound4TF or (internalTrend.bias == BEARISH and amyEventHTFBearOK))
"""
repl(old, new, 'liquidity qualifier')

# 2) Strong High / Low protected layer improved the still-unpassed Strong labels; keep it independent from invalidation/target.
marker = """bool amyQualifiedSwingBullBOS = amyBaseQualifiedSwingBullBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH)
bool amyQualifiedSwingBearBOS = amyBaseQualifiedSwingBearBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH)
bool amyQualifiedSwingBullCHoCH = amyBaseQualifiedSwingBullCHoCH
bool amyQualifiedSwingBearCHoCH = amyBaseQualifiedSwingBearCHoCH

if amyBSLSweep
"""
insert = """bool amyQualifiedSwingBullBOS = amyBaseQualifiedSwingBullBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH)
bool amyQualifiedSwingBearBOS = amyBaseQualifiedSwingBearBOS and (na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH)
bool amyQualifiedSwingBullCHoCH = amyBaseQualifiedSwingBullCHoCH
bool amyQualifiedSwingBearCHoCH = amyBaseQualifiedSwingBearCHoCH

// Protected Strong layer retained from Round 4. It does not feed Final Bias, Target, or Invalidation.
var float amyProtectedStrongHigh = na
var float amyProtectedStrongLow = na
var int amyProtectedStrongHighBar = na
var int amyProtectedStrongLowBar = na
if barstate.isconfirmed
    if (amyBaseQualifiedSwingBullBOS or amyBaseQualifiedSwingBullCHoCH) and not na(swingLow.currentLevel)
        amyProtectedStrongLow := swingLow.currentLevel
        amyProtectedStrongLowBar := swingLow.barIndex
    if (amyBaseQualifiedSwingBearBOS or amyBaseQualifiedSwingBearCHoCH) and not na(swingHigh.currentLevel)
        amyProtectedStrongHigh := swingHigh.currentLevel
        amyProtectedStrongHighBar := swingHigh.barIndex

if amyBSLSweep
"""
repl(marker, insert, 'strong layer insertion')

old = """            if currentText == 'Strong High'
                label.set_text(currentLabel, 'Strong High ' + amyPrice(trailing.top))
            else if currentText == 'Weak High'
                label.set_text(currentLabel, 'Weak High ' + amyPrice(trailing.top))
            else if currentText == 'Strong Low'
                label.set_text(currentLabel, 'Strong Low ' + amyPrice(trailing.bottom))
            else if currentText == 'Weak Low'
                label.set_text(currentLabel, 'Weak Low ' + amyPrice(trailing.bottom))
"""
new = """            if str.contains(currentText, 'Strong High')
                if not na(amyProtectedStrongHigh) and not na(amyProtectedStrongHighBar)
                    label.set_xy(currentLabel, amyProtectedStrongHighBar, amyProtectedStrongHigh)
                    label.set_text(currentLabel, 'Strong High ' + amyPrice(amyProtectedStrongHigh))
                else
                    label.set_text(currentLabel, 'Strong High ' + amyPrice(trailing.top))
            else if currentText == 'Weak High'
                label.set_text(currentLabel, 'Weak High ' + amyPrice(trailing.top))
            else if str.contains(currentText, 'Strong Low')
                if not na(amyProtectedStrongLow) and not na(amyProtectedStrongLowBar)
                    label.set_xy(currentLabel, amyProtectedStrongLowBar, amyProtectedStrongLow)
                    label.set_text(currentLabel, 'Strong Low ' + amyPrice(amyProtectedStrongLow))
                else
                    label.set_text(currentLabel, 'Strong Low ' + amyPrice(trailing.bottom))
            else if currentText == 'Weak Low'
                label.set_text(currentLabel, 'Weak Low ' + amyPrice(trailing.bottom))
"""
repl(old, new, 'strong display')

# 3) Dealing Range: stricter context improved M5 but reduced M15. Apply it only to tested M5.
old = """bool amyDRBullContext = amyDRBias == BULLISH and swingTrend.bias == BULLISH and internalTrend.bias != BEARISH
bool amyDRBearContext = amyDRBias == BEARISH and swingTrend.bias == BEARISH and internalTrend.bias != BULLISH
"""
new = """// H1 65/35 passed profile is unchanged. Round 4 stricter context is retained only on M5.
bool amyDRM5Strict = timeframe.period == '5'
bool amyDRBullHTFConfirm = na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH
bool amyDRBearHTFConfirm = na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH
bool amyDRBullContextBase = amyDRBias == BULLISH and swingTrend.bias == BULLISH and internalTrend.bias != BEARISH
bool amyDRBearContextBase = amyDRBias == BEARISH and swingTrend.bias == BEARISH and internalTrend.bias != BULLISH
bool amyDRBullContext = amyDRBullContextBase and (not amyDRM5Strict or (internalTrend.bias == BULLISH and amyDRBullHTFConfirm))
bool amyDRBearContext = amyDRBearContextBase and (not amyDRM5Strict or (internalTrend.bias == BEARISH and amyDRBearHTFConfirm))
"""
repl(old, new, 'dealing range')

# 4) Pattern: M5 keeps Round 3; M15/H1 keep Round 4 because those two improved.
old = """int amyPatternVotes = amyPatternBiasActive == 0 ? 0 : (amySafeHTFBias == amyPatternBiasActive ? 1 : 0) + (amyCurrentSwingBias == amyPatternBiasActive ? 1 : 0) + (amyCurrentInternalBias == amyPatternBiasActive ? 1 : 0) + (amyLiquidityBiasActive == amyPatternBiasActive ? 1 : 0)
int amyPatternOpposes = amyPatternBiasActive == 0 ? 0 : (amySafeHTFBias != 0 and amySafeHTFBias == -amyPatternBiasActive ? 1 : 0) + (amyCurrentSwingBias != 0 and amyCurrentSwingBias == -amyPatternBiasActive ? 1 : 0) + (amyCurrentInternalBias != 0 and amyCurrentInternalBias == -amyPatternBiasActive ? 1 : 0) + (amyLiquidityBiasActive != 0 and amyLiquidityBiasActive == -amyPatternBiasActive ? 1 : 0)
bool amyPatternReversal = amyLastPattern == 'Morning Star' or amyLastPattern == 'Evening Star' or amyLastPattern == 'Hammer' or amyLastPattern == 'Shooting Star' or amyLastPattern == 'Bullish Pin Bar' or amyLastPattern == 'Bearish Pin Bar'
bool amyPatternLocalBoth = amyPatternBiasActive != 0 and amyCurrentSwingBias == amyPatternBiasActive and amyCurrentInternalBias == amyPatternBiasActive
bool amyPatternLiquidityConfirm = amyPatternBiasActive != 0 and amyLiquidityBiasActive == amyPatternBiasActive
bool amyPatternContextQualified = amyPatternBiasActive != 0 and amyPatternVotes >= 2 and amyPatternOpposes <= 1 and (not amyPatternReversal or amyPatternLiquidityConfirm or amyPatternLocalBoth)
amyPatternBiasActive := amyPatternContextQualified ? amyPatternBiasActive : 0
"""
new = """int amyPatternCandidate = amyPatternBiasActive
int amyPatternVotes = amyPatternCandidate == 0 ? 0 : (amySafeHTFBias == amyPatternCandidate ? 1 : 0) + (amyCurrentSwingBias == amyPatternCandidate ? 1 : 0) + (amyCurrentInternalBias == amyPatternCandidate ? 1 : 0) + (amyLiquidityBiasActive == amyPatternCandidate ? 1 : 0)
int amyPatternOpposes = amyPatternCandidate == 0 ? 0 : (amySafeHTFBias != 0 and amySafeHTFBias == -amyPatternCandidate ? 1 : 0) + (amyCurrentSwingBias != 0 and amyCurrentSwingBias == -amyPatternCandidate ? 1 : 0) + (amyCurrentInternalBias != 0 and amyCurrentInternalBias == -amyPatternCandidate ? 1 : 0) + (amyLiquidityBiasActive != 0 and amyLiquidityBiasActive == -amyPatternCandidate ? 1 : 0)
bool amyPatternReversal = amyLastPattern == 'Morning Star' or amyLastPattern == 'Evening Star' or amyLastPattern == 'Hammer' or amyLastPattern == 'Shooting Star' or amyLastPattern == 'Bullish Pin Bar' or amyLastPattern == 'Bearish Pin Bar'
bool amyPatternLocalBoth = amyPatternCandidate != 0 and amyCurrentSwingBias == amyPatternCandidate and amyCurrentInternalBias == amyPatternCandidate
bool amyPatternLiquidityConfirm = amyPatternCandidate != 0 and amyLiquidityBiasActive == amyPatternCandidate
bool amyPatternRound4TF = timeframe.period == '15' or timeframe.period == '60'
bool amyPatternContextQualified = false
if amyPatternCandidate != 0
    if not amyPatternRound4TF
        amyPatternContextQualified := amyPatternVotes >= 2 and amyPatternOpposes <= 1 and (not amyPatternReversal or amyPatternLiquidityConfirm or amyPatternLocalBoth)
    else
        bool amyPatternBearPriority = amyLastPattern == 'Bearish Engulfing' or amyLastPattern == 'Evening Star' or amyLastPattern == 'Bearish Pin Bar'
        bool amyPatternBullish = amyPatternCandidate == BULLISH
        int amyPatternRequiredVotes = amyPatternBearPriority ? 2 : 3
        bool amyPatternConflictOK = amyPatternBearPriority ? amyPatternOpposes <= 1 : amyPatternOpposes == 0
        bool amyPatternBullExtra = not amyPatternBullish or amyPatternLiquidityConfirm or amyPatternLocalBoth
        bool amyPatternReversalExtra = not amyPatternReversal or amyPatternLiquidityConfirm or amyPatternLocalBoth
        amyPatternContextQualified := amyPatternVotes >= amyPatternRequiredVotes and amyPatternConflictOK and amyPatternBullExtra and amyPatternReversalExtra
amyPatternBiasActive := amyPatternContextQualified ? amyPatternCandidate : 0
"""
repl(old, new, 'pattern')

# Passed components / profiles must remain frozen.
assert 'amyFinalScore = amySafeHTFBias * 35 + amyCurrentSwingBias * 30 + amyCurrentInternalBias * 20 + amyLiquidityBiasActive * 15' in s
assert 'PASSED CHECKPOINT — OTE→1.272 M15: 85.71% (6/7)' in s
assert 'PASSED CHECKPOINT — Fib 1.272: M5 70.27% (26/37), M15 81.82% (9/11)' in s
assert 'amyPassedDRPremiumRatio = 0.65' in s and 'amyPassedDRDiscountRatio = 0.35' in s
assert 'amyTargetEligible' not in s
assert 'amyxExtendedEligible' not in s

p.write_text(s)
