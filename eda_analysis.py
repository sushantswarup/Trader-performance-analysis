from __future__ import annotations

import os
from pathlib import Path


OUTPUT_DIR = Path("eda_outputs")
TRADER_CSV_PATH = Path("historical_data.csv")
SENTIMENT_CSV_PATH = Path("fear_greed_index.csv")
os.environ.setdefault("MPLCONFIGDIR", str(OUTPUT_DIR / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def save_csv(df: pd.DataFrame, name: str) -> None:
    df.to_csv(OUTPUT_DIR / name, index=False)


def save_plot(fig: plt.Figure, name: str) -> None:
    fig.tight_layout()
    fig.savefig(OUTPUT_DIR / name, dpi=180, bbox_inches="tight")
    plt.close(fig)


def load_trader_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df.attrs["source_columns"] = list(df.columns)
    df["timestamp_ist_dt"] = pd.to_datetime(
        df["Timestamp IST"], format="%d-%m-%Y %H:%M", errors="coerce"
    )
    df["date"] = df["timestamp_ist_dt"].dt.normalize()
    df["month"] = df["timestamp_ist_dt"].dt.to_period("M").astype(str)
    df["hour"] = df["timestamp_ist_dt"].dt.hour
    df["net_pnl"] = df["Closed PnL"] - df["Fee"]
    return df


def load_sentiment_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    return df[["date", "value", "classification"]].dropna(subset=["date"]).copy()


def build_summary(trader_df: pd.DataFrame, sentiment_df: pd.DataFrame) -> pd.DataFrame:
    trader_dates = trader_df["date"].dropna()
    overlap_start = max(trader_dates.min(), sentiment_df["date"].min())
    overlap_end = min(trader_dates.max(), sentiment_df["date"].max())
    summary = [
        ("trader_rows", len(trader_df)),
        ("trader_columns", len(trader_df.attrs.get("source_columns", trader_df.columns))),
        ("accounts", trader_df["Account"].nunique()),
        ("coins", trader_df["Coin"].nunique()),
        ("unique_orders", trader_df["Order ID"].nunique()),
        ("unique_transactions", trader_df["Transaction Hash"].nunique()),
        ("trader_date_start", str(trader_dates.min())),
        ("trader_date_end", str(trader_dates.max())),
        ("sentiment_rows", len(sentiment_df)),
        ("sentiment_date_start", str(sentiment_df["date"].min())),
        ("sentiment_date_end", str(sentiment_df["date"].max())),
        ("overlap_date_start", str(overlap_start)),
        ("overlap_date_end", str(overlap_end)),
        ("gross_volume_usd", round(trader_df["Size USD"].sum(), 2)),
        ("total_closed_pnl", round(trader_df["Closed PnL"].sum(), 2)),
        ("total_fees", round(trader_df["Fee"].sum(), 2)),
        ("total_net_pnl", round(trader_df["net_pnl"].sum(), 2)),
        ("buy_trades", int((trader_df["Side"] == "BUY").sum())),
        ("sell_trades", int((trader_df["Side"] == "SELL").sum())),
    ]
    return pd.DataFrame(summary, columns=["metric", "value"])


def build_trader_tables(trader_df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    account_summary = (
        trader_df.groupby("Account")
        .agg(
            trades=("Order ID", "count"),
            active_days=("date", "nunique"),
            volume_usd=("Size USD", "sum"),
            gross_pnl=("Closed PnL", "sum"),
            fees=("Fee", "sum"),
            net_pnl=("net_pnl", "sum"),
        )
        .sort_values("net_pnl", ascending=False)
        .reset_index()
    )
    account_summary["net_pnl_per_1k_volume"] = (
        account_summary["net_pnl"] / account_summary["volume_usd"] * 1000
    )

    coin_summary = (
        trader_df.groupby("Coin")
        .agg(
            trades=("Order ID", "count"),
            active_days=("date", "nunique"),
            volume_usd=("Size USD", "sum"),
            gross_pnl=("Closed PnL", "sum"),
            fees=("Fee", "sum"),
            net_pnl=("net_pnl", "sum"),
        )
        .sort_values("net_pnl", ascending=False)
        .reset_index()
    )
    coin_summary["net_pnl_per_1k_volume"] = (
        coin_summary["net_pnl"] / coin_summary["volume_usd"] * 1000
    )

    monthly_summary = (
        trader_df.groupby("month")
        .agg(
            trades=("Order ID", "count"),
            volume_usd=("Size USD", "sum"),
            gross_pnl=("Closed PnL", "sum"),
            fees=("Fee", "sum"),
            net_pnl=("net_pnl", "sum"),
        )
        .reset_index()
    )

    hourly_summary = (
        trader_df.groupby("hour")
        .agg(
            trades=("Order ID", "count"),
            volume_usd=("Size USD", "sum"),
            gross_pnl=("Closed PnL", "sum"),
            fees=("Fee", "sum"),
            net_pnl=("net_pnl", "sum"),
        )
        .reset_index()
    )

    direction_summary = (
        trader_df.groupby("Direction")
        .agg(
            trades=("Order ID", "count"),
            volume_usd=("Size USD", "sum"),
            gross_pnl=("Closed PnL", "sum"),
            fees=("Fee", "sum"),
            net_pnl=("net_pnl", "sum"),
        )
        .sort_values("trades", ascending=False)
        .reset_index()
    )

    return {
        "account_summary.csv": account_summary,
        "coin_summary.csv": coin_summary,
        "monthly_summary.csv": monthly_summary,
        "hourly_summary.csv": hourly_summary,
        "direction_summary.csv": direction_summary,
    }


def build_sentiment_tables(
    trader_df: pd.DataFrame, sentiment_df: pd.DataFrame
) -> dict[str, pd.DataFrame]:
    daily_summary = (
        trader_df.groupby("date")
        .agg(
            trades=("Order ID", "count"),
            accounts=("Account", "nunique"),
            coins=("Coin", "nunique"),
            volume_usd=("Size USD", "sum"),
            gross_pnl=("Closed PnL", "sum"),
            fees=("Fee", "sum"),
            net_pnl=("net_pnl", "sum"),
            win_rate=("Closed PnL", lambda s: (s > 0).mean()),
        )
        .reset_index()
    )

    daily_sentiment = daily_summary.merge(sentiment_df, on="date", how="left")
    daily_sentiment["sentiment_bucket"] = pd.qcut(
        daily_sentiment["value"], q=4, duplicates="drop"
    )

    regime_summary = (
        daily_sentiment.groupby("classification", dropna=False)
        .agg(
            days=("date", "count"),
            avg_trades=("trades", "mean"),
            avg_accounts=("accounts", "mean"),
            avg_coins=("coins", "mean"),
            avg_volume_usd=("volume_usd", "mean"),
            total_net_pnl=("net_pnl", "sum"),
            avg_net_pnl=("net_pnl", "mean"),
            median_net_pnl=("net_pnl", "median"),
            avg_win_rate=("win_rate", "mean"),
        )
        .sort_values("avg_net_pnl", ascending=False)
        .reset_index()
    )

    sentiment_quartile_summary = (
        daily_sentiment.groupby("sentiment_bucket", dropna=False, observed=False)
        .agg(
            days=("date", "count"),
            avg_net_pnl=("net_pnl", "mean"),
            avg_volume_usd=("volume_usd", "mean"),
            avg_win_rate=("win_rate", "mean"),
        )
        .reset_index()
    )

    account_day_summary = (
        trader_df.groupby(["date", "Account"])
        .agg(
            trades=("Order ID", "count"),
            volume_usd=("Size USD", "sum"),
            net_pnl=("net_pnl", "sum"),
        )
        .reset_index()
        .merge(sentiment_df, on="date", how="left")
    )
    account_day_sentiment_summary = (
        account_day_summary.groupby("classification", dropna=False)
        .agg(
            account_day_obs=("Account", "count"),
            profitable_share=("net_pnl", lambda s: (s > 0).mean()),
            avg_account_day_pnl=("net_pnl", "mean"),
            median_account_day_pnl=("net_pnl", "median"),
        )
        .sort_values("avg_account_day_pnl", ascending=False)
        .reset_index()
    )

    coin_day_summary = (
        trader_df.groupby(["date", "Coin"])
        .agg(
            trades=("Order ID", "count"),
            volume_usd=("Size USD", "sum"),
            net_pnl=("net_pnl", "sum"),
        )
        .reset_index()
        .merge(sentiment_df, on="date", how="left")
    )
    coin_day_sentiment_summary = (
        coin_day_summary.groupby("classification", dropna=False)
        .agg(
            coin_day_obs=("Coin", "count"),
            profitable_share=("net_pnl", lambda s: (s > 0).mean()),
            avg_coin_day_pnl=("net_pnl", "mean"),
        )
        .sort_values("avg_coin_day_pnl", ascending=False)
        .reset_index()
    )

    return {
        "daily_sentiment_summary.csv": daily_sentiment,
        "sentiment_regime_summary.csv": regime_summary,
        "sentiment_quartile_summary.csv": sentiment_quartile_summary,
        "account_day_sentiment_summary.csv": account_day_sentiment_summary,
        "coin_day_sentiment_summary.csv": coin_day_sentiment_summary,
    }


def build_plots(
    trader_df: pd.DataFrame,
    monthly_summary: pd.DataFrame,
    hourly_summary: pd.DataFrame,
    coin_summary: pd.DataFrame,
    account_summary: pd.DataFrame,
    daily_sentiment: pd.DataFrame,
    regime_summary: pd.DataFrame,
) -> None:
    sns.set_theme(style="whitegrid")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(monthly_summary["month"], monthly_summary["net_pnl"], marker="o", linewidth=2)
    ax.set_title("Monthly Net PnL")
    ax.set_xlabel("Month")
    ax.set_ylabel("Net PnL")
    ax.tick_params(axis="x", rotation=45)
    save_plot(fig, "monthly_net_pnl.png")

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.bar(monthly_summary["month"], monthly_summary["volume_usd"], color="#2a9d8f")
    ax.set_title("Monthly Traded Volume (USD)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Volume USD")
    ax.tick_params(axis="x", rotation=45)
    save_plot(fig, "monthly_volume.png")

    fig, ax = plt.subplots(figsize=(11, 5))
    sns.barplot(data=hourly_summary, x="hour", y="net_pnl", color="#e76f51", ax=ax)
    ax.set_title("Net PnL by Hour of Day (IST)")
    ax.set_xlabel("Hour")
    ax.set_ylabel("Net PnL")
    save_plot(fig, "hourly_net_pnl.png")

    top_coin_plot = coin_summary.head(12).sort_values("net_pnl")
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(
        data=top_coin_plot,
        x="net_pnl",
        y="Coin",
        hue="Coin",
        dodge=False,
        palette="viridis",
        legend=False,
        ax=ax,
    )
    ax.set_title("Top Coins by Net PnL")
    ax.set_xlabel("Net PnL")
    ax.set_ylabel("Coin")
    save_plot(fig, "top_coin_net_pnl.png")

    top_account_plot = account_summary.head(12).sort_values("net_pnl")
    fig, ax = plt.subplots(figsize=(11, 6))
    sns.barplot(
        data=top_account_plot,
        x="net_pnl",
        y="Account",
        hue="Account",
        dodge=False,
        palette="mako",
        legend=False,
        ax=ax,
    )
    ax.set_title("Top Accounts by Net PnL")
    ax.set_xlabel("Net PnL")
    ax.set_ylabel("Account")
    save_plot(fig, "top_account_net_pnl.png")

    sampled = trader_df.sample(min(len(trader_df), 15000), random_state=42).copy()
    fig, ax = plt.subplots(figsize=(9, 6))
    sns.scatterplot(
        data=sampled,
        x="Size USD",
        y="Closed PnL",
        hue="Side",
        alpha=0.45,
        s=20,
        ax=ax,
    )
    ax.set_title("Trade Size vs Closed PnL (sampled)")
    ax.set_xlabel("Trade Size USD")
    ax.set_ylabel("Closed PnL")
    ax.set_xscale("symlog")
    save_plot(fig, "trade_size_vs_pnl.png")

    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax2 = ax1.twinx()
    ax1.plot(daily_sentiment["date"], daily_sentiment["net_pnl"], color="#264653", linewidth=1.5)
    ax2.plot(daily_sentiment["date"], daily_sentiment["value"], color="#e76f51", linewidth=1.2)
    ax1.set_title("Daily Net PnL vs Fear & Greed Value")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Net PnL", color="#264653")
    ax2.set_ylabel("Fear & Greed Value", color="#e76f51")
    save_plot(fig, "sentiment_vs_daily_pnl.png")

    fig, ax = plt.subplots(figsize=(10, 5))
    regime_plot = regime_summary.dropna(subset=["classification"]).copy()
    sns.barplot(
        data=regime_plot,
        x="classification",
        y="avg_net_pnl",
        hue="classification",
        dodge=False,
        palette="crest",
        legend=False,
        ax=ax,
    )
    ax.set_title("Average Daily Net PnL by Sentiment Regime")
    ax.set_xlabel("Sentiment Regime")
    ax.set_ylabel("Average Daily Net PnL")
    ax.tick_params(axis="x", rotation=25)
    save_plot(fig, "avg_daily_pnl_by_sentiment.png")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.scatterplot(
        data=daily_sentiment.dropna(subset=["value"]),
        x="value",
        y="net_pnl",
        hue="classification",
        alpha=0.8,
        ax=ax,
    )
    ax.set_title("Sentiment Value vs Daily Net PnL")
    ax.set_xlabel("Fear & Greed Value")
    ax.set_ylabel("Daily Net PnL")
    save_plot(fig, "sentiment_value_vs_net_pnl.png")


def build_report(
    summary: pd.DataFrame,
    account_summary: pd.DataFrame,
    coin_summary: pd.DataFrame,
    monthly_summary: pd.DataFrame,
    hourly_summary: pd.DataFrame,
    direction_summary: pd.DataFrame,
    daily_sentiment: pd.DataFrame,
    regime_summary: pd.DataFrame,
    account_day_sentiment_summary: pd.DataFrame,
) -> str:
    metric = dict(summary.values)

    best_month = monthly_summary.loc[monthly_summary["net_pnl"].idxmax()]
    best_hour = hourly_summary.loc[hourly_summary["net_pnl"].idxmax()]
    best_account = account_summary.iloc[0]
    best_coin = coin_summary.iloc[0]
    best_regime = regime_summary.dropna(subset=["classification"]).iloc[0]
    worst_regime = regime_summary.dropna(subset=["classification"]).iloc[-1]
    correlation = daily_sentiment["value"].corr(daily_sentiment["net_pnl"])
    activity_correlation = daily_sentiment["value"].corr(daily_sentiment["trades"])
    best_win_regime = regime_summary.dropna(subset=["classification"]).sort_values(
        "avg_win_rate", ascending=False
    ).iloc[0]
    best_account_day_regime = account_day_sentiment_summary.dropna(
        subset=["classification"]
    ).iloc[0]

    lines = [
        "# Bitcoin Trading and Sentiment Analysis Report",
        "",
        "## Dataset Overview",
        f"- Trader rows: {int(metric['trader_rows']):,}",
        f"- Trader columns: {int(metric['trader_columns'])}",
        f"- Sentiment rows: {int(metric['sentiment_rows']):,}",
        f"- Accounts: {int(metric['accounts'])}",
        f"- Coins: {int(metric['coins'])}",
        f"- Overlap window: {metric['overlap_date_start']} to {metric['overlap_date_end']}",
        f"- Gross traded volume: ${float(metric['gross_volume_usd']):,.2f}",
        f"- Net PnL after fees: ${float(metric['total_net_pnl']):,.2f}",
        "",
        "## Core Findings",
        f"- Activity is slightly sell-heavy: {int(metric['sell_trades']):,} SELL trades vs {int(metric['buy_trades']):,} BUY trades.",
        f"- Best month overall is {best_month['month']} with ${best_month['net_pnl']:,.2f} net PnL.",
        f"- Strongest trading hour in IST is {int(best_hour['hour'])}:00 with ${best_hour['net_pnl']:,.2f} net PnL.",
        f"- Top account by net PnL is {best_account['Account']} at ${best_account['net_pnl']:,.2f}.",
        f"- Top coin by net PnL is {best_coin['Coin']} at ${best_coin['net_pnl']:,.2f}.",
        "",
        "## Sentiment Insights",
        f"- The strongest sentiment regime by average daily net PnL is {best_regime['classification']} at ${best_regime['avg_net_pnl']:,.2f} per day.",
        f"- The weakest sentiment regime by average daily net PnL is {worst_regime['classification']} at ${worst_regime['avg_net_pnl']:,.2f} per day.",
        f"- The best regime by average win rate is {best_win_regime['classification']} at {best_win_regime['avg_win_rate']:.2%}.",
        f"- The strongest account-day regime is {best_account_day_regime['classification']} at ${best_account_day_regime['avg_account_day_pnl']:,.2f} average account-day PnL.",
        f"- Fear & Greed value has a weak negative correlation with daily net PnL ({correlation:.3f}), suggesting lower sentiment tends to coincide with larger PnL days.",
        f"- Fear & Greed value also has a negative correlation with daily trade count ({activity_correlation:.3f}), meaning trader activity tends to rise when sentiment is lower.",
        "",
        "## Direction-Level Behavior",
    ]

    for _, row in direction_summary.head(6).iterrows():
        lines.append(
            f"- {row['Direction']}: {int(row['trades']):,} trades, ${row['volume_usd']:,.2f} volume, ${row['net_pnl']:,.2f} net PnL"
        )

    lines.extend(
        [
            "",
            "## Output Files",
            "- `eda_outputs/summary_metrics.csv`",
            "- `eda_outputs/account_summary.csv`",
            "- `eda_outputs/coin_summary.csv`",
            "- `eda_outputs/monthly_summary.csv`",
            "- `eda_outputs/hourly_summary.csv`",
            "- `eda_outputs/direction_summary.csv`",
            "- `eda_outputs/daily_sentiment_summary.csv`",
            "- `eda_outputs/sentiment_regime_summary.csv`",
            "- `eda_outputs/sentiment_quartile_summary.csv`",
            "- `eda_outputs/account_day_sentiment_summary.csv`",
            "- `eda_outputs/coin_day_sentiment_summary.csv`",
            "- `eda_outputs/monthly_net_pnl.png`",
            "- `eda_outputs/monthly_volume.png`",
            "- `eda_outputs/hourly_net_pnl.png`",
            "- `eda_outputs/top_coin_net_pnl.png`",
            "- `eda_outputs/top_account_net_pnl.png`",
            "- `eda_outputs/trade_size_vs_pnl.png`",
            "- `eda_outputs/sentiment_vs_daily_pnl.png`",
            "- `eda_outputs/avg_daily_pnl_by_sentiment.png`",
            "- `eda_outputs/sentiment_value_vs_net_pnl.png`",
        ]
    )

    return "\n".join(lines) + "\n"


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    (OUTPUT_DIR / ".mplconfig").mkdir(exist_ok=True)

    trader_df = load_trader_data(TRADER_CSV_PATH)
    sentiment_df = load_sentiment_data(SENTIMENT_CSV_PATH)

    summary = build_summary(trader_df, sentiment_df)
    save_csv(summary, "summary_metrics.csv")

    trader_tables = build_trader_tables(trader_df)
    sentiment_tables = build_sentiment_tables(trader_df, sentiment_df)

    for name, table in {**trader_tables, **sentiment_tables}.items():
        save_csv(table, name)

    build_plots(
        trader_df=trader_df,
        monthly_summary=trader_tables["monthly_summary.csv"],
        hourly_summary=trader_tables["hourly_summary.csv"],
        coin_summary=trader_tables["coin_summary.csv"],
        account_summary=trader_tables["account_summary.csv"],
        daily_sentiment=sentiment_tables["daily_sentiment_summary.csv"],
        regime_summary=sentiment_tables["sentiment_regime_summary.csv"],
    )

    report = build_report(
        summary=summary,
        account_summary=trader_tables["account_summary.csv"],
        coin_summary=trader_tables["coin_summary.csv"],
        monthly_summary=trader_tables["monthly_summary.csv"],
        hourly_summary=trader_tables["hourly_summary.csv"],
        direction_summary=trader_tables["direction_summary.csv"],
        daily_sentiment=sentiment_tables["daily_sentiment_summary.csv"],
        regime_summary=sentiment_tables["sentiment_regime_summary.csv"],
        account_day_sentiment_summary=sentiment_tables["account_day_sentiment_summary.csv"],
    )
    Path("EDA_REPORT.md").write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
