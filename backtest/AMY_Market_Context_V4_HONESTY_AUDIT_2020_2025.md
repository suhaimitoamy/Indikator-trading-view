# AMY Market Context V4 — Audit Kejujuran Pasar 2020–2025

## Tujuan

Audit ini menguji **kejujuran indikator terhadap kondisi pasar**, bukan sekadar memastikan kode Pine berjalan. Pengujian memakai seluruh data XAUUSD Januari 2020–Desember 2025 dan tidak memilih contoh chart secara manual.

## Dataset dan rekonstruksi

- 72 arsip bulanan XAUUSD.
- 2.080.540 candle M1 setelah duplikasi batas bulan dibuang.
- 416.229 candle M5.
- 138.750 candle M15.
- OHLC tanpa nilai kosong atau candle rusak.
- M5 dan M15 diverifikasi ulang dari agregasi M1; selisih maksimum hanya 0,005 karena pembulatan.
- Logika Market Context M15, POI, sweep, DOL, protected structure, key liquidity, PDH/PDL, Asia, Midnight Open, dan claim filter direkonstruksi dari file Pine pada branch backtest.

## Aturan audit independen

1. Semua event hanya boleh memakai candle yang sudah tutup; tidak ada data masa depan.
2. Wick menentukan sentuhan zona dan sweep. Close menentukan kegagalan, invalidasi, serta acceptance.
3. Zona baru boleh dinilai setelah minimal satu candle M15 tertutup setelah pembentukannya.
4. **Respect**: setelah sentuhan, harga bergerak keluar dari batas zona minimal 0,50 ATR M15 ke arah yang semestinya sebelum terjadi acceptance.
5. **Strong respect**: pergerakan minimal 1,00 ATR M15.
6. **Decisive break/acceptance**: dua close M5 berturut-turut di luar batas terjauh zona.
7. Horizon reaksi zona dan sweep: 4 jam.
8. Label `Failed` diuji lebih ketat: dalam 30 menit setelah label, minimal 4 dari 6 close M5 harus bertahan di luar zona dan harga melanjutkan minimal 0,25 ATR. Jika cepat kembali, diklasifikasikan quick reclaim.
9. Target V4 diuji sesuai horizon asli indikator: Protected 1 jam, key liquidity/Asia/MO/POI 4 jam, PDH/PDL 8 jam, risk 4 jam.

## Hasil utama

### 1. Zona mentah FVG dan Order Block

| Objek | Dibentuk | Tersentuh sebelum diganti | Respect ≥0,5 ATR | Break lebih dahulu | Strong respect ≥1 ATR |
|---|---:|---:|---:|---:|---:|
| FVG | 28,363 | 15,267 (53.83%) | 56.27% | 41.51% | 37.77% |
| Order Block | 34,223 | 17,722 (51.78%) | 63.08% | 34.53% | 40.70% |

- 46.17% FVG dan 48.21% OB diganti oleh zona baru sebelum sempat disentuh. Artinya engine konteks hanya menyimpan zona terbaru per arah; ia tidak mempertahankan seluruh zona yang pernah dibuat.
- FVG mentah menghasilkan respect bermakna pada 56.27% sentuhan. OB lebih baik pada 63.08%.
- Label `Failed` menjadi acceptance berkelanjutan hanya 62.66% untuk FVG dan 62.48% untuk OB. Sekitar 37% cepat direclaim.

**Kesimpulan zona mentah:** indikator benar dalam mencatat bahwa zona tersentuh, termitigasi, atau ditutup melewati batas. Namun zona mentah belum cukup akurat untuk menyimpulkan bahwa harga pasti respect atau bahwa satu close di luar zona sudah menjadi acceptance permanen.

### 2. Sweep dan Draw on Liquidity mentah

- Sweep M15 diuji: 9,329 event.
- Reaksi reversal minimal 0,5 ATR terjadi lebih dahulu pada 77.99% event.
- Target DOL mentah benar-benar tercapai hanya 31.31%.
- DOL mentah invalid 49.29%, expired 7.11%, dan abandoned 12.29%.

**Kesimpulan DOL mentah:** sweep cukup sering menghasilkan reaksi awal, tetapi tidak berarti harga akan mencapai likuiditas berlawanan. DOL mentah harus tetap berstatus observasi.

### 3. Klaim yang lolos filter V4

| Klaim | Event | Akurasi | Bull | Bear |
|---|---:|---:|---:|---:|
| PROTECTED_1H | 5,085 | 92.88% | 93.64% | 92.11% |
| VALIDATED_RISK_4H | 527 | 85.58% | 85.66% | 85.48% |
| VALIDATED_DOL | 116 | 92.24% | 91.94% | 92.59% |
| KEY_LIQUIDITY_4H | 22,819 | 82.34% | 83.31% | 81.28% |
| PDH_PDL_8H | 397 | 85.64% | 83.77% | 88.17% |
| ASIA_TARGET_4H | 632 | 86.87% | 86.40% | 87.38% |
| MIDNIGHT_OPEN_RETEST_4H | 1,866 | 86.44% | 87.25% | 85.61% |
| POI_REVISIT_4H | 3,167 | 83.11% | 84.62% | 81.74% |

- Total seluruh klaim tervalidasi/konteks: 34.609 event, 29.204 berhasil; akurasi berbobot 84,38%.
- Rata-rata sederhana antarjenis klaim: 86,89%.
- Validated DOL mencapai 92,24%, tetapi hanya muncul 116 kali—sekitar 1,24% dari 9.329 DOL mentah. Filter sangat selektif.
- Validated Risk menghasilkan 85,58%, hampir sama dengan angka 85,55% yang tertulis di Pine.
- Protected bullish 93,64% dan bearish 92,11%, sangat dekat dengan angka indikator 93,47% dan 91,86%.

### 4. Stabilitas tahun 2025

| Klaim | Event 2025 | Akurasi 2025 |
|---|---:|---:|
| PROTECTED_1H | 859 | 92.78% |
| VALIDATED_RISK_4H | 82 | 87.80% |
| VALIDATED_DOL | 15 | 93.33% |
| KEY_LIQUIDITY_4H | 3,828 | 82.71% |
| PDH_PDL_8H | 85 | 85.88% |
| ASIA_TARGET_4H | 102 | 89.22% |
| MIDNIGHT_OPEN_RETEST_4H | 312 | 81.41% |
| POI_REVISIT_4H | 554 | 84.48% |

- Seluruh klaim 2025 masih berada di atas 80%.
- Midnight Open turun menjadi 81,41%, paling lemah pada 2025 tetapi masih melewati batas 80%.
- FVG mentah 2025 respect 57,63%; OB mentah 61,78%. Ini menegaskan bahwa kekuatan indikator berasal dari filter V4, bukan dari semua zona mentah.

## Putusan audit

**Indikator ini memang mampu mencatat kondisi pasar, tetapi kemampuan itu tidak merata.**

- **Layak dipercaya sebagai pencatat:** sentuhan, mitigasi, sweep, protected structure, dan status terminal.
- **Layak dipercaya untuk klaim ke depan hanya ketika marker tervalidasi muncul:** hasilnya sekitar 82–92%.
- **Tidak layak diperlakukan sebagai prediksi hanya karena sebuah FVG, OB, sweep, atau DOL mentah muncul.**
- **Label Failed belum sama dengan acceptance kuat:** sekitar 37% kegagalan zona direclaim dengan cepat.
- **DOL mentah paling berbahaya bila dianggap prediksi:** target hanya tercapai sekitar 31%; validated DOL jauh lebih baik tetapi sangat jarang.

## Batasan

- Threshold indikator memang dibentuk dari data 2020–2025, sehingga pengujian periode yang sama tetap bersifat in-sample. Pemisahan per tahun menunjukkan kestabilan, tetapi belum menggantikan pengujian pada data baru setelah 2025.
- Audit ini menilai engine Market Context V4 dan klaim assistant, bukan kualitas estetika seluruh box ICT dasar.
- Hasil dihitung dari data OHLC; urutan intrabar yang terjadi di dalam satu candle hanya dapat dipastikan sampai tingkat M1 yang tersedia.

## Rekomendasi status di indikator

- `RAW/OBSERVATION`: FVG, OB, sweep, DOL mentah, near invalid mentah.
- `VALIDATED CONTEXT`: key liquidity, PDH/PDL, Asia, MO, POI revisit setelah filter.
- `VALIDATED CLAIM`: protected, risk, dan validated DOL.
- Ganti makna visual `Failed` menjadi **close di luar zona**, bukan otomatis **acceptance**, kecuali syarat persistence tambahan terpenuhi.
