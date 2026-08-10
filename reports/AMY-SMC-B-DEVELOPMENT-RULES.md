# Amy SMC B — Official Baseline & Development Rules

## Status

`Amy-SMC-B.pine` is the official baseline to beat for all future Amy SMC experiments.

`Amy-SMC-B-LAB.pine` is the single active development file. Do not create additional `Amy-SMC-B-*.pine` experiment variants. Use Git history and reports for rollback/versioning.

Historical reference files remain frozen:

- `Amy-SMC-Z.pine` — historical benchmark/reference.
- `Amy-SMC-A.pine` — stable A reference.
- `Amy-SMC-A-LAB.pine` — final A research endpoint/reference; no new work goes here.

## Construction of B

B is built from frozen `Amy-SMC-Z.pine` plus only the M5 TGT2 segmented target/expiry module that passed clean walk-forward validation.

Retained unchanged from Z:

- HTF Swing
- Swing Structure
- Internal Structure
- raw Liquidity with original reversal semantics
- Dealing Range
- raw Pattern
- Final Bias
- Sweep Continuation predictor
- qualified CHoCH/BOS
- qualified Pattern
- M5 Round-9 entry/regime and invalidation
- M15 Next Move + Target V1 + 32-bar expiry
- H1 Next Move/confirmed-sweep override + Target V1 + 24-bar expiry

Promoted improvement:

- **M5 TGT2 segmented 2-bucket Target/expiry** only.

Explicitly excluded:

- Liquidity-Fixed experiment
- old M5 Regime Redesign experiment
- FinalBias SignedGrid experiment
- Priority #1 M5 execution-gate redesign
- Priority #3 M15 Target/expiry redesign

## Official B Next Move benchmark

Full raw ZIP replay 2004–2026, sequential Pine-logic mirror, rolling 8-year train -> next 1-year OOS test, test years 2012–2026, `<30` test signals = low confidence.

| TF | Baseline logic | OOS signals | Directional | TP win rate | Expectancy | HC windows |
|---|---|---:|---:|---:|---:|---:|
| M5 | Z Round 9 + **B TGT2** | 691 | **75.1085%** | **72.0695%** | **+0.020636R** | **15/15** |
| M15 | Z original | 7,888 | **77.9539%** | 46.6405% | -0.006004R | **15/15** |
| H1 | Z original | 2,069 | **83.5669%** | 42.1943% | -0.002766R | **15/15** |

M15/H1 retain the Z execution lifecycle because no Target/expiry redesign has yet produced positive robust OOS expectancy without changing their predictor population.

## M5 TGT2

Latest deployment parameters selected from train 2018–2025 only:

- `riskATR 3–<5`: keep a closer valid structural Target V1; otherwise cap target distance at `0.375R`; expiry `60` M5 bars.
- `riskATR >=5`: keep a closer valid structural Target V1; otherwise cap target distance at `0.35R`; expiry `192` M5 bars.

Walk-forward family sanity result:

- 691 OOS signals retained.
- Directional remains 75.1085%.
- TP improves from Z 57.7424% to 72.0695%.
- pooled expectancy improves from Z +0.008516R to +0.020636R.
- 15/15 annual windows remain high confidence.
- TP win rate improved versus Z in 15/15 OOS test years; expectancy improved in 10/15.

## Descriptive benchmark

B descriptive fields are source-identical to Z. Fresh sanity replay reproduced the same flip-to-flip scoreboard:

| Module | M5 | M15 | H1 |
|---|---:|---:|---:|
| HTF Swing | 33.5036% | 34.4518% | 34.4278% |
| Swing Structure | 42.0160% | 45.4815% | 46.8750% |
| Internal Structure | 45.9582% | 46.8264% | 51.6845% |
| Raw Liquidity | 43.2480% | 45.2880% | 45.6790% |
| Dealing Range | 49.5890% | 50.2857% | 34.3750% |
| Raw Pattern | 58.7115% | 58.5627% | 58.4163% |
| Final Bias | 36.6289% | 38.1973% | 39.4541% |

These are descriptive flip-to-flip scores and must not be compared to predictor metrics.

## B-LAB promotion rules

1. All new experiments happen only in `Amy-SMC-B-LAB.pine`.
2. Tune/select parameters only from each rolling 8-year train window.
3. Evaluate on the next 1-year OOS window using the same raw replay protocol; 2026 is Jan–Jul partial.
4. `<30` OOS events/signals = low confidence.
5. Predictor must be compared only with predictor; descriptive only with descriptive.
6. Compare a changed module against **Amy-SMC-B.pine**, not against a weaker historical baseline.
7. A change is retained only if it beats B on the same category/metric with adequate sample and cross-window robustness and does not regress already-retained modules.
8. Failed experiments are rolled back in B-LAB. Do not create another Pine experiment filename.
9. `Amy-SMC-B.pine` remains frozen until a B-LAB change passes promotion criteria.
