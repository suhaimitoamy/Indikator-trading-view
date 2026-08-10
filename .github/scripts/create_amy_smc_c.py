from pathlib import Path
import hashlib
import subprocess

EXPECTED = {
    'Amy-SMC-B.pine': '3b9b718a238e1c836920e76449bc5e4e11246440',
    'Amy-SMC-B-LAB.pine': '5df16e233afe06402307bebe71703093f50af58d',
    'Amy-SMC-Z.pine': '389036df09d03125a2f71189722953658a901170',
    'Amy-SMC-A.pine': 'edb769a2bcfc59fe53237eda2a926fe31a14003b',
    'Amy-SMC-A-LAB.pine': '66b80304c44556040dc587557913bda309ca7b7d',
}

def git_blob(path: str) -> str:
    return subprocess.check_output(['git', 'hash-object', path], text=True).strip()

for path, sha in EXPECTED.items():
    actual = git_blob(path)
    if actual != sha:
        raise SystemExit(f'guard failed: {path} {actual} != {sha}')

for path in ('Amy-SMC-C.pine', 'Amy-SMC-C-LAB.pine'):
    if Path(path).exists():
        raise SystemExit(f'{path} already exists')

s = Path('Amy-SMC-B.pine').read_text()
s = s.replace("indicator('Amy SMC B', 'Amy SMC B',", "indicator('Amy SMC C', 'Amy SMC C',", 1)
start = "float amyPassedDRPremiumRatio = 0.65"
end = "\nint amyLiquidityAge ="
i = s.index(start)
j = s.index(end, i)
new = '''// AMY SMC C — DEALING RANGE PURE-LOCATION REDESIGN.
// Fresh raw XAUUSD 2004-2026, rolling 8y->1y OOS 2012-2026:
// M5 uses 70/30 pure location; M15 uses 60/40 pure location. No Swing/Internal/HTF confirmation is required.
// H1 intentionally keeps the frozen B/Z 65/35 context-gated definition because its redesign was not stable.
float amyPassedDRPremiumRatio = 0.65
float amyPassedDRDiscountRatio = 0.35
float amyPremiumGate = amyDRValid ? amyRangeBottom + amyRangeSpan * amyPassedDRPremiumRatio : na
float amyDiscountGate = amyDRValid ? amyRangeBottom + amyRangeSpan * amyPassedDRDiscountRatio : na
bool amyDRM5Strict = timeframe.period == '5'
bool amyDRBullHTFConfirm = na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BULLISH
bool amyDRBearHTFConfirm = na(amyHTFSwing) or amyHTFSwing == 0 or amyHTFSwing == BEARISH
bool amyDRBullContextBase = amyDRBias == BULLISH and swingTrend.bias == BULLISH and internalTrend.bias != BEARISH
bool amyDRBearContextBase = amyDRBias == BEARISH and swingTrend.bias == BEARISH and internalTrend.bias != BULLISH
bool amyDRBullContext = amyDRBullContextBase and (not amyDRM5Strict or (internalTrend.bias == BULLISH and amyDRBullHTFConfirm))
bool amyDRBearContext = amyDRBearContextBase and (not amyDRM5Strict or (internalTrend.bias == BEARISH and amyDRBearHTFConfirm))

bool amyCDealingPureTF = amyRound5M5 or amyRound5M15
float amyCDealingPremiumRatio = amyRound5M5 ? 0.70 : amyRound5M15 ? 0.60 : amyPassedDRPremiumRatio
float amyCDealingDiscountRatio = amyRound5M5 ? 0.30 : amyRound5M15 ? 0.40 : amyPassedDRDiscountRatio
float amyCDealingPremiumGate = amyDRValid ? amyRangeBottom + amyRangeSpan * amyCDealingPremiumRatio : na
float amyCDealingDiscountGate = amyDRValid ? amyRangeBottom + amyRangeSpan * amyCDealingDiscountRatio : na

string amyDealingRange = 'EQUILIBRIUM'
int amyDealingBias = 0
if amyDRValid
    if amyCDealingPureTF
        // C M5/M15: the field itself is the validated pure-location signal.
        // PREMIUM = bearish, DISCOUNT = bullish; middle band remains equilibrium/neutral.
        if close >= amyCDealingPremiumGate
            amyDealingRange := 'PREMIUM'
            amyDealingBias := BEARISH
        else if close <= amyCDealingDiscountGate
            amyDealingRange := 'DISCOUNT'
            amyDealingBias := BULLISH
    else
        // H1 and other timeframes retain the frozen B/Z behavior exactly.
        if close > amyEQUpper
            amyDealingRange := 'PREMIUM'
            amyDealingBias := close >= amyPremiumGate and amyDRBearContext ? BEARISH : 0
        else if close < amyEQLower
            amyDealingRange := 'DISCOUNT'
            amyDealingBias := close <= amyDiscountGate and amyDRBullContext ? BULLISH : 0
'''
s = s[:i] + new + s[j:]
Path('Amy-SMC-C.pine').write_text(s)
Path('Amy-SMC-C-LAB.pine').write_text(s.replace("indicator('Amy SMC C', 'Amy SMC C',", "indicator('Amy SMC C LAB', 'Amy SMC C LAB',", 1))

c = Path('Amy-SMC-C.pine').read_text()
cl = Path('Amy-SMC-C-LAB.pine').read_text()
assert "float amyCDealingPremiumRatio = amyRound5M5 ? 0.70 : amyRound5M15 ? 0.60 : amyPassedDRPremiumRatio" in c
assert "float amyCDealingDiscountRatio = amyRound5M5 ? 0.30 : amyRound5M15 ? 0.40 : amyPassedDRDiscountRatio" in c
assert "H1 and other timeframes retain the frozen B/Z behavior exactly." in c
assert cl.replace('Amy SMC C LAB', 'Amy SMC C') == c
print('C_BUILT_OK')
