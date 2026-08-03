# AMY Simple ATR Bot

Indikator sederhana untuk TradingView dengan konsep:

- ATR trailing stop.
- Pergantian arah BUY/SELL saat harga menyeberangi trailing stop.
- Konfirmasi candle close secara default.
- Filter EMA opsional, default nonaktif.
- Sumber harga Close atau Heikin Ashi.
- Alert BUY dan SELL.

## Pengaturan awal XAUUSD

Gunakan terlebih dahulu:

- Sensitivity / Key Value: `1.0`
- ATR Period: `10`
- Konfirmasi Saat Candle Close: `aktif`
- Sumber Harga: `Close`
- Filter EMA: `nonaktif`
- Jarak Minimum Antar Sinyal: `0`

Pengaturan tersebut sengaja dibuat dekat dengan konsep bot ATR sederhana yang sensitif.

## Cara membaca

- Label BUY muncul ketika harga menyeberang ke atas ATR trailing stop.
- Label SELL muncul ketika harga menyeberang ke bawah ATR trailing stop.
- Garis hijau berarti arah berjalan bullish.
- Garis merah berarti arah berjalan bearish.
- Sinyal berlawanan dapat digunakan sebagai tanda keluar atau pembalikan arah, tergantung aturan trading pengguna.

## Catatan

Indikator ini tidak menjamin profit. Pada market ranging, sinyal dapat bolak-balik. Uji setiap timeframe secara terpisah dan pertimbangkan spread XAUUSD sebelum digunakan pada akun nyata.
