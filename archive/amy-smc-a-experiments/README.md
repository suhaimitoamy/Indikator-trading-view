# Amy SMC A — Archived Experiments

These files are preserved for research traceability and are **not active development baselines**.

- `Amy-SMC-A-Liquidity-Fixed.pine` — experiment that changed the raw/descriptive sweep state to continuation semantics. Useful evidence, but it blurred the separation between descriptive liquidity context and predictive sweep continuation.
- `Amy-SMC-A-Liquidity-Fixed-M5-Regime-Redesign.pine` — M5 Consensus4 regime experiment built on the Liquidity-Fixed branch. Its walk-forward result remains useful research, but it must be revalidated on the clean descriptive/predictive architecture before promotion.
- `Amy-SMC-A-Liquidity-Fixed-FinalBias-SignedGrid.pine` — Final Bias signed-weight experiment. It optimized a descriptive continuous field using a predictive directional objective and produced inverse-HTF behavior; keep as research only.

## Active lineage

1. `Amy-SMC-Z.pine` — benchmark to beat; do not tune casually.
2. `Amy-SMC-A.pine` — stable A baseline.
3. `Amy-SMC-A-LAB.pine` — the **only** active A experiment file.

Future experiments should modify `Amy-SMC-A-LAB.pine`, record results in `reports/`, and use Git commits for rollback instead of creating more root-level A variants.
