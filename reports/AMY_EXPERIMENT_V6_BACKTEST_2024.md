# AMY Market Context Experiment V6 — Backtest 2024

## Ruang lingkup

Pengujian hanya mengulang komponen yang sebelumnya belum lulus:

- status Failed/Acceptance FVG dan Order Block;
- DOL mentah dan Validated DOL;
- POI Revisit;
- Asia Entry.

FVG respect, Order Block respect, Protected Structure, Validated Risk, Key Liquidity, PDH/PDL, Asia Target, dan Midnight Open tidak diuji ulang.

## Perbaikan

1. **Acceptance zona**
   - acceptance membutuhkan tiga close M15 berturut-turut di luar zona;
   - close ketiga harus minimal 0,30 ATR melewati batas zona;
   - status visual diubah dari `Failed` menjadi `Accepted`.

2. **DOL**
   - target yang telah disentuh pada candle sweep atau sebelum tampil tidak boleh dihitung;
   - kandidat diuji dengan bias searah, struktur valid, target maksimum 0,75 ATR, directional close, dan close pada minimal 80% sisi tujuan candle;
   - karena hasil tetap di bawah 80%, DOL dan Validated DOL tetap dinonaktifkan. Raw sweep tetap observasi.

3. **POI Revisit**
   - dibuat mesin FVG fresh tersendiri memakai M15 yang baru selesai, tanpa keterlambatan ganda engine utama;
   - hanya FVG revisit yang dapat menjadi klaim;
   - maksimal jarak 1,25 ATR;
   - OB revisit tetap observasi.

4. **Asia Entry**
   - maksimum jarak target dipersempit dari 1,50 ATR menjadi 1,00 ATR;
   - reward:risk tetap 0,20 seperti desain lama.

## Hasil 2024

| Komponen | Event | Berhasil | Akurasi | Jan–Jun | Jul–Des | Status |
|---|---:|---:|---:|---:|---:|---|
| FVG Acceptance | 347 | 291 | **83,86%** | — | — | Lulus |
| OB Acceptance | 444 | 383 | **86,26%** | — | — | Lulus |
| Screened DOL 4H | 14 | 11 | **78,57%** | 75,00% | 83,33% | Gagal |
| Validated DOL | 0 | 0 | — | — | — | Dinonaktifkan |
| FVG POI Revisit 4H | 92 | 77 | **83,70%** | 83,72% | 83,67% | Lulus |
| Asia Entry 4H | 39 | 33 | **84,62%** | 82,35% | 86,36% | Lulus |
| OB POI Revisit 4H | 150 | 110 | **73,33%** | — | — | Gagal |

## Detail

### Acceptance

Standar audit setelah status terlihat: minimal empat dari enam close M5 berikutnya bertahan di luar zona dan harga melanjutkan minimal 0,25 ATR.

- FVG Acceptance: 83,86%.
- OB Acceptance: 86,26%.

### DOL

Pemeriksaan target untouched menghapus keberhasilan palsu yang terjadi sebelum marker dapat digunakan. Filter terbaik yang masih masuk akal hanya menghasilkan 11 keberhasilan dari 14 event atau 78,57%. Karena belum melewati 80% dan sampelnya kecil, DOL tidak boleh kembali menjadi klaim tervalidasi.

### POI Revisit

- FVG fresh dengan mesin tanpa keterlambatan ganda: 83,70%.
- Jan–Jun dan Jul–Des hampir sama, sehingga hasil relatif stabil.
- OB revisit hanya 73,33%, sehingga dinonaktifkan.

### Asia Entry

- 33 TP, 5 SL, dan 1 timeout.
- Win rate 84,62%.
- Reward:risk 0,20 tetap berarti risiko lima kali reward; akurasi tinggi tidak otomatis menghasilkan expectancy besar setelah spread dan biaya.

## Putusan

Diaktifkan:

- FVG Acceptance;
- OB Acceptance;
- FVG POI Revisit;
- Asia Entry.

Tetap dinonaktifkan:

- DOL mentah sebagai target;
- Validated DOL;
- Order Block POI Revisit.

## Batasan

Threshold dipilih dan diuji pada data 2024 yang sama. Pembagian Jan–Jun dan Jul–Des membantu mengukur kestabilan internal, tetapi hasil masih in-sample.
