# AMY Simple ATR Bot v6 — Full-History Monthly Research

## Status

- Instrument: XAUUSD BID
- Data tersedia: Januari 2019 sampai Juli 2026 (91 bulan)
- Timeframe diuji: M5 dan M15
- Semua sesi diperlakukan sama
- SL / TP: 10 / 10 poin harga
- Entry: open candle berikutnya setelah sinyal candle close
- Biaya simulasi: 0,3 poin per trade
- Resolusi pemeriksaan SL/TP: M1
- Jika SL dan TP tersentuh pada candle M1 yang sama, SL dianggap lebih dahulu

## Pemisahan data

Parameter dipilih tanpa memakai periode pemeriksaan akhir:

- Development: Januari 2019–Desember 2023
- Validation: Januari 2024–Desember 2025
- Holdout: Januari–Juli 2026

## Pelajaran dari v5

V5 terlalu selektif pada kondisi tertentu tetapi tidak konsisten sepanjang sejarah. Pada Januari 2019–Juli 2026, jumlah dua pengujian independen M5 dan M15 menghasilkan 3.021 trade, win rate 51,97%, dan net +283,7 poin. Beberapa tahun tetap negatif.

Eksperimen v6 menunjukkan aturan yang paling sederhana dan lebih tahan lintas tahun adalah:

1. ATR trailing stop dengan Key Value 2,0 dan ATR 20.
2. EMA 80 dengan kemiringan dua bar.
3. Candle sinyal hanya diterima jika body maksimal 40% dari seluruh range candle. Artinya total wick minimal 60%.

Filter body/wick membuang candle sinyal yang terlalu penuh dan cenderung menjadi entry terlambat, tanpa membatasi sesi atau arah perdagangan.

## Parameter v6

| Parameter | Nilai |
|---|---:|
| Key Value | 2,0 |
| ATR Period | 20 |
| EMA Length | 80 |
| EMA Slope | 2 bar |
| Maksimum body/range | 0,40 |
| Stop Loss | 10 poin |
| Take Profit | 10 poin |

## Hasil Januari 2019–Juli 2026

| Hasil | M5 | M15 |
|---|---:|---:|
| Trade | 1.114 | 461 |
| Menang | 591 | 258 |
| Win rate | 53,05% | 55,97% |
| Profit factor setelah biaya | 1,064 | 1,197 |
| Net setelah biaya | +345,8 | +411,7 |
| Max drawdown | 176,7 | 87,7 |
| Loss beruntun maksimum | 7 | 5 |

Jumlah dua pengujian independen:

- Trade: 1.575
- Win rate: 53,90%
- Net setelah biaya: +757,5 poin
- Bulan positif: 53 dari 91
- Bulan negatif: 38 dari 91
- Seluruh tahun kalender yang tersedia berakhir positif

> Catatan: hasil gabungan adalah penjumlahan pengujian M5 dan M15 yang berdiri sendiri. Itu bukan simulasi satu akun yang membuka kedua timeframe secara bersamaan.

## Hasil per tahun

| Tahun | Trade | Win rate | Net |
|---|---:|---:|---:|
| 2019 | 126 | 53,17% | +42,2 |
| 2020 | 229 | 54,59% | +141,3 |
| 2021 | 203 | 55,67% | +169,1 |
| 2022 | 208 | 53,85% | +97,6 |
| 2023 | 198 | 53,03% | +60,6 |
| 2024 | 202 | 53,96% | +99,4 |
| 2025 | 242 | 52,07% | +27,4 |
| 2026 Jan–Jul | 167 | 55,09% | +119,9 |

## Pemeriksaan holdout 2026

2026 tidak dipakai memilih parameter. Hasil Januari–Juli 2026:

- 167 trade
- Win rate 55,09%
- Net +119,9 poin setelah biaya 0,3

## Sensitivitas kualitas data

Terdapat sejumlah celah pendek pada arsip M1. Setelah semua trade yang melintasi celah 2–60 menit dikeluarkan:

- 1.405 trade tersisa
- Win rate 53,81%
- Net +648,5 poin

Arah kesimpulan tetap positif, tetapi hasil tetap bergantung pada kualitas feed dan urutan harga intramenit.

## Sensitivitas biaya

Jumlah dua pengujian independen:

| Biaya per trade | Net |
|---:|---:|
| 0,00 | +1.230,0 |
| 0,30 | +757,5 |
| 0,50 | +442,5 |
| 0,75 | +48,8 |
| 1,00 | −345,0 |

Karena SL dan TP sama-sama 10 poin, biaya transaksi sangat berpengaruh. Spread, komisi, dan slippage broker nyata harus dimasukkan sebelum dipakai live.

## Batas validasi

Backtest ini adalah replay candle lokal, bukan hasil compiler dan broker emulator native TradingView. Kode Pine perlu diverifikasi kembali di Strategy Tester pada simbol, broker feed, dan pengaturan biaya yang sama.
