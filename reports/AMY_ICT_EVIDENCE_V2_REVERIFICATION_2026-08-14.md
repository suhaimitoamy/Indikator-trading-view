# Amy ICT Evidence V2 — Replay Re-verification

Date: 2026-08-14 WITA
Target: `Amy-ICT-Evidence-V2.pine`
Target commit: `c106efa56ff46da8e21bf4c251115cb0dbea9599`
Target blob inspected after commit: `386e80e43388cfc7f5fc804d4cb41ddac11a376c`

## Verdict

**RESEARCH-LOGIC REPLAY IDENTITY: PASS**

The V2 logic mirror reproduces the frozen BT09-F event universe exactly on the canonical XAUUSD replay when the published rules are implemented with the recovered execution semantics below.

This is an implementation-logic verification against the canonical replay, not a TradingView cloud/compiler execution test. The Pine source still needs to be opened/saved in TradingView before claiming editor/runtime compatibility.

## What Changed From V1

V1 failed identity verification because it stored only one active SMR setup per direction. Official BT09-F permits concurrent causal sweep lineages and removes duplicates only when they converge to the same executable SMR identity.

V2 therefore:

1. stores concurrent SMR lineages in `array<SmrSetup>`;
2. freezes each lineage's sweep time, opposing break level, HTF state, last opposite candle, MSS, FVG and OB state independently;
3. applies anti-pseudoreplication at executable identity, keeping the latest causal sweep lineage;
4. uses first valid M1 retest after MSS;
5. keeps Session and SMT separate from BT09-F entry gating.

## Recovered Sweep Semantics

The exact `qualifying first sweep` count is reproduced when:

- high reclaim = active latest high is strictly penetrated and candle closes back below it;
- low reclaim = active latest low is strictly penetrated and candle closes back above it;
- if both active high and active low reclaim on the same M5 bar, the bar is ambiguous and excluded;
- an excluded dual bar does **not** retire either referenced level;
- a non-dual sweep retires its referenced level only when that side is qualifying under the frozen LTF state.

Result: **58,114 qualifying first sweeps — exact official match.**

## Recovered Chronology Semantics

The full replay identity matches only when the >15 minute observed-data gap rule is applied to the post-MSS retest/path chronology, not as a hard blocker during the sweep-to-MSS search.

The sweep-to-MSS search remains a maximum four wall-clock hours across strict observed M5 candidates.

## ATR Floating Arithmetic

The final one-event discrepancy was traced to floating arithmetic at exact 0.80 ATR boundary cases.

Using a direct rolling mean of the prior 14 completed strict-M5 True Range values reproduces the official result exactly. This is the intended simple mean definition and corresponds to V2 maintaining the 14 TR values and evaluating `array.avg(tr14)` before appending the current bar's TR.

No threshold was changed. `0.80` remains frozen.

## Exact BT09-F Funnel Reproduction

| Funnel item | Official | V2 logic mirror |
|---|---:|---:|
| Active M1 rows | 6,950,845 | 6,950,845 |
| Strict M5 bars | 1,295,578 | 1,295,578 |
| Qualifying first sweeps | 58,114 | 58,114 |
| Raw MSS confirmations | 34,652 | 34,652 |
| Identity duplicates removed | 5,221 | 5,221 |
| Unique SMR confirmations | 29,431 | 29,431 |
| Valid retest entries | 19,103 | 19,103 |
| No-touch 4H | 4,985 | 4,985 |
| Gap-invalid retest | 1,104 | 1,104 |
| Ambiguous same-minute | 828 | 828 |
| No POI | 3,411 | 3,411 |

### Valid-event identity

- official valid events: **19,103**
- V2 mirror valid events: **19,103**
- intersection: **19,103**
- official missing from mirror: **0**
- mirror extra vs official: **0**

**Identity = 100%.**

## Previously Verified Layers Retained

### Session / BT06-B

- 119,400 official anchors compared.
- **0 mismatches**.

### Daily HTF / BT09-F lineage

- 5,520 eligible New York Daily bars reconstructed.
- Compared against all 19,103 official BT09-F valid events.
- **0 HTF-state mismatches**.

### SMT XAUUSD opportunity engine / BT08-A

- 42,349 official XAUUSD M15 opportunities.
- **42,349 / 42,349 exact XAU-side identities**.
- 0 missing, 0 extra, 0 direction mismatch, 0 reference-level mismatch.

## Remaining DXY Source Caveat

BT08-A historical research used actual Dukascopy `DOLLAR.IDX-USD` BID minute observations. The complete raw DXY M1 archive was not retained with the project; only the event-level synchronization/classification snapshot is stored.

V2 uses a configurable TradingView DXY symbol (`TVC:DXY` by default). The rule mechanics are preserved, but TradingView's historical feed cannot be claimed bit-identical to the frozen Dukascopy feed without the original raw source archive.

Therefore:

- XAU-side SMT mechanics: verified exact.
- frozen historical DXY source identity inside TradingView: not claimable.

## Production Status

`Amy-ICT-Evidence-V2.pine` is now the preferred research-faithful candidate over V1.

Research-logic replay identity for the XAUUSD BT09-F SMR engine: **PASS, 100% event identity**.

Still required before calling the Pine file production-ready:

1. TradingView Pine Editor compile/save test;
2. chart runtime smoke test on standard XAUUSD M5;
3. verify the chosen live DXY symbol behaves as intended;
4. do not add new filters or optimize parameters during implementation verification.

No profitability, SL/TP, cost, spread, slippage, sizing, or expectancy claim is introduced by this verification.