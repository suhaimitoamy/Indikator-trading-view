from pathlib import Path

p = Path('Amy-SMC-Z.pine')
s = p.read_text()
old = """amyStructureBias(int length) =>
    float ph = ta.pivothigh(high, length, length)
    float pl = ta.pivotlow(low, length, length)
    float lastPH = ta.valuewhen(not na(ph), ph, 0)
    float prevPH = ta.valuewhen(not na(ph), ph, 1)
    float lastPL = ta.valuewhen(not na(pl), pl, 0)
    float prevPL = ta.valuewhen(not na(pl), pl, 1)
    bool bullishStructure = not na(lastPH) and not na(prevPH) and not na(lastPL) and not na(prevPL) and lastPH > prevPH and lastPL > prevPL
    bool bearishStructure = not na(lastPH) and not na(prevPH) and not na(lastPL) and not na(prevPL) and lastPH < prevPH and lastPL < prevPL
    int result = 0
    if bullishStructure
        result := BULLISH
    else if bearishStructure
        result := BEARISH
    else
        float baseline = ta.sma(close, length * 2)
        result := na(baseline) ? 0 : close >= baseline ? BULLISH : BEARISH
    result
"""
new = """amyStructureBias(int length) =>
    float ph = ta.pivothigh(high, length, length)
    float pl = ta.pivotlow(low, length, length)
    float lastPH = ta.valuewhen(not na(ph), ph, 0)
    float prevPH = ta.valuewhen(not na(ph), ph, 1)
    float lastPL = ta.valuewhen(not na(pl), pl, 0)
    float prevPL = ta.valuewhen(not na(pl), pl, 1)
    float baseline = ta.sma(close, length * 2)
    bool bullishStructure = not na(lastPH) and not na(prevPH) and not na(lastPL) and not na(prevPL) and lastPH > prevPH and lastPL > prevPL
    bool bearishStructure = not na(lastPH) and not na(prevPH) and not na(lastPL) and not na(prevPL) and lastPH < prevPH and lastPL < prevPL
    int result = 0
    if bullishStructure
        result := BULLISH
    else if bearishStructure
        result := BEARISH
    else
        result := na(baseline) ? 0 : close >= baseline ? BULLISH : BEARISH
    result
"""
if old not in s:
    raise SystemExit('target block not found')
s = s.replace(old, new, 1)
p.write_text(s)
