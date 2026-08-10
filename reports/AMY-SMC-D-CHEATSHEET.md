# Amy SMC D — Directional Accuracy Cheat-Sheet

**Baseline:** `Amy-SMC-D.pine`
**Purpose:** referensi baku pembacaan dashboard manual; directional/context only.
**Data:** raw XAUUSD 2005–Jul 2026; OOS 2012–Jul 2026 bila dicantumkan; 2004 warm-up.
**Low-confidence:** <30 evaluable events per yearly/window slice.

## Final baseline definition

Amy SMC D = **logic Amy SMC Z asli + hanya tiga fix descriptive Dealing Range**:

- **M5:** pure-location; Premium >=70% bearish, Discount <=30% bullish.
- **M15:** pure-location; Premium >=60% bearish, Discount <=40% bullish.
- **H1:** high/low dari **previous 240 closed H1 bars** (`high[1]`/`low[1]`); Premium >=55% bearish, Discount <=45% bullish; tanpa Swing/Internal/HTF context gate.

D **tidak membawa** M5 TGT2 segmented target/expiry dari B dan **tidak membawa** ATR trade-management M15/H1 dari B-LAB. Original Z logic, termasuk Z Target V1, tetap utuh.

## RELIABLE / FIXED only

| Field | Status | M5 | M15 | H1 | Catatan manual |
|---|---|---:|---:|---:|---|
| Dealing Range | **FIXED** | **65.54%** full; OOS 65.41%, 15/15 HC | **62.48%** full; OOS 62.98%, 15/15 HC | **64.33%** full, N=1,214, 22/22 HC; **65.39% OOS**, N=887, 15/15 HC | Descriptive location state; H1 replay memakai opposite directional flip across equilibrium dan censor event lintas tahun |
| Swing Structure — fresh | **RELIABLE** | **81.42%**, N=5,822 | **88.97%**, N=1,941 | **94.55%**, N=422; low yearly sample | Baca hanya saat baru flip |
| Internal Structure — fresh | **RELIABLE** | **69.27%**, N=40,283 | **74.44%**, N=14,172 | **80.15%**, N=3,617 | Fresh structure evidence |
| HTF Swing — fresh | **RELIABLE** | **68.94%**, N=52,961 | **76.20%**, N=12,554 | **82.16%**, N=2,926 | Jangan invert |
| Final Bias — fresh | **RELIABLE when fresh** | **71.41%**, N=41,820 | **77.87%**, N=11,433 | **84.20%**, N=2,822 | Fresh only; stale bukan primary direction |
| Next Move | **RELIABLE** | **73.62%**, N=944; OOS 74.89% | **77.87%**, N=11,433; OOS 77.98% | **83.34%**, N=2,906; OOS 83.92% | Primary forward direction; invalidation-based, tanpa TP scoring |
| Sweep Continuation | **RELIABLE M5/M15** | **79.86%**, N=4,678 | **84.72%**, N=1,616 | **92.48%**, N=319; low yearly sample | Arah setelah raw sweep |
| Raw Valid Break | **RELIABLE** | **83.99%**, N=10,096 | **89.73%**, N=3,565 | **96.07%**, N=814 | Strong structural-survival evidence |
| Qualified Valid Break | **RELIABLE where sampled** | **88.92%**, N=352; low yearly sample | **90.66%**, N=1,328; 21/22 HC | **97.82%**, N=412; low yearly sample | Hormati low-sample flag |
| Qualified CHoCH | **RELIABLE where sampled** | **78.50%**, N=963; 21/22 HC | **92.60%**, N=473; low yearly sample | **97.56%**, N=82; low sample | Evidence kuat saat muncul |
| Raw Pattern | **RELIABLE** | **65.21%**, N=180,069 | **70.97%**, N=56,662 | **75.03%**, N=12,634 | Raw candlestick evidence |
| Qualified Pattern | **RELIABLE M15/H1** | **67.45%**, N=424; low yearly coverage | **90.56%**, N=5,108; 22/22 HC | **93.60%**, N=1,359; 22/22 HC | Prefer qualified M15/H1 |

Continuous Swing/Internal/HTF/Final Bias, raw continuous Liquidity, Event History, raw Sweep, dan Qualified BOS sengaja tidak dimasukkan karena statusnya SUBSTITUTE/CONTEXT ONLY/LOW SAMPLE, bukan standalone daily directional read yang disahkan.
