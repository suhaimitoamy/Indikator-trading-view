from pathlib import Path

p = Path('Amy-SMC-X.pine')
s = p.read_text()

old = """// PASSED CORE — Jun-Jul 2026 backtest checkpoint.\n// Final Bias is driven only by components already accepted: HTF Swing, Swing Structure, Internal Structure, and Liquidity Context.\n// Dealing Range and Pattern remain visible/contextual but do not influence the accepted core until their own logic passes.\n"""
new = """// FINAL ALL-PASSED CHECKPOINT — all accepted Amy SMC X modules are consolidated in this file.\n// Final Bias keeps the already-passed core weights (HTF Swing, Swing Structure, Internal Structure, Liquidity Context).\n// Pattern / qualified CHoCH / qualified Valid Break stay as independent confirmation layers instead of being double-counted\n// into Final Bias, because their evidence is derived from the same underlying structure/liquidity state. Their best passed\n// filters remain active for chart labels, alerts and downstream Target qualification.\n"""
if old not in s:
    raise SystemExit('final bias checkpoint block not found')
s = s.replace(old, new, 1)

old2 = """// Next Move uses only accepted directional inputs. Event History remains the short-term refinement layer.\n"""
new2 = """// FINAL ALL-PASSED NEXT MOVE — preserve the passed directional core and Event History refinement.\n// Newly passed predictive modules remain corroboration layers, preventing correlated signals from being counted twice.\n"""
if old2 not in s:
    raise SystemExit('next move checkpoint block not found')
s = s.replace(old2, new2, 1)

marker = """alertcondition(amyQualifiedBSLSweep or amyQualifiedSSLSweep, 'Liquidity Sweep', 'Qualified liquidity sweep detected')\n"""
insert = """// FINAL CONSOLIDATION LOCK\n// Passed modules present in Amy SMC X: Internal/Swing/HTF structure, Liquidity Context, Event History, Next Move,\n// Final Bias, EQH/EQL, Weak/Strong H-L, Daily/Weekly/Monthly H-L, Dealing Range, FVG, Order Block, Invalidation,\n// Confidence, OTE, Fibonacci Extension, Pattern, qualified BOS/CHoCH, qualified Sweep/Valid Break, and Target.\n// Future tuning must not overwrite a better passed profile with a worse result.\n\n""" + marker
if marker not in s:
    raise SystemExit('alert marker not found')
s = s.replace(marker, insert, 1)

p.write_text(s)
