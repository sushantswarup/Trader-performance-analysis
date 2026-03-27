# Bitcoin Trading and Sentiment Analysis Report

## Dataset Overview
- Trader rows: 211,224
- Trader columns: 16
- Sentiment rows: 2,644
- Accounts: 32
- Coins: 246
- Overlap window: 2023-05-01 00:00:00 to 2025-05-01 00:00:00
- Gross traded volume: $1,191,187,442.46
- Net PnL after fees: $10,051,101.22

## Core Findings
- Activity is slightly sell-heavy: 108,528 SELL trades vs 102,696 BUY trades.
- Best month overall is 2024-12 with $2,992,071.50 net PnL.
- Strongest trading hour in IST is 12:00 with $908,393.52 net PnL.
- Top account by net PnL is 0xb1231a4a2dd02f2276fa3c5e2a2f3436e6bfed23 at $2,127,387.28.
- Top coin by net PnL is @107 at $2,777,959.69.

## Sentiment Insights
- The strongest sentiment regime by average daily net PnL is Extreme Fear at $51,087.26 per day.
- The weakest sentiment regime by average daily net PnL is Greed at $10,813.63 per day.
- The best regime by average win rate is Extreme Greed at 46.74%.
- The strongest account-day regime is Fear at $5,182.06 average account-day PnL.
- Fear & Greed value has a weak negative correlation with daily net PnL (-0.079), suggesting lower sentiment tends to coincide with larger PnL days.
- Fear & Greed value also has a negative correlation with daily trade count (-0.245), meaning trader activity tends to rise when sentiment is lower.

## Direction-Level Behavior
- Open Long: 49,895 trades, $380,171,434.91 volume, $-76,852.42 net PnL
- Close Long: 48,678 trades, $382,213,248.89 volume, $3,544,366.86 net PnL
- Open Short: 39,741 trades, $185,484,862.58 volume, $-39,967.94 net PnL
- Close Short: 36,013 trades, $179,800,893.60 volume, $3,669,547.71 net PnL
- Sell: 19,902 trades, $30,108,794.11 volume, $2,900,573.63 net PnL
- Buy: 16,716 trades, $31,196,797.04 volume, $-3,764.98 net PnL

## Output Files
- `eda_outputs/summary_metrics.csv`
- `eda_outputs/account_summary.csv`
- `eda_outputs/coin_summary.csv`
- `eda_outputs/monthly_summary.csv`
- `eda_outputs/hourly_summary.csv`
- `eda_outputs/direction_summary.csv`
- `eda_outputs/daily_sentiment_summary.csv`
- `eda_outputs/sentiment_regime_summary.csv`
- `eda_outputs/sentiment_quartile_summary.csv`
- `eda_outputs/account_day_sentiment_summary.csv`
- `eda_outputs/coin_day_sentiment_summary.csv`
- `eda_outputs/monthly_net_pnl.png`
- `eda_outputs/monthly_volume.png`
- `eda_outputs/hourly_net_pnl.png`
- `eda_outputs/top_coin_net_pnl.png`
- `eda_outputs/top_account_net_pnl.png`
- `eda_outputs/trade_size_vs_pnl.png`
- `eda_outputs/sentiment_vs_daily_pnl.png`
- `eda_outputs/avg_daily_pnl_by_sentiment.png`
- `eda_outputs/sentiment_value_vs_net_pnl.png`
