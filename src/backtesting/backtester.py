import numpy as np
import pandas as pd

from src.utils.config import CONFIG


class Backtester:
    """
    Backtest selected monthly portfolios against the Ibovespa benchmark.
    """

    def __init__(self) -> None:
        self.initial_capital = CONFIG.initial_capital
        self.risk_free_rate = CONFIG.risk_free_rate

    def run_backtest(
        self,
        selected_portfolio: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate monthly portfolio returns from selected assets.
        """
        portfolio = selected_portfolio.copy()
        portfolio["date"] = pd.to_datetime(portfolio["date"])

        portfolio["weighted_return"] = (
            portfolio["future_stock_return"] * portfolio["portfolio_weight"]
        )

        monthly_returns = (
            portfolio.groupby("date")
            .agg(
                portfolio_return=("weighted_return", "sum"),
                benchmark_return=("future_benchmark_return", "first"),
                num_assets=("ticker", "nunique"),
            )
            .reset_index()
            .sort_values("date")
        )

        monthly_returns["portfolio_cumulative_return"] = (
            1.0 + monthly_returns["portfolio_return"]
        ).cumprod() * self.initial_capital

        monthly_returns["benchmark_cumulative_return"] = (
            1.0 + monthly_returns["benchmark_return"]
        ).cumprod() * self.initial_capital

        monthly_returns["excess_return"] = (
            monthly_returns["portfolio_return"] - monthly_returns["benchmark_return"]
        )

        monthly_returns["beat_benchmark"] = monthly_returns["excess_return"] > 0

        return monthly_returns

    def calculate_performance_metrics(
        self,
        backtest_result: pd.DataFrame,
    ) -> dict[str, float]:
        """
        Calculate portfolio performance metrics.
        """
        result = backtest_result.copy()

        portfolio_returns = result["portfolio_return"]
        benchmark_returns = result["benchmark_return"]

        portfolio_total_return = (
            result["portfolio_cumulative_return"].iloc[-1] / self.initial_capital - 1.0
        )

        benchmark_total_return = (
            result["benchmark_cumulative_return"].iloc[-1] / self.initial_capital - 1.0
        )

        portfolio_volatility = portfolio_returns.std() * np.sqrt(12)

        benchmark_volatility = benchmark_returns.std() * np.sqrt(12)

        portfolio_sharpe = self._calculate_sharpe_ratio(
            returns=portfolio_returns,
        )

        benchmark_sharpe = self._calculate_sharpe_ratio(
            returns=benchmark_returns,
        )

        portfolio_max_drawdown = self._calculate_max_drawdown(
            cumulative_returns=result["portfolio_cumulative_return"],
        )

        benchmark_max_drawdown = self._calculate_max_drawdown(
            cumulative_returns=result["benchmark_cumulative_return"],
        )

        hit_rate = result["beat_benchmark"].mean()

        return {
            "portfolio_total_return": portfolio_total_return,
            "benchmark_total_return": benchmark_total_return,
            "portfolio_volatility": portfolio_volatility,
            "benchmark_volatility": benchmark_volatility,
            "portfolio_sharpe": portfolio_sharpe,
            "benchmark_sharpe": benchmark_sharpe,
            "portfolio_max_drawdown": portfolio_max_drawdown,
            "benchmark_max_drawdown": benchmark_max_drawdown,
            "hit_rate": hit_rate,
        }

    def _calculate_sharpe_ratio(
        self,
        returns: pd.Series,
    ) -> float:
        """
        Calculate annualized Sharpe ratio using monthly returns.
        """
        excess_returns = returns - (self.risk_free_rate / 12)

        if excess_returns.std() == 0:
            return 0.0

        return excess_returns.mean() / excess_returns.std() * np.sqrt(12)

    def _calculate_max_drawdown(
        self,
        cumulative_returns: pd.Series,
    ) -> float:
        """
        Calculate maximum drawdown from cumulative return series.
        """
        running_max = cumulative_returns.cummax()

        drawdown = cumulative_returns / running_max - 1.0

        return drawdown.min()
