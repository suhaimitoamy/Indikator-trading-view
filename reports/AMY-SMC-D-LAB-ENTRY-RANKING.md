# Amy SMC D-LAB — Entry Ranking Report

Last updated: 2026-08-11
Repository: `suhaimitoamy/Indikator-trading-view`
Branch: `main`

## Scope lock

This report is for **Amy SMC D-LAB entry-method research only**.

- Focus: entry methods, TP/SL outcome, win rate, profit/loss, drawdown, OOS robustness.
- Do **not** restart directional/predictive accuracy research here. That phase was completed earlier in the Amy SMC C baseline research.
- Amy SMC D production baseline remains frozen and is not modified by this report.
- Existing K1-K6 and Pullback research remain preserved.
- K7-K21 are the later entry-method exploration / walk-forward research set.

## Reporting standard going forward

Use these account assumptions for human-readable reporting:

- Starting balance: **$10,000**
- Position risk: **1% of current balance per entry**
- Risk model: **compound / dynamic balance**
- Primary displayed metrics: Entry count, Win Rate / TP Hit Rate, Ending Balance, Net Profit, Max Drawdown, OOS robustness.
- Do not use R as the main user-facing unit. Convert research results into dollars when enough information exists.

### Important compounding caveat

The historical K1-K21 reports store aggregate execution counts and average expectancy, but do not preserve the complete chronological WIN/LOSS sequence for every candidate. Therefore the balances below are **mathematical compounding projections from aggregate expectancy**, not a trade-by-trade account-equity replay.

For future backtests, calculate compounding chronologically from each individual trade so Ending Balance and Max Drawdown are exact.

## Current K1-K21 ranking — OOS entry research

| Rank | K | Method | TF | OOS Entries | WR / TP Hit | Projected Ending Balance | Projected Net Profit | Research Status |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | **K7** | Donchian Trend Breakout | M15 | 18,061 | 64.18% | **$211,587** | **+$201,587** | Robust |
| 2 | **K20** | Asia Range Breakout + H1 | M15 | 2,376 | 55.64% | **$29,682** | **+$19,682** | Robust — strongest quality candidate |
| 3 | **K6** | QCH Retest | M5 | 358 | 60.89% | **$12,259** | **+$2,259** | Positive |
| 4 | **K1** | QVB + Internal Structure | M15 | 878 | 39.98% | **$11,368** | **+$1,368** | Primary legacy candidate |
| 5 | **K2** | QCH + Internal Structure | M15 | 319 | 42.01% | **$10,840** | **+$840** | Secondary legacy candidate |
| 6 | **K8** | Sweep-Reclaim Trend | M15 | 166 | **72.89%** | **$10,768** | **+$768** | Positive, low sample / low HC |
| 7 | **K4** | Pattern + Dealing Range + Internal | M5 | 63 | 66.67% | **$10,295** | **+$295** | Exploratory |
| 8 | **K5** | QVB Retest | M15 | 434 | 43.09% | **$10,092** | **+$92** | Very thin edge |
| 9 | K3 | Sweep Continuation + Dealing Range | M5 | 555 | 53.51% | $9,857 | -$143 | Not preferred |
| 10 | K16 | FVG Displacement Trend | M15 | 12,034 | 66.31% | $9,082 | -$918 | Proven overfit |
| 11 | K21 | Volatility-Contraction Breakout | H1 | 334 | 68.26% | $8,624 | -$1,376 | Rejected main target / low HC |
| 12 | K10 | EMA Cross + ADX | M15 | 1,958 | 69.51% | $6,934 | -$3,066 | Rejected |
| 13 | K11 | Bollinger Squeeze Breakout | M15 | 5,520 | 69.51% | $2,290 | -$7,710 | Rejected |
| 14 | K19 | EMA Pullback + H1 ADX | M15 | 4,358 | 65.33% | $2,137 | -$7,863 | Rejected |
| 15 | K18 | M5 Sweep + H1 Volatility | M5 | 7,778 | 67.85% | $239 | -$9,761 | Rejected |
| 16 | K17 | M5 Breakout + H1 Trend | M5 | 47,237 | 67.64% | $228 | -$9,772 | Rejected |
| 17 | K13 | Inside-Bar Breakout + HTF | M5 | 15,510 | 68.57% | $33 | -$9,967 | Rejected |
| 18 | K15 | Pinbar Trend + HTF | M15 | 7,523 | 62.38% | <$1 | ≈-$9,999 | Rejected |
| 19 | K14 | Engulfing Trend | M15 | 15,420 | 66.12% | <$1 | ≈-$10,000 | Rejected |
| 20 | K9 | EMA Pullback + HTF Trend | M15 | 44,673 | 67.18% | ≈$0 | ≈-$10,000 | Rejected |
| 21 | K12 | Narrow-Range Breakout + HTF | M5 | 37,334 | 66.83% | ≈$0 | ≈-$10,000 | Rejected |

## Interpretation lock

- **K20** remains the strongest new candidate by quality / robustness from the K7-K21 walk-forward research.
- **K7** produces the highest projected total profit mainly because its OOS execution count is extremely large; its edge per entry is much thinner than K20.
- **K8** has the highest TP hit rate among the positive new candidates, but the OOS sample is too sparse for production promotion.
- High TP hit rate alone is not enough. Several rejected candidates have approximately 65-70% TP hit rates but negative aggregate expectancy because their loss geometry overwhelms the smaller winning payoff.
- K1-K6 remain preserved. This report does not overwrite their original research definitions.

## Future backtest output format

For every new entry-method candidate, report at minimum:

1. Candidate name / K number
2. Timeframe
3. Number of executions
4. Wins
5. Losses
6. Win Rate / TP Hit Rate
7. Starting Balance = $10,000
8. Risk = 1% of current balance per entry
9. Ending Balance
10. Net Profit / Loss in dollars
11. Max Drawdown in dollars and percent
12. OOS / walk-forward robustness
13. Final status: PROMOTE / WATCH / REJECT / OVERFIT

Directional accuracy is **not** part of the primary D-LAB entry-method scorecard.