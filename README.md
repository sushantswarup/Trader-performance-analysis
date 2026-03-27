# Trader Performance Analysis

This project analyzes the relationship between Bitcoin market sentiment and trader performance using Hyperliquid historical trader data and the Bitcoin Fear & Greed Index.

It focuses on how trader behavior changes across fear and greed regimes and whether sentiment can help explain variation in activity, profitability, and win rate.

## Repository Overview

This project was built as an exploratory data analysis case study using:

- a Bitcoin market sentiment dataset
- Hyperliquid historical trader execution data
- a Jupyter notebook for interactive analysis
- a Python script for reproducible output generation

The final output includes merged daily sentiment-performance tables, charts, and a notebook that explains the findings step by step.

## Project Objective

The goal is to explore how trader activity, profitability, and win behavior change across different market sentiment regimes such as:

- Extreme Fear
- Fear
- Neutral
- Greed
- Extreme Greed

This analysis is designed to uncover patterns that can help inform smarter trading strategies.

## Datasets Used

### 1. Bitcoin Market Sentiment Dataset

File: `fear_greed_index.csv`

Main columns:

- `date`
- `value`
- `classification`

### 2. Historical Trader Data from Hyperliquid

File: `historical_data.csv`

Main columns:

- `Account`
- `Coin`
- `Execution Price`
- `Size Tokens`
- `Size USD`
- `Side`
- `Timestamp IST`
- `Start Position`
- `Direction`
- `Closed PnL`
- `Fee`

## Project Files

- `Bitcoin_Trading_EDA.ipynb`: Main notebook with full step-by-step analysis
- `eda_analysis.py`: Script version of the analysis
- `EDA_REPORT.md`: Short written summary of findings
- `eda_outputs/`: Exported CSV summaries and PNG charts

## Exported Outputs

The `eda_outputs/` folder contains generated analysis files such as:

- daily sentiment summary tables
- sentiment regime summary tables
- account-day and coin-day analysis tables
- monthly and hourly performance charts
- sentiment vs PnL visualizations

Some key generated files:

- `eda_outputs/sentiment_regime_summary.csv`
- `eda_outputs/account_day_sentiment_summary.csv`
- `eda_outputs/coin_day_sentiment_summary.csv`
- `eda_outputs/sentiment_vs_daily_pnl.png`
- `eda_outputs/avg_daily_pnl_by_sentiment.png`
- `eda_outputs/sentiment_value_vs_net_pnl.png`

## Key Analysis Performed

- Data cleaning and timestamp parsing
- Daily aggregation of trade activity
- Merge between trader data and sentiment data by date
- Sentiment regime analysis
- Sentiment quartile analysis
- Correlation analysis
- Account-day and coin-day performance analysis
- Visual analysis for PnL, sentiment, and behavior patterns

## Main Findings

- Lower sentiment periods were associated with higher trading activity.
- Extreme Fear showed the highest average daily net PnL.
- Extreme Greed showed the strongest average win rate.
- Sentiment value had a weak negative relationship with daily net PnL and trade count.
- Traders appeared to be more active when market sentiment was weaker.

## Key Results

- `Extreme Fear` delivered the highest average daily net PnL.
- `Extreme Greed` produced the best average win rate.
- Daily sentiment value showed a weak negative correlation with net PnL.
- Daily sentiment value also showed a negative relationship with trade count.
- Lower sentiment regimes were associated with higher participation and larger opportunity days.

## Strategy Insight

One useful interpretation from this project is that market sentiment can be treated as a context variable rather than just a descriptive signal.

- In fear-driven conditions, traders appear more active and daily PnL opportunities become larger.
- In greed-driven conditions, activity is lower, but trade win rate can improve.
- This suggests position sizing, participation rate, and strategy aggressiveness may be adjusted by sentiment regime.

## Notebook Walkthrough

The notebook is organized into a simple step-by-step flow:

1. import libraries
2. load the two datasets
3. clean timestamp and date columns
4. create summary metrics
5. build daily trader-level summaries
6. merge daily trader performance with sentiment
7. analyze by sentiment regime and quartile
8. compute correlations
9. compare account-day and coin-day behavior
10. visualize the results

## Visual Highlights

The notebook and exported charts include:

- daily net PnL trend
- fear and greed value trend
- average daily net PnL by sentiment regime
- sentiment value vs daily net PnL scatter plot
- average account-day PnL by sentiment
- average win rate by sentiment

## How To Run

### Option 1: Open the Notebook

Open:

- `Bitcoin_Trading_EDA.ipynb`

Run the cells from top to bottom using a Python 3 / Anaconda kernel.

### Option 2: Run the Python Script

```bash
python3 eda_analysis.py
```

This refreshes:

- `EDA_REPORT.md`
- files inside `eda_outputs/`

## Suggested Environment

Use a Python 3 environment with these libraries installed:

- pandas
- numpy
- matplotlib
- seaborn
- jupyter

## Tools and Libraries

- Python
- pandas
- numpy
- matplotlib
- seaborn
- Jupyter Notebook

## Future Improvements

- add statistical significance testing for regime differences
- compare spot, long, and short behavior separately
- add rolling-window sentiment analysis
- build a simple rule-based trading framework using sentiment filters
- add dashboard-style visuals for easier presentation

## GitHub Repository

Repository link:

- https://github.com/sushantswarup/Trader-performance-analysis
