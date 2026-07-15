# AMY Predictive QRR — Sweep/Reclaim Monthly Walk-Forward Backtest

## Scope
- Instrument: XAUUSD
- Timeframe: M5
- Data: January 2022 through June 2026
- Candles: 311,817
- Initial capital: $2,000
- Risk: 1% of current balance per closed trade
- Maximum SL: 150 pips, with 1 pip = 0.10 price
- Spread, commission, swap, and slippage: excluded

## Corrected entry logic
1. A confirmed swing or previous-day level creates a pending zone.
2. Price must sweep through the outside of the zone and close back across it.
3. BUY requires a bullish rejection candle; SELL requires a bearish rejection candle.
4. The next confirmation candle must close beyond the rejection candle high/low.
5. Entry is made at that confirmation candle close, not at an intrabar stop trigger.
6. If the planned SL is touched before confirmation, the setup is cancelled because no entry occurred.
7. A zone can produce only one setup.
8. Only one trade can be active at a time.
9. The entry candle cannot hit TP or SL. On later candles touching both, SL is counted first.
10. Trades still open after 288 M5 bars are neutral timeouts.

## Monthly correction process
- Every month is first tested using the code inherited from the previous month.
- A profitable month keeps the code unchanged.
- A non-profitable month may change only one logic/ATR field for the following month.
- The candidate change is checked on the full month and on both halves of that month.
- The current month’s optimized result is diagnostic only; the valid walk-forward result is the inherited-code result.

## Valid sequential results

| RR | Wins | Losses | WR | Net R | Final balance | Month-end max DD | Positive months | Code changes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1:1 | 1,396 | 1,353 | 50.78% | +43R | $2,679.70 | 53.34% | 33/54 | 21 |
| 1:2 | 986 | 1,893 | 34.25% | +79R | $3,297.79 | 42.29% | 26/54 | 28 |
| 1:3 | 643 | 1,817 | 26.14% | +112R | $4,212.25 | 38.35% | 25/54 | 29 |

## July 2026 profiles

| RR | Sources | Confirm bars | ATR | Pivot | Zone ATR | Sweep ATR | Reclaim ATR | SL buffer ATR | Body ATR | Close location | Expiry |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1:1 | Swing + PDH/PDL | 1 | 21 | 5 | 0.30 | 0.00 | 0.00 | 0.20 | 0.05 | 0.60 | 24 |
| 1:2 | Swing + PDH/PDL | 1 | 7 | 7 | 0.40 | 0.20 | 0.00 | 0.25 | 0.05 | 0.55 | 24 |
| 1:3 | Swing + PDH/PDL | 1 | 14 | 7 | 0.40 | 0.05 | 0.10 | 0.10 | 0.15 | 0.55 | 144 |

## Interpretation
- RR 1:1 became profitable, but its edge remains thin and can be heavily affected by trading costs.
- RR 1:2 produced a stronger return than 1:1 with a similar number of trades.
- RR 1:3 produced the highest final balance and net R in this test, while its 26.14% WR is only modestly above the 25% break-even rate.
- The reported drawdown is based on chained month-end balances. Continuous intramonth drawdown may be higher.
- The Pine script was statically reviewed but not compiled inside TradingView.