# Amy ICT Evidence Engine — Implementation Verification

Date: 2026-08-14 WITA
Target: `Amy-ICT-Evidence.pine`
Target creation commit: `08ca6b063f2b8b47a39c8b3f282e1de664afd9e0`
Target blob inspected: `25ca872b38e7bbda47bdff064922f8361a5ad484`

## Verdict

**IDENTITY VERIFICATION V1: FAIL**

Do not label the current Pine implementation as production-equivalent to the frozen BT06 / BT08-A / BT09-F research yet.

The failure is implementation identity, not a new performance result. No parameter optimization or post-result retuning was performed.

## Sources Used

- Canonical replay: `XAUUSD_REPLAY_2005_2026_REUSABLE.zip`
- BT06-B official session events
- BT08-A official XAUUSD/DXY SMT events and DXY synchronization snapshot
- BT09-F official method lock, implementation addendum, report, and 19,103-event core sheet

## Verification Results

### 1. Canonical replay / strict M5 construction — PASS

Reconstructed from the canonical observed M1 replay:

- Active M1 rows: **6,950,845** — exact match.
- Strict contiguous M5 bars: **1,295,578** — exact match.
- Strict M5 pivot highs: **279,862**.
- Strict M5 pivot lows: **280,202**.

The base observed-data and strict-M5 construction used by the Pine mirror are consistent with the frozen research population.

### 2. Session classification — PASS / exact

Compared the Pine session rules against all **119,400** BT06-B anchors.

Frozen America/New_York windows:

- Asia: 20:00–24:00
- London: 02:00–05:00
- New York: 07:00–10:00
- Off-session: all other eligible anchors

Result: **0 mismatches / 119,400**.

Observed counts:

- Asia: 16,357
- London: 16,331
- New York: 16,295
- Off-session: 70,417

Session remains context/expansion information only; it is not promoted to an independent directional signal.

### 3. Frozen Daily HTF state — PASS / exact

Reconstructed New York Daily bars from canonical M1 replay using:

- Mon–Fri calendar dates
- >=240 observed active M1 rows per eligible day
- strict 2-left / 2-right Daily pivots
- state changes only on completed Daily body-close break
- consumed swing levels not repeatedly counted

Eligible Daily bars reconstructed: **5,520**.

Compared against the official `htf_state` lineage of all **19,103** BT09-F valid retest events.

Result: **0 mismatches / 19,103**.

### 4. SMT XAUUSD opportunity engine — PASS / exact on XAU side

Reconstructed BT08-A XAUUSD M15 opportunity engine from canonical replay for 2018–2026:

- exact UTC quarter-hour M15 buckets
- strict 1-left / 1-right pivots
- pivot usable only after right bar closes
- latest active swing level
- first strict penetration retires the level

Official XAU opportunities: **42,349**.

Result after matching signal timestamp to completed M15 close:

- identity matches: **42,349 / 42,349**
- missing official opportunities: **0**
- extra opportunities: **0**
- direction mismatch: **0**
- reference swing mismatch: **0**
- source M1-count mismatch: **0**

### 5. SMT DXY historical identity — NOT BIT-VERIFIED

The frozen BT08-A research used actual Dukascopy `DOLLAR.IDX-USD` BID minute observations. The stored Drive artifact is an event-level DXY synchronization/classification snapshot; the complete raw historical DXY M1 archive is not stored with the project.

The Pine overlay uses a configurable TradingView DXY symbol (`TVC:DXY` by default). Therefore the live/chart implementation can follow the same exact-bar mechanics, but historical DXY values cannot be claimed bit-identical to the frozen Dukascopy source without the original raw source archive.

This is a source-identity limitation, not evidence that the SMT rule itself changed.

### 6. BT09-F SMR overlap handling — FAIL / material mismatch

The current Pine implementation stores only **one active setup per direction** (`bullStage` and `bearStage`). The frozen BT09-F event universe permits overlapping causal opportunities and later removes only duplicate *executable identities*.

Official BT09-F valid retest entries: **19,103**.

Same-direction official valid events whose sweep begins while another same-direction valid event is still unresolved:

- BULL: **1,018 / 9,394 = 10.84%**
- BEAR: **1,081 / 9,709 = 11.13%**
- maximum concurrent valid same-direction events observed: **4**

A direct one-active-per-direction simulation over the official valid-event intervals retains only **17,077 / 19,103 = 89.39%** and skips **2,026 = 10.61%**.

This alone proves the present Pine state machine cannot be identity-equivalent to BT09-F.

### 7. Full BT09-F replay mirror — CLOSE BUT NOT EXACT

A literal replay reconstruction using the published method lock produced:

| Funnel item | Official | Literal mirror |
|---|---:|---:|
| Active M1 | 6,950,845 | 6,950,845 |
| Strict M5 | 1,295,578 | 1,295,578 |
| Raw MSS confirmations | 34,652 | 34,907 |
| Unique confirmations | 29,431 | 29,648 |
| Valid retests | 19,103 | 19,064 |
| No-touch | 4,985 | 5,006 |
| Gap-invalid | 1,104 | 1,091 |
| Ambiguous same-minute | 828 | 829 |
| No POI | 3,411 | 3,658 |

Valid-event identity intersection in this literal mirror:

- official ∩ mirror: **18,076**
- official missing from mirror: **1,027**
- mirror extra vs official: **988**

The remaining discrepancy concentrates around the exact implementation semantics of the frozen `qualifying first sweep` / `dual sweep excluded` lineage. The official report records **58,114 qualifying first sweeps** and **3,324 dual sweeps excluded**, but the stored method text does not expose enough implementation detail to reproduce that funnel bit-for-bit from prose alone.

This unresolved lineage detail must not be guessed or retuned.

## Required Correction Before Re-verification

1. Replace single `bullStage` / `bearStage` state with an array-based multi-active setup engine.
2. Preserve each sweep's own frozen opposing-break level, HTF state, timestamps, last opposite candle, POIs, and timeout/gap state.
3. Apply BT09-F anti-pseudoreplication only when separate sweeps converge to the exact same executable SMR identity: same direction + MSS confirmation + FVG level (if any) + OB level (if any), retaining the latest causal sweep lineage.
4. Do not add Session, SMT, OTE, Premium/Discount, Killzone, AMD/PO3, or other filters to rescue identity.
5. Recover or explicitly freeze the exact `qualifying first sweep` / dual-sweep implementation before claiming full BT09-F identity.
6. Keep the DXY source-identity caveat visible for SMT historical equivalence.

## Status of Current Indicator

`Amy-ICT-Evidence.pine` remains an **implementation candidate / visual research overlay**.

Verified exact layers:

- strict canonical M5 construction
- Session classification
- frozen Daily HTF state
- XAUUSD side of BT08-A SMT opportunity logic

Not yet production-verified:

- full BT09-F SMR event identity
- historical DXY source identity inside TradingView

No profitability, SL/TP, spread, slippage, or expectancy claim is added by this verification.