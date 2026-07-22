# AMY Market Context — Experimental Honesty Hardening

Branch: `backtest/amy-market-context-v4`

## Tujuan

Perubahan ini dibuat setelah audit 2020–2025 menunjukkan bahwa zona mentah dan DOL mentah belum cukup akurat untuk diperlakukan sebagai prediksi. Struktur M15 dan Protected Structure sengaja tidak diubah.

## Perubahan

### FVG

- FVG baru harus didukung candle displacement searah.
- Body candle minimal 1,20 kali rata-rata body 20 candle.
- Lebar gap dikunci antara 0,15–0,75 ATR M15.
- Satu close di luar zona tidak lagi langsung dianggap gagal.
- Acceptance membutuhkan dua close M15 berturut-turut di luar batas zona.

### Order Block

- Harus berasal dari candle lawan yang nyata; fallback ke candle displacement dihapus.
- Displacement minimal 2,00 kali rata-rata body 20 candle.
- Lebar OB dikunci antara 0,30–1,50 ATR M15.
- Acceptance membutuhkan dua close M15 berturut-turut di luar batas zona.

### Sweep dan DOL

- Semua sweep tetap dicatat sebagai observasi.
- DOL hanya dibuat jika arah sweep selaras dengan bias M15.
- Kondisi struktur harus valid, bukan Near Invalid atau tanpa bias.
- Jarak target maksimum 1,00 ATR saat DOL dibuat.
- Dashboard membedakan sweep mentah dengan DOL yang lolos filter.

### Validasi dan keselamatan regresi

- Protected Structure, Validated Risk, Key Liquidity, PDH/PDL, Asia Target, dan Midnight Open tidak diubah.
- Angka lama untuk Validated DOL, POI Revisit, dan Asia Entry dinonaktifkan sementara karena bergantung pada logika yang berubah.
- Marker tersebut menunggu backtest ulang dan tidak boleh membawa klaim akurasi lama.

## Regresi awal berbasis event audit 2020–2025

| Komponen | Sebelum | Setelah filter awal |
|---|---:|---:|
| FVG respect ≥0,50 ATR | 56,27% | 69,32% |
| OB respect ≥0,50 ATR | 63,08% | 69,59% |
| DOL target reached | 31,31% | sekitar 83,95% |

Catatan: angka DOL setelah filter adalah pemeriksaan awal dari event historis berdasarkan alignment dan jarak target. Hasil final harus berasal dari pemutaran ulang penuh kode eksperimen.

## Status

- File asli pada `main`: tidak berubah.
- File eksperimen pada branch backtest: sudah diperbarui.
- `amyExpV5_retestRequired`: tetap `true` sampai backtest penuh selesai.
