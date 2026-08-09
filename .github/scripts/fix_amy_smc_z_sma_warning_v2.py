from pathlib import Path

p = Path('Amy-SMC-Z.pine')
s = p.read_text()
old = """    float baseline = ta.sma(close, length * 2)\n"""
new = """    float baselineSum = 0.0\n    int baselineLength = length * 2\n    for offset = 0 to baselineLength - 1\n        baselineSum += close[offset]\n    float baseline = baselineSum / baselineLength\n"""
if s.count(old) != 1:
    raise SystemExit(f'expected exactly one ta.sma baseline, found {s.count(old)}')
s = s.replace(old, new, 1)
if 'ta.sma(' in s:
    raise SystemExit('ta.sma still present after patch')
p.write_text(s)
