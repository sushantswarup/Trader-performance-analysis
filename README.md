# Trader Performance Analysis

This project analyzes the relationship between Bitcoin market sentiment and trader performance using Hyperliquid historical trader data and the Bitcoin Fear & Greed Index.

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

## Tools and Libraries

- Python
- pandas
- numpy
- matplotlib
- seaborn
- Jupyter Notebook

## GitHub Repository

Repository link:

- https://github.com/sushantswarup/Trader-performance-analysis
