# AMY Market Context Experiment V5 — Backtest Kejujuran 2025

## Tujuan

Menguji kejujuran indikator terhadap kondisi pasar XAUUSD sepanjang 2025 setelah filter eksperimen diterapkan pada FVG, Order Block, dan DOL. Ini bukan pengujian apakah kode dapat berjalan.

## Data dan aturan

- Data: XAUUSD M5 dan M15 Januari–Desember 2025, dengan histori 2020–2024 sebagai warm-up struktur dan ATR.
- Event Market Context M15 baru dianggap terlihat 30 menit setelah timestamp candle pembentuk, sesuai pola `request.security("15", engine)` yang di dalam engine kembali memakai data `[1]`.
- Zona yang sudah tersentuh sebelum saat tampil dikategorikan **stale at birth**, bukan keberhasilan forward.
- Respect: harga bergerak minimal 0,50 ATR M15 ke arah zona sebelum dua close M5 berturut-turut menerima harga di luar zona.
- Strong respect: minimal 1,00 ATR M15.
- Horizon: 4 jam atau sampai zona diganti.
- Failure persistence: setelah status Failed, minimal 4 dari 6 close M5 tetap di luar zona dan harga melanjutkan minimal 0,25 ATR.

## Hasil FVG dan Order Block

| Komponen | Zona terbentuk | Stale saat tampil | Zona bersih yang tersentuh | Respect ≥0,5 ATR | Strong respect ≥1 ATR | Failed benar-benar bertahan |
|---|---:|---:|---:|---:|---:|---:|
| FVG | 734 | 110 (14,99%) | 352 | 285 (80,97%) | 52,27% | 70,49% |
| Order Block | 999 | 264 (26,43%) | 437 | 357 (81,69%) | 57,67% | 74,69% |

Perbandingan dengan logika lama pada 2025:

| Komponen | Respect lama | Respect filter eksperimen |
|---|---:|---:|
| FVG | 57,63% | 80,97% pada zona bersih |
| Order Block | 61,78% | 81,69% pada zona bersih |

Catatan:

- Filter membuang sekitar 85% FVG mentah dan 83% OB mentah, sehingga zona jauh lebih selektif.
- Kenaikan di atas 80% hanya berlaku setelah zona yang sudah tersentuh sebelum tampil dikeluarkan.
- Status Failed membaik, tetapi masih sekitar 29,51% FVG dan 25,31% OB tidak menunjukkan acceptance berkelanjutan.
- Sebanyak 39,51% FVG Failed dan 36,93% OB Failed mengalami setidaknya satu reclaim close dalam 30 menit pertama, walaupun sebagian tetap melanjutkan kemudian.

## Hasil DOL eksperimen

- Sweep yang tetap tercatat: 2.752.
- Sweep yang lolos filter menjadi DOL: 93 (3,38%).
- Engine internal melabeli Reached: 69 dari 93 (74,19%).
- Namun 57 dari 93 DOL (61,29%) sudah menyentuh target sebelum DOL terlihat di layar.
- DOL forward yang benar-benar bersih: 36.
- Target tercapai setelah DOL terlihat: 13 dari 36 (**36,11%**).
- Invalid lebih dahulu: 23 dari 36 (**63,89%**).

### Putusan DOL

Filter jarak 1 ATR dan keselarasan bias belum menyelesaikan masalah. Angka internal 74,19% terlihat tinggi karena target yang tersentuh selama keterlambatan tampilan ikut tercatat sebagai keberhasilan. Setelah hanya menghitung pergerakan setelah sinyal benar-benar terlihat, akurasinya 36,11%.

Angka pemeriksaan awal sekitar 83,95% tidak valid sebagai akurasi forward karena belum menghapus event stale-at-birth.

## Klaim yang tidak terdampak perubahan

Karena logika struktur dan key-level berikut tidak diubah, hasil regresi 2025 tetap:

| Klaim | Event | Akurasi 2025 |
|---|---:|---:|
| Protected Structure 1H | 859 | 92,78% |
| Validated Risk 4H | 82 | 87,80% |
| Key Liquidity 4H | 3.828 | 82,71% |
| PDH/PDL 8H | 85 | 85,88% |
| Asia Target 4H | 102 | 89,22% |
| Midnight Open Retest 4H | 312 | 81,41% |

Validated DOL, POI Revisit, dan Asia Entry tetap dinonaktifkan oleh flag eksperimen sampai retest selesai.

## Putusan akhir

1. **FVG eksperimen: lulus bersyarat.** Zona bersih mencapai 80,97%, tetapi perlu perlindungan stale-at-birth.
2. **Order Block eksperimen: lulus bersyarat.** Zona bersih mencapai 81,69%, tetapi 26,43% sudah tersentuh sebelum tampil.
3. **Status Failed: belum sepenuhnya jujur.** Acceptance berkelanjutan baru 70–75%.
4. **DOL eksperimen: gagal.** Akurasi forward bersih hanya 36,11%; jangan diaktifkan sebagai validated target.
5. **Protected dan klaim independen lain tetap aman**, karena mesin struktur M15 tidak diubah.

## Perbaikan berikut yang diperlukan

- Saat zona pertama kali tampil, cek seluruh M5/M1 sejak candle pembentuk selesai. Jika sudah tersentuh, tandai `Touched/Mitigated` atau buang; jangan tampilkan `Fresh`.
- DOL harus memeriksa apakah target pernah disentuh sejak sweep terbentuk, bukan hanya candle M5 saat marker muncul.
- Hilangkan keterlambatan ganda pada engine M15: jangan memakai snapshot `[1]` di dalam engine jika `request.security(..., lookahead_off)` sudah menjamin candle tertutup.
- Status Failed sebaiknya memerlukan dua close di luar zona plus continuation minimum ATR, bukan dua close saja.

## Batasan

Backtest direkonstruksi dari kode Pine dan data OHLC, bukan dieksekusi langsung oleh mesin TradingView. Rekonstruksi mesin lama cocok sekitar 96,6% terhadap timestamp event DOL yang tersimpan; perbedaan kecil berasal dari detail pivot/tie dan batas data. Temuan keterlambatan 30 menit diverifikasi dari koordinat zona dan timestamp event yang tercatat pada output sebelumnya.
