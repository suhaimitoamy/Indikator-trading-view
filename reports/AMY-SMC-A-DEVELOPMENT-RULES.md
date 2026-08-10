# Amy SMC A Development Rules

Goal: make Amy SMC A demonstrably better than Amy SMC Z without mixing descriptive and predictive metrics.

## File roles

- `Amy-SMC-Z.pine`: frozen benchmark/reference.
- `Amy-SMC-A.pine`: stable retained A baseline.
- `Amy-SMC-A-LAB.pine`: single active development file.
- `archive/amy-smc-a-experiments/`: old experimental branches preserved only for research.

## Two independent scoreboards

### PREDICTIVE
Evaluate only forward-looking modules against the Z predictive benchmark: qualified Pattern/BOS/CHoCH/Sweep, Next Move, regime gating, Target/TP, directional accuracy, expectancy, and execution lifecycle.

### DESCRIPTIVE
Evaluate context/state modules on their descriptive job, not by forcing them to behave like Next Move: HTF/Swing/Internal structure, raw Liquidity context, Dealing Range, raw Pattern, Event History, Final Bias/context summary, zones/levels.

## Promotion rule

A LAB change is promoted only when:
1. selection/tuning uses train data only;
2. the same walk-forward protocol is used for A and Z;
3. `<30` events/signals in a test window is low-confidence;
4. it beats Z on the **same module category and metric** with adequate sample and cross-window consistency;
5. it does not regress already-retained modules outside the intended scope.

If a change fails, rollback the LAB commit. Do not create another A filename.

## Current research notes

- The continuation interpretation of sweep is strong as a **predictive cue**, but this does not justify overwriting the raw descriptive sweep state.
- The Consensus4 M5 result is worth retesting on the clean architecture because its prior test was built on the Liquidity-Fixed experiment.
- The signed-grid Final Bias result is not production-ready; its inverse-HTF behavior indicates a semantic/objective mismatch that needs a separate audit.
