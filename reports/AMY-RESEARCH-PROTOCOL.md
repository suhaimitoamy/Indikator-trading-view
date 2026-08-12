# Amy Research Protocol

Status: **ACTIVE / SOURCE OF TRUTH untuk riset indikator & execution method**  
Tanggal ditetapkan: 2026-08-12  
Repository: `suhaimitoamy/Indikator-trading-view`

## 1. Tujuan

Amy Research Protocol adalah kerangka permanen untuk mengembangkan, menguji, membandingkan, dan mempromosikan predictor maupun execution method tanpa mencampur akurasi arah dengan kualitas eksekusi.

Tujuan utamanya bukan mencari backtest paling cantik, tetapi memastikan bahwa setiap kandidat yang dipertahankan:

1. memiliki predictive value yang bisa dibuktikan;
2. bisa dieksekusi secara realistis;
3. lolos validasi causal / no-lookahead;
4. stabil lintas tahun dan bukan hanya hasil beberapa periode kuat;
5. mempunyai parity antara research replay dan executable code;
6. cukup sederhana untuk diaudit dan dipakai live dengan risiko implementation bug yang terkendali.

---

# 2. Tiga Layer Wajib

## Layer A — Predictor

Pertanyaan: **"Apakah informasi ini benar-benar membantu membaca arah / keadaan market?"**

Contoh:
- Qualified Valid Break;
- Internal / Swing Structure;
- liquidity sweep;
- regime;
- HTF context;
- descriptive fields.

Predictor dinilai terpisah dari entry, SL, TP, fill, RR, dan account P/L.

### Metrik minimum Predictor

- source count;
- directional accuracy / structural survival;
- coverage dari source universe;
- hasil per tahun;
- stability antar regime / timeframe bila relevan;
- no future candle / no repaint / no lookahead.

**Aturan:** predictor tidak boleh dianggap gagal hanya karena execution construction tertentu gagal. Sebaliknya, execution yang profit tidak boleh dianggap membuktikan predictor jika profit itu berasal dari filter/geometry lain.

---

## Layer B — Execution

Pertanyaan: **"Kalau predictor benar, bagaimana sinyal itu dieksekusi secara realistis?"**

Execution mencakup:
- entry timing;
- entry price;
- SL geometry;
- TP geometry;
- fill semantics;
- lifecycle / timeout;
- same-bar ambiguity;
- realism floor;
- invalidation.

### Realism floor XAUUSD yang aktif

Untuk penelitian execution Amy SMC D saat ini:

- minimum absolute SL distance: **$5.00 XAUUSD**;
- minimum absolute TP distance: **$5.00 XAUUSD**;
- setup yang tidak memenuhi salah satu floor = **INVALID**, bukan trade;
- SL / TP tidak boleh dipaksa melebar hanya agar lolos floor jika itu mengubah construction yang sedang diuji.

Floor adalah constraint eksekusi, bukan predictor filter.

### Same-candle ambiguity

Jika TP dan SL sama-sama reachable pada candle yang sama dan intrabar ordering tidak diketahui:

**SL dihitung lebih dahulu.**

Ini adalah default konservatif sampai tersedia data intrabar yang benar-benar membuktikan urutan.

---

## Layer C — Validation

Pertanyaan: **"Apakah hasil yang terlihat bisa dipercaya dan bisa direproduksi live?"**

Validation adalah gate terakhir dan tidak boleh dilewati hanya karena net profit tinggi.

Wajib memeriksa:

- raw source parity;
- raw data integrity;
- no synthetic candle kecuali eksperimen khusus menyatakannya secara eksplisit;
- no future leak / lookahead;
- parameter availability pada waktu keputusan;
- exact entry/fill semantics;
- exact SL/TP semantics;
- same-bar tie-break;
- chronology;
- account compounding;
- research-to-executable parity.

---

# 3. Urutan Riset Standar

Setiap eksperimen baru mengikuti urutan berikut.

## Gate 0 — Freeze Source of Truth

Sebelum eksperimen:

- catat file baseline;
- catat blob SHA / commit baseline;
- tentukan file LAB;
- baseline produksi tidak boleh berubah selama riset kecuali ada perintah promosi eksplisit;
- source signal universe harus dibekukan sebelum tuning execution.

## Gate 1 — Source Parity

Sebelum membandingkan metode:

- jumlah source event harus match benchmark;
- distribusi tahunan harus masuk akal / match replay sebelumnya;
- perubahan source count yang tidak direncanakan = **STOP dan audit**.

Perubahan besar seperti 716 → 28 atau 878 → jumlah lain tanpa alasan mekanis yang jelas dianggap indikasi bug sampai terbukti sebaliknya.

## Gate 2 — Predictor Validation

Uji predictor tanpa mencampur entry/SL/TP.

Pertahankan:
- directional metric;
- structural cancellation boundary;
- horizon yang didefinisikan sebelum evaluasi;
- no future candle.

## Gate 3 — Execution Construction

Baru setelah predictor dipahami, uji:

- NEXT OPEN;
- retest;
- stop entry;
- local / structural SL;
- target method;
- lifecycle.

Satu eksperimen hanya boleh mengubah hal yang sedang diuji. Matched-fill / ablation digunakan bila perlu untuk mengetahui mekanisme sebenarnya.

## Gate 4 — Realism

Sebelum sebuah route dihitung sebagai trade:

- geometry harus benar;
- SL floor harus lolos;
- TP floor harus lolos;
- validity diperiksa ketika semua informasi yang dibutuhkan sudah causally known;
- tidak boleh menunggu hasil masa depan untuk menentukan apakah setup dari masa lalu sebenarnya valid.

## Gate 5 — Walk-Forward

Parameter yang dioptimasi harus dipilih dari TRAIN, bukan dari OOS penuh.

Default Amy SMC D:

- rolling **8 tahun TRAIN → 1 tahun OOS**;
- OOS tahunan;
- keputusan parameter untuk suatu tahun hanya boleh memakai data sebelum tahun tersebut;
- lifecycle TRAIN yang menyeberang batas OOS harus dikeluarkan bila berpotensi bocor.

Full-history / full-OOS sweep boleh dipakai sebagai **diagnostic curve**, tetapi tidak boleh sendirian menjadi alasan promosi parameter.

## Gate 6 — Stability

Minimum report untuk kandidat execution:

- valid trades;
- coverage dari source universe;
- TP / SL / Timeout / Collision / Invalid / No-fill bila relevan;
- WR;
- expectancy;
- net profit;
- MaxDD;
- HC;
- positive years;
- annual breakdown;
- mode/frequency parameter walk-forward bila parameter dipilih per fold.

## Gate 7 — Executable Parity

Sebelum executable dianggap siap:

- mirror kode executable ke research replay;
- source count harus match;
- valid trade count harus match;
- floor / route count harus match;
- outcome counts harus match atau selisihnya dijelaskan secara mekanis;
- net / DD / HC harus berada pada tolerance yang disepakati;
- mismatch besar = **jangan commit / jangan promote** sampai diaudit.

## Gate 8 — Promotion

Kandidat baru boleh dipromosikan jika:

- lolos semua gate di atas;
- tidak hanya unggul pada satu metrik;
- trade-off-nya diketahui;
- implementation complexity sebanding dengan manfaatnya;
- baseline lama tidak dihapus sampai kandidat baru dinyatakan stabil.

---

# 4. Metrik yang Tidak Boleh Dicampur

## Directional Accuracy

Menjawab: **apakah arah / thesis predictor bertahan?**

Tidak sama dengan WR.

## Win Rate

Menjawab: **berapa persen valid trade mencapai TP menurut lifecycle yang ditetapkan?**

Tidak sama dengan predictor accuracy.

## Coverage

`valid executable trades / source signals`

Menjawab: **berapa banyak source signal yang benar-benar bisa dipakai setelah geometry/floor/eligibility diterapkan?**

Coverage tinggi bukan berarti sistem profit; coverage rendah bisa membuat subset terlihat sangat bagus tetapi tidak robust.

## HC — High-Coverage Year

Default D-LAB:

**tahun dengan >=30 valid execution.**

HC dipakai agar strategi tidak terlihat stabil hanya karena beberapa tahun memiliki sangat sedikit trade.

## Timeout

Timeout bukan otomatis "salah arah".

Timeout berarti harga tidak menyelesaikan TP atau SL dalam horizon. Ini harus dianalisis terpisah karena bisa menunjukkan masalah:

- magnitude;
- timing;
- target terlalu jauh;
- horizon terlalu pendek;
- bukan predictor direction.

## Max Drawdown

Net profit tanpa DD tidak cukup untuk promosi.

Kandidat dengan net sedikit lebih tinggi tetapi DD jauh lebih buruk tidak otomatis lebih baik.

---

# 5. Prinsip Anti-Overfit

1. Jangan memilih parameter dari hasil OOS penuh lalu menyebutnya walk-forward.
2. Jangan memakai future touch / future no-fill untuk mengubah keputusan yang seharusnya dibuat lebih awal.
3. Jangan mengubah denominator setelah melihat outcome.
4. Jangan membuang tahun buruk tanpa alasan data-integrity yang objektif.
5. Jangan menyintesis candle kosong hanya agar replay terlihat rapi.
6. Jangan mengoptimasi terlalu banyak parameter sekaligus tanpa ablation.
7. Jangan menganggap higher WR = better system tanpa melihat coverage, DD, HC dan expectancy.
8. Jangan menganggap higher net = production-ready jika implementation complexity / causal validity buruk.

---

# 6. Prinsip Kompleksitas

**Simplicity mendapat prioritas jika performa risk-adjusted sebanding.**

Setiap branch/fallback/filter tambahan menambah:

- state complexity;
- timing ambiguity;
- parity risk;
- future-leak risk;
- live implementation risk.

Kandidat kompleks hanya layak menggantikan kandidat sederhana jika improvement-nya cukup besar dan stabil untuk membayar complexity cost tersebut.

---

# 7. Aturan Retain / Rollback

Setiap eksperimen menghasilkan salah satu status:

- **RETAIN** — terbukti memperbaiki baseline tanpa merusak gate utama;
- **RETAIN AS DIAGNOSTIC** — memberi pengetahuan mekanis tetapi tidak layak produksi;
- **ROLLBACK / REJECT** — lebih buruk, terlalu sparse, tidak causal, tidak robust, atau implementation risk tidak sebanding;
- **RE-AUDIT** — hasil menjanjikan tetapi parity / data / realism belum dapat dipercaya.

Tidak ada eksperimen yang boleh diam-diam menimpa hasil yang lebih baik.

---

# 8. Reference Implementation #1 — Amy SMC D / K1 Production Entry

## Baseline produksi yang dibekukan

`Amy-SMC-D.pine`

Frozen blob:

`d6e6d7c979dd5a852bddd9661bef0480caa2eb35`

## Research / executable host

`Amy-SMC-D-LAB.pine`

## Source predictor

K1 M15:

**Qualified Valid Break + same-direction Internal Structure**

Source logic tidak diubah oleh execution research.

## Final production entry construction

- Entry: **NEXT OPEN (+1 candle)**
- SL: **full opposite structural Swing boundary**
- TP: **1.00R**
- SL floor: **$5.00**
- TP floor: **$5.00**
- Same-candle TP/SL: **SL first**
- Toggle: `Show K1 Production Entry (1.00R)` default ON
- Alerts:
  - `K1 BUY - Production 1.00R`
  - `K1 SELL - Production 1.00R`

## Why this is the reference implementation

K1 NEXT OPEN 1.00R dipilih bukan karena memiliki win rate tertinggi, tetapi karena setelah seluruh autopsi:

- source predictor memiliki parity yang jelas;
- construction hanya satu jalur;
- tidak memakai local-SL/fallback branching;
- tidak membutuhkan future-dependent routing;
- floor dapat dicek langsung pada +1 open;
- walk-forward TP study memilih 1.00R sebagai mode TRAIN pada 12/15 fold;
- fixed 1.00R mempunyai near-full OOS coverage dan HC penuh;
- implementation risk jauh lebih rendah dibanding Hybrid Causal Repair.

### Locked OOS sanity — 2012-2026, fixed 1.00R

- source K1: **878**
- valid trades: **871**
- coverage: **99.20%**
- TP / SL / Timeout: **96 / 75 / 700**
- TP WR: **11.02%**
- Net: **+$845.61** from $10,000 standalone OOS replay
- MaxDD: **16.29%**
- HC: **15/15**
- positive years: **10/15**

### Full available-history checkpoint — 2004-2026

Full-history replay dengan modal $10,000 dan chronological compounding menghasilkan checkpoint riset:

- source: **1,342**
- valid trades: **1,291**
- coverage: **96.20%**
- Net: **+$2,702.93**
- ending equity: **$12,702.93**
- MaxDD: **16.29%**
- HC: **21/23**
- positive years: **14/23**

2004 dan 2026 adalah partial data windows pada dataset yang tersedia ketika checkpoint dibuat.

Hasil historis ini adalah reference validation, **bukan jaminan performa masa depan**.

---

# 9. Checklist Wajib Sebelum Kandidat Baru Disebut "Siap Dipakai"

- [ ] Baseline SHA dicatat dan tetap identik.
- [ ] Source universe parity lolos.
- [ ] Predictor metric terpisah dari execution metric.
- [ ] Tidak ada future leak / lookahead.
- [ ] Entry semantics eksplisit.
- [ ] SL semantics eksplisit.
- [ ] TP semantics eksplisit.
- [ ] Realism floor diterapkan sebelum eligibility final.
- [ ] Same-bar ambiguity rule eksplisit.
- [ ] Walk-forward parameter selection hanya dari TRAIN.
- [ ] Fixed/full-OOS sweep diberi label diagnostic jika memakai hindsight.
- [ ] Coverage dilaporkan.
- [ ] HC dilaporkan.
- [ ] Annual stability dilaporkan.
- [ ] Net dan MaxDD dilaporkan bersama.
- [ ] Timeout/no-fill/invalid tidak disembunyikan.
- [ ] Research replay dan executable parity lolos.
- [ ] Complexity cost dibandingkan dengan improvement.
- [ ] Kandidat lama tidak dihapus sebelum promosi eksplisit.

---

# 10. Prinsip Inti

> **Predictor, execution, dan validation adalah tiga problem berbeda. Jangan mengorbankan predictive edge hanya untuk membuat backtest terlihat bagus, dan jangan mempromosikan execution yang bagus sebelum dibuktikan causal, realistis, stabil, serta identik dengan executable.**

Amy Research Protocol harus dipakai sebagai default untuk riset berikutnya kecuali Amy secara eksplisit menetapkan metodologi eksperimen yang berbeda.