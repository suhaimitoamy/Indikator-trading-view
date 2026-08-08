from pathlib import Path

x_path = Path('Amy-SMC-X.pine')
y_path = Path('Amy-SMC-Y.pine')

if not x_path.exists():
    raise SystemExit('Amy-SMC-X.pine not found')
if y_path.exists():
    raise SystemExit('Amy-SMC-Y.pine already exists; refusing to overwrite')

x = x_path.read_text()

indicator_x = "indicator('Amy SMC X', 'Amy SMC X', overlay = true, max_labels_count = 500, max_lines_count = 500, max_boxes_count = 500)"
if indicator_x not in x:
    raise SystemExit('Amy SMC X indicator declaration not found')
if '// FINAL CONSOLIDATION LOCK' not in x:
    raise SystemExit('final consolidation lock not found in Amy SMC X')
if 'Round 5' not in x and 'ROUND 5' not in x:
    raise SystemExit('Round 5 predictive profile not found in Amy SMC X')

baseline_note = """// FINAL LONG-HISTORY BASELINE — XAUUSD 2010–2026 validation checkpoint.\n// The current Amy SMC X configuration beat the previous settings on the same long-history replay, so its logic is frozen as the reference baseline.\n// Further predictive development continues in Amy SMC Y; Amy SMC X should not be changed unless explicitly requested.\n\n"""
marker = '// FINAL CONSOLIDATION LOCK\n'
if baseline_note not in x:
    x = x.replace(marker, baseline_note + marker, 1)
    x_path.write_text(x)

# Create Y as an exact behavioral copy of the finalized X baseline.
y = x.replace(indicator_x, "indicator('Amy SMC Y', 'Amy SMC Y', overlay = true, max_labels_count = 500, max_lines_count = 500, max_boxes_count = 500)", 1)
y = y.replace('// AMY SMC X — INDEPENDENT CHART MODULES', '// AMY SMC Y — INDEPENDENT CHART MODULES')

y_header = """// AMY SMC Y DEVELOPMENT COPY\n// Baseline: finalized Amy SMC X after the 2010–2026 full-history validation.\n// NON-PREDICTIVE LOCK: structure/context modules that already perform their descriptive/functional jobs are inherited unchanged.\n// Development scope for Amy SMC Y is the predictive layer unless the user explicitly changes that rule.\n\n"""
addon_marker = '// AMY SMC ADD-ON\n'
if addon_marker not in y:
    raise SystemExit('Amy SMC add-on marker not found')
y = y.replace(addon_marker, y_header + addon_marker, 1)

y_path.write_text(y)

# Safety checks: Y must keep the LuxAlgo license and differ behaviorally only by identity/comments.
if not y.startswith('// This work is licensed under a Attribution-NonCommercial-ShareAlike 4.0 International'):
    raise SystemExit('license header missing from Amy SMC Y')
if "indicator('Amy SMC Y', 'Amy SMC Y'" not in y:
    raise SystemExit('Amy SMC Y declaration was not written')
