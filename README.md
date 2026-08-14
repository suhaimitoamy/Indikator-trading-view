# XAUUSD Smart Context Project

Repositori ini berisi koleksi indikator dan strategi TradingView untuk **XAUUSD (Gold)** berbasis Smart Money Concepts (SMC), ICT Concepts, price action, breakout-retest, context narration, projection, entry trigger, dan risk management.

## Index Repo

| File | Tipe | Status | Isi Utama |
|---|---|---|---|
| `README.md` | Dokumentasi | Aktif | Dokumentasi utama dan index seluruh isi repo. |
| `Amy-FX-Scalper-Engine.pine` | Indicator Pine v6 | Aktif | Port engine scalper Amy FX Preview: 10 driver setup, gate BT6/BT6.1, AMD, lifecycle entry/TP/SL, dashboard, dan alert close-confirmed. |
| `Amy-Swing-Flow.pine` | Indicator Pine v6 | Aktif | Mesin swing adaptif yang dibangun dari nol tanpa future bars; reversal ATR, context trend/range, grade sinyal, ZigZag terkunci, dan alert. |
| `Swing high & low` | Indicator Pine v5 | Diperbaiki | Swing pivot terkonfirmasi; label tidak dipindah/dihapus, alternasi swing, filter ATR/EMA, struktur HH/HL/LH/LL, dan alert. |
| `AMY_ICT_NextGen.pine` | Indicator Pine v5 | Aktif | Market mapping utama dengan session, BOS/MSS, BSL/SSL, PDH/PDL, PWH/PWL, OB/FVG, liquidity draw, rejection context, entry map, dan dashboard. |
| `indikator-v1.pine` | Strategy Pine v6 | Aktif | XAUUSD Smart Context + Entry PRO Non-Repaint dengan session filter, HTF bias, structure, FVG, OB, OTE, Asia range, confluence score, entry BUY/SELL, SL/TP, dan alert. |
| `indikator-v2.pine` | Strategy Pine v6 | Aktif | Versi production lanjutan dari v1 dengan dashboard, trade level, signal memory, quality tag, compact/full mode, dan visual trade plan. |
| `indikator-v3.pine` | Strategy Pine v6 | Aktif | Versi modular dengan Context Engine, Warning Engine, Entry Engine, Risk Engine, risk-based sizing, session-native timezone, premium/discount guide, dan debug label. |
| `indikator-v10.pine` | Strategy Pine v6 | Aktif | V10 Ultimate Strategy. Menggabungkan SMC, ICT PO3, Judas Swing, Premium/Discount, MSS, OB/FVG, scoring 0-100, dynamic risk, trailing stop, breakeven, dashboard, dan alert. |
| `v10.md` | Dokumentasi | Aktif | Dokumentasi khusus `indikator-v10.pine`: ringkasan, fitur, cara penggunaan, dan evolusi versi. |
| `ICT` | Indicator Pine v5 | Aktif | ICT Concepts dengan MSS, BOS, displacement, volume imbalance, OB, liquidity, FVG/IFVG, BPR, NWOG/NDOG, Fibonacci, dan killzones. |
| `ICT 2` | Indicator Pine v5 | Aktif | Iterasi ICT Concepts dengan struktur utama ICT, liquidity, OB, FVG, NWOG/NDOG, Fibonacci, dan killzones. |
| `ICT 3` | Indicator Pine v5 | Aktif | Iterasi ICT Concepts berbasis struktur MSS/BOS, liquidity map, OB, FVG, dan killzones. |
| `ICT 5` | Indicator Pine v5 | Aktif | Iterasi ICT Concepts dengan pengembangan struktur, liquidity, FVG, OB, dan session tools. |
| `ICT 6` | File tidak valid | Perlu diperiksa | Isi file bukan Pine Script valid. |
| `ICT 8` | Indicator Pine v5 | Aktif | ICT Concepts dengan tambahan context/roadmap/trigger/trade plan visual. |
| `ICT 11` | Indicator Pine v5 | Aktif | Versi ICT Concepts terbaru di repo dengan MSS, BOS, liquidity, OB, FVG, NWOG/NDOG, Fibonacci, killzones, dan visual context. |
| `V4` | Indicator Pine v6 | Aktif | XAUUSD Context Narrator v1.3 dengan session, HTF bias, support/resistance, Asia range, context state, narrative dashboard, dan scenario text. |
| `V9` | Indicator Pine v6 | Aktif | XAUUSD Context Narrator v9.7 Full Dash dengan adaptive logic, dealing range, POI refinement, OB/FVG, execution zone, projection path, SL/TP, trade lock, dan dashboard. |
| `V10` | Indicator Pine v6 | Aktif | XAUUSD Context Narrator v10 Visual Pro dengan visual clean style, swing high/low, Asia high/low, execution zone, OB/FVG, projected path, trigger marker, dashboard, SL/TP, dan trade plan. |
| `V11` | Indicator Pine v6 | Aktif | XAUUSD SnR Breakout & Retest V5 dengan S&R MTF, breakout normal, momentum breakout langsung, retest trigger, pinbar/engulfing, dan label BUY/SELL. |
| `GCX-Matrix-V12.pine` | Indicator Pine v5 | Aktif | GCX Matrix V12. Gold Context Execution Matrix dengan Context Engine, Warning Engine, Entry Engine, Risk Engine, projection, dashboard, delta/order-flow proxy, dan no-trade filter. |
| `GCX-Entry-Only-V1.pine` | Indicator Pine v5 | Aktif | GCX Entry Only V1. Fokus entry trigger tanpa dashboard, HTF bias, context score, atau projection score. Menggunakan vote trigger, retest, sweep, S/R rejection, candle pattern, FVG, OB, breakout, delta filter, SL/TP, dan alert. |

## Indicator Amy 2026

### `Amy-FX-Scalper-Engine.pine`

Port TradingView dari snapshot engine Amy FX Preview. Deteksi memakai candle yang sudah close dan registry timeframe M15/M30/H1/H4. Driver yang tersedia: FVG, CRT, Order Block, Breaker Block, Retest BOS, Trendline Break & Retest, EMA Pullback, False Breakout/Judas, Range Expansion, dan AMD. Engine mempertahankan gate BT6/BT6.1, structural stop dengan ATR buffer, target +10/+20 poin, batas hold 24 jam, serta alert dinamis.

> Catatan: lifecycle aplikasi aslinya dievaluasi pada candle M1. Untuk replay lifecycle yang benar-benar presisi, gunakan level setup indikator pada data M1.

### `Amy-Swing-Flow.pine`

Mesin swing kausal yang dibuat dari nol—tidak memakai `ta.pivothigh`, `ta.pivotlow`, future bars, atau lookahead. Kandidat ekstrem tetap internal; label baru dibuat pada candle reversal yang sudah close dan tidak pernah dipindah atau dihapus. Context adaptif membedakan trend dan range menggunakan EMA, DMI/ADX, RSI, structure break, serta kekuatan reversal ATR.

### `Swing high & low`

Versi lama sudah diperbaiki menjadi confirmed non-repaint. Pivot tetap memerlukan right bars sebagai delay konfirmasi, tetapi setelah label dibuat, label tersebut tidak akan hilang walaupun arah berikutnya berbeda. Pilihan `Bar konfirmasi` menunjukkan waktu sinyal yang jujur; `Titik swing` hanya memindahkan posisi visual ke ekstrem historis yang baru diketahui setelah konfirmasi.

## Struktur Sistem

### Smart Context Strategy Series

File strategy untuk backtest dan eksekusi berbasis konteks market.

- `indikator-v1.pine`
- `indikator-v2.pine`
- `indikator-v3.pine`
- `indikator-v10.pine`

### ICT Concepts Series

File indikator ICT Concepts berbasis MSS, BOS, liquidity, OB, FVG, NWOG/NDOG, Fibonacci, dan killzones.

- `ICT`
- `ICT 2`
- `ICT 3`
- `ICT 5`
- `ICT 8`
- `ICT 11`

### Context Narrator Series

File indikator narasi market, dealing range, POI, projection, dashboard, dan trade plan visual.

- `V4`
- `V9`
- `V10`

### Breakout & Retest Series

File indikator khusus support/resistance, breakout, momentum breakout, dan retest.

- `V11`

### GCX Series

File indikator GCX untuk context matrix dan entry-only execution.

- `GCX-Matrix-V12.pine`
- `GCX-Entry-Only-V1.pine`

## Detail File

### `AMY_ICT_NextGen.pine`

Indikator market mapping utama dengan pembacaan struktur dan liquidity terintegrasi.

Fitur utama:

- Asia High/Low.
- PDH/PDL dan PWH/PWL.
- BOS/MSS dan structural invalidation.
- BSL/SSL dengan riwayat sweep spesifik.
- HTF bias dan EMA stack.
- Order Block dan Fair Value Gap.
- Premium/Discount.
- Predicted liquidity draw dengan rejection filter.
- Target liquidity terdekat pada dashboard.
- Compact entry map M5, M15, dan H1.

### `indikator-v1.pine`

Strategy awal untuk XAUUSD Smart Context + Entry PRO Non-Repaint.

Fitur utama:

- Session filter Asia, London, New York.
- HTF bias EMA 20/50.
- Support/resistance structure.
- Breakout dan retest.
- False break dan rejection.
- Fair Value Gap.
- Order Block.
- OTE zone.
- Asia range sweep.
- Buy/Sell confluence score.
- Entry BUY/SELL.
- SL/TP.
- Alert BUY/SELL.

### `indikator-v2.pine`

Versi production lanjutan dari v1.

Fitur utama:

- Semua fondasi v1.
- Dashboard compact/full.
- Signal memory.
- Quality tag A+/A/B/C/D.
- Visual entry, SL, TP.
- Trade state.
- Signal age.
- Panel informasi market real-time.

### `indikator-v3.pine`

Versi modular dengan pemisahan logic.

Fitur utama:

- Context Engine.
- Warning Engine.
- Entry Engine.
- Risk Engine.
- Risk-based position sizing.
- Session-native timezone.
- Premium/discount guide.
- Warning label.
- Entry label.
- Bias ribbon.
- Market state / impulse detection.
- Debug no-entry option.

### `indikator-v10.pine`

V10 Ultimate dalam format Strategy.

Fitur utama:

- Backtestable strategy.
- ICT Power of 3.
- Asia accumulation range.
- Judas Swing filter.
- London/New York execution session.
- HTF bias non-repaint.
- Premium/Discount zone.
- Market Structure Shift.
- Order Block.
- Fair Value Gap.
- Confluence score 0-100.
- Setup grade A+/A/B/C/Avoid.
- Dynamic risk management.
- Trailing stop ATR.
- Breakeven option.
- Professional dashboard.
- Buy/Sell alert.

### `v10.md`

Dokumentasi khusus untuk `indikator-v10.pine`.

Isi utama:

- Ringkasan V10 Ultimate.
- Fitur ICT PO3.
- Premium/Discount zone.
- Advanced scoring engine.
- Dynamic risk management.
- Professional dashboard.
- Cara penggunaan.
- Evolusi dari versi sebelumnya.

### `ICT`

ICT Concepts versi awal di repo.

Fitur utama:

- Market Structure.
- MSS.
- BOS.
- Displacement.
- Volume Imbalance.
- Order Block.
- Liquidity.
- FVG.
- IFVG.
- BPR.
- NWOG.
- NDOG.
- Fibonacci.
- Killzones.
- New York session.
- London Open session.
- London Close session.
- Asian session.

### `ICT 2`

Iterasi lanjutan ICT Concepts.

Fitur utama:

- MSS/BOS.
- Order Block.
- Liquidity boxes.
- Fair Value Gap.
- Implied Fair Value Gap.
- Balance Price Range.
- NWOG/NDOG.
- Fibonacci between selected objects.
- Killzones.

### `ICT 3`

Iterasi ICT Concepts dengan struktur visual dan liquidity.

Fitur utama:

- Market structure shift.
- Break of structure.
- Buyside liquidity.
- Sellside liquidity.
- Bullish/Bearish OB.
- Bullish/Bearish FVG.
- NWOG/NDOG.
- Killzone session.

### `ICT 5`

Iterasi ICT Concepts dengan pengembangan komponen SMC.

Fitur utama:

- Market Structures.
- Displacement.
- Volume Imbalance.
- Order Blocks.
- Liquidity.
- Fair Value Gaps.
- Balance Price Range.
- NWOG/NDOG.
- Fibonacci.
- Killzones.

### `ICT 6`

Status:

- File tidak berisi Pine Script valid.
- Perlu dicek ulang sebelum digunakan di TradingView.

### `ICT 8`

ICT Concepts dengan tambahan visual context dan trade plan.

Fitur utama:

- Market Structure.
- MSS.
- BOS.
- Displacement.
- Volume Imbalance.
- Order Block.
- Liquidity.
- FVG/IFVG.
- BPR.
- NWOG/NDOG.
- Fibonacci.
- Killzones.
- NX Context Engine.
- NX Structure Roadmap.
- NX Sequential Trigger Engine.
- NX Trade Plan Visuals.
- Projected zone.
- Execution zone.
- Trigger marker.
- Trade plan label.

### `ICT 11`

Versi ICT Concepts terbaru di repo.

Fitur utama:

- Market Structure.
- MSS.
- BOS.
- Displacement.
- Volume Imbalance.
- Order Block.
- Liquidity.
- FVG.
- IFVG.
- BPR.
- NWOG.
- NDOG.
- Fibonacci.
- Killzones.
- Session tools.
- Visual context.
- Trade plan support.

### `V4`

XAUUSD Context Narrator v1.3.

Fitur utama:

- Session Asia, London, New York.
- HTF bias.
- Structure timeframe.
- Support/resistance.
- Asia range.
- Sweep detection.
- Breakout detection.
- Retest state machine.
- Premium/discount context.
- Narrative engine.
- Scenario text.
- Mobile/Desktop dashboard.

### `V9`

XAUUSD Context Narrator v9.7 Full Dash.

Fitur utama:

- HTF validation.
- Dealing range.
- Anti-choppy filter.
- Adaptive Fibonacci zone.
- OB/FVG POI refinement.
- Buy/Sell execution zone.
- Trigger detection.
- Trade lock.
- SL/TP.
- Projected path.
- Full dashboard.
- Narrative trade plan.

### `V10`

XAUUSD Context Narrator v10 Visual Pro.

Fitur utama:

- Clean visual style.
- HTF validation.
- Dealing range.
- Asia range.
- Break and sweep engine.
- OB/FVG polished boxes.
- Buy/Sell execution zone.
- Projected path.
- False break marker.
- Trigger marker.
- SL/TP.
- Dashboard.
- Trade plan text.

### `V11`

XAUUSD SnR Breakout & Retest V5.

Fitur utama:

- Support/resistance MTF.
- Breakout normal.
- Momentum breakout langsung tanpa retest.
- Retest entry.
- Pinbar confirmation.
- Engulfing confirmation.
- Label BUY momentum.
- Label SELL momentum.
- Label BUY retest.
- Label SELL retest.

### `GCX-Matrix-V12.pine`

Gold Context Execution Matrix.

Fitur utama:

- Context Engine.
- Warning Engine.
- Entry Engine.
- Risk Engine.
- Session filter.
- HTF bias.
- Structure TF.
- Premium/Discount.
- FVG.
- Order Block.
- OTE.
- Liquidity sweep.
- Delta/order-flow proxy.
- Market regime filter.
- No-trade filter.
- Projection logic.
- Warning label.
- BUY/SELL signal.
- Entry, SL, TP1, TP2 visual.
- Dashboard.
- Alert.

### `GCX-Entry-Only-V1.pine`

Indicator entry trigger saja.

Fitur utama:

- Tidak memakai dashboard.
- Tidak memakai HTF bias.
- Tidak memakai context score.
- Tidak memakai projection score.
- Entry berdasarkan vote trigger.
- Breakout retest.
- Liquidity sweep reclaim/reject.
- Support/resistance rejection.
- Pinbar/engulfing.
- FVG reaction.
- Order Block reaction.
- Direct breakout optional.
- Delta filter.
- Signal cooldown.
- Reason label.
- Entry, SL, TP1, TP2 visual.
- Alert BUY/SELL.

## Cara Penggunaan

1. Buka file indikator atau strategy yang ingin digunakan.
2. Copy seluruh kode.
3. Buka TradingView.
4. Masuk ke Pine Editor.
5. Paste kode.
6. Klik **Add to Chart**.
7. Sesuaikan input di menu **Settings**.

## Catatan File

- `indikator-v10.pine` adalah **Strategy V10 Ultimate**.
- `V10` adalah **Indicator Context Narrator v10 Visual Pro**.
- `ICT 6` perlu dicek karena bukan Pine Script valid.
- File tanpa ekstensi seperti `ICT`, `ICT 2`, `V4`, `V9`, `V10`, dan `V11` tetap berisi script Pine dan bisa dicopy ke Pine Editor.

---
*Dibuat dengan dedikasi untuk menyempurnakan sistem trading XAUUSD.*
