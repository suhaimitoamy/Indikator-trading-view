# AMY Market Context V6 — Backtest Komponen Belum Lulus (2023)

## Ruang lingkup

Komponen yang sudah lulus tidak diuji dan tidak diubah. Pengujian hanya mencakup:

- Screened DOL / DOL mentah sebagai target;
- Validated DOL;
- Order Block POI Revisit.

Aturan yang digunakan sama dengan pengujian 2024:

- hanya candle yang sudah tutup;
- target yang sudah tersentuh sebelum marker muncul tidak dihitung;
- horizon target 4 jam;
- DOL harus searah bias, struktur valid, target dekat, dan candle sweep menutup kuat;
- OB Revisit hanya memakai OB fresh yang belum tersentuh, searah bias, dan berjarak maksimum 1,25 ATR.

## Hasil 2023

| Komponen | Event | Berhasil | Akurasi | Jan–Jun | Jul–Des | Status |
|---|---:|---:|---:|---:|---:|---|
| Screened DOL 4H | 22 | 16 | **72,73%** | 71,43% | 73,33% | Gagal |
| Validated DOL | 0 | 0 | — | — | — | Tetap dinonaktifkan |
| OB POI Revisit 4H | 74 | 61 | **82,43%** | 83,87% | 81,40% | Lulus pada 2023 saja |

## Gabungan 2023–2024

| Komponen | Event | Berhasil | Akurasi gabungan | Putusan |
|---|---:|---:|---:|---|
| Screened DOL 4H | 36 | 27 | **75,00%** | Gagal |
| Validated DOL | 0 | 0 | — | Tetap dinonaktifkan |
| OB POI Revisit 4H | 224 | 171 | **76,34%** | Gagal |

## Putusan

Tidak ada komponen baru yang boleh diaktifkan.

- DOL tetap gagal dan tidak stabil.
- Validated DOL tidak dapat diaktifkan karena sumber DOL belum lulus.
- OB Revisit memang mencapai 82,43% pada 2023, tetapi gagal pada 2024 dan akurasi gabungan hanya 76,34%.
- Semua komponen yang sebelumnya sudah lulus tetap dibekukan dan tidak disentuh.

## Catatan

Hasil 2023 adalah pengujian tahun terpisah menggunakan aturan V6 yang telah dikunci pada pengujian 2024. Tidak ada threshold baru yang dituning memakai data 2023.
