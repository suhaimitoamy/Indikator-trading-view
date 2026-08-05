# AMY Adaptive Regime Compass 2019–2026

## Tujuan

Indikator ini adalah **pembaca arah dan kondisi market**, bukan strategy dan bukan sistem entry otomatis.

Output utamanya:

- arah resmi: **BULLISH / BEARISH / TUNGGU**;
- kondisi: continuation, pullback, expansion, range, kandidat reversal, atau transition;
- konteks D1–H4–H1–M15/M5;
- level struktur yang membatalkan arah resmi;
- label Buy/Sell hanya ketika arah resmi benar-benar berubah.

## Dataset

Seluruh arsip candle XAUUSD yang tersedia telah dibaca dari Januari 2019 sampai 31 Juli 2026.

| Timeframe | Bar |
|---|---:|
| M5 | 548.000 |
| M15 | 182.680 |
| H1 | 45.690 |
| H4 | 12.421 |
| D1 | 2.389 |

Pembagian pengembangan:

- **2019–2023:** mempelajari perilaku trend, range, pullback, ekspansi volatilitas, dan reversal;
- **2024:** validasi aturan awal;
- **2025:** stress test pada trend besar dan ekspansi harga;
- **2026 Januari–Juli:** pemeriksaan out-of-sample pada volatilitas dan sumber data berbeda.

Data 2026 belum merupakan satu tahun penuh.

## Temuan utama per kondisi market

### Trend kuat

Periode 2019–2020 dan terutama 2024–2025 menunjukkan bahwa koreksi lokal berulang kali terjadi tanpa mengubah arah besar. Karena itu, indikator tidak lagi membalik arah hanya karena momentum lokal atau EMA cepat berubah.

Arah resmi dipertahankan selama struktur dan konteks H1/H4 belum terinvalidasi. Koreksi ditampilkan sebagai **BULLISH PULLBACK** atau **BEARISH PULLBACK**.

### Range dan rotasi

Periode 2021–2023 menunjukkan banyak persilangan, breakout pendek, dan perubahan momentum yang gagal berlanjut. Label berdasarkan ambang skor mentah menghasilkan puluhan ribu perubahan dan secara diagnostik mendekati acak.

Karena itu, kondisi range memerlukan:

- efisiensi pergerakan rendah;
- ADX rendah;
- konteks lokal dan timeframe penghubung sama-sama lemah;
- output **TUNGGU**, bukan Buy/Sell berulang.

### Volatility expansion

Volatilitas absolut XAUUSD berubah sangat besar dari 2019 sampai 2026. Semua jarak utama dinormalisasi terhadap ATR. Expansion hanya diakui ketika:

- ATR meningkat dibanding baseline 100 bar;
- true range lebih besar dari ATR normal;
- body candle cukup dominan;
- arah candle sesuai dorongan struktur.

### Reversal

Reversal tidak lagi ditentukan oleh satu crossover. Perubahan arah resmi membutuhkan kombinasi:

- sweep pada swing sebelumnya;
- market structure shift atau break struktur yang kuat;
- candle sudah close;
- H1 mulai mendukung;
- H4 tidak lagi kuat melawan;
- konfirmasi berurutan dan minimum hold time agar arah tidak berkedip.

## State machine

Alur arah resmi:

```text
TUNGGU
  ├─> BULLISH
  │     ├─> BULLISH CONTINUATION
  │     ├─> BULLISH EXPANSION
  │     └─> BULLISH PULLBACK
  │            └─> tetap bullish sampai invalidasi/reversal terkonfirmasi
  └─> BEARISH
        ├─> BEARISH CONTINUATION
        ├─> BEARISH EXPANSION
        └─> BEARISH PULLBACK
               └─> tetap bearish sampai invalidasi/reversal terkonfirmasi
```

Saat belum ada arah resmi, indikator dapat menunjukkan:

- RANGE / SIDEWAYS;
- TRANSISI;
- KANDIDAT BULLISH;
- KANDIDAT BEARISH.

## Hierarki timeframe

### Chart M5

Bobot konteks:

- M15: 15%;
- H1: 35%;
- H4: 35%;
- D1: 15%.

M5 membutuhkan dua candle konfirmasi dan minimum hold 12 bar, setara sekitar satu jam.

### Chart M15

Bobot konteks:

- H1: 45%;
- H4: 40%;
- D1: 15%.

M15 membutuhkan satu candle close dan minimum hold empat bar, juga sekitar satu jam.

Indikator sengaja dibatasi untuk M5 dan M15 karena dua timeframe tersebut yang dianalisis dan divalidasi secara langsung pada dataset.

## Buy dan Sell di chart

Label **Buy** dan **Sell** bukan order atau rekomendasi entry.

- Buy muncul ketika arah resmi berubah menjadi bullish.
- Sell muncul ketika arah resmi berubah menjadi bearish.
- Pullback tidak menghasilkan label berlawanan.
- Range, transition, dan konflik H1/H4 tidak menghasilkan label.
- Semua label memakai candle yang sudah close dan tetap terlihat sebagai riwayat arah.

## Anti-repaint

- keputusan lokal memakai candle chart yang sudah close;
- data M15, H1, H4, dan D1 memakai candle HTF sebelumnya yang sudah selesai;
- `lookahead_on` hanya digunakan bersama offset satu candle HTF;
- state dan label diperbarui hanya saat `barstate.isconfirmed`.

## Yang sengaja dihapus

Versi state-machine tidak memiliki:

- `strategy()`;
- simulasi order;
- entry otomatis;
- Stop Loss atau Take Profit;
- profit factor;
- target harga buatan;
- skor Memory Edge yang sulit diterjemahkan;
- label Buy/Sell dari perubahan skor mentah.

## Batasan yang jujur

Data historis tidak dapat menjamin arah masa depan. Pengujian menunjukkan bahwa memaksa prediksi pada setiap perubahan kecil menghasilkan akurasi yang mendekati acak. Oleh sebab itu, indikator ini memprioritaskan:

1. pembacaan kondisi market saat ini;
2. kestabilan arah resmi;
3. pemisahan pullback dari reversal;
4. memilih TUNGGU ketika konteks belum cukup.

Data baru belum diperlukan untuk merancang ulang logika ini. Data setelah Juli 2026 sebaiknya digunakan sebagai forward validation, bukan untuk terus menyesuaikan aturan agar cocok dengan masa lalu.
