import pandas as pd

from src.utils.config import CONFIG


class TargetBuilder:
    """
    Build future excess return targets.

    target =
        future_stock_return
        -
        future_benchmark_return
    """

    def __init__(
        self,
        prediction_horizon_months: int | None = None,
    ) -> None:
        self.prediction_horizon_months = (
            prediction_horizon_months or CONFIG.prediction_horizon_months
        )

    def build_monthly_target(
        self,
        stock_prices: pd.DataFrame,
        benchmark_prices: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Build excess-return target.

        Parameters
        ----------
        stock_prices:
            Universe dataset.

        benchmark_prices:
            Ibovespa dataset.

        Returns
        -------
        pd.DataFrame
        """
        stock_df = stock_prices.copy()
        benchmark_df = benchmark_prices.copy()

        stock_df["date"] = pd.to_datetime(stock_df["date"])
        benchmark_df["date"] = pd.to_datetime(benchmark_df["date"])

        stock_df = stock_df.sort_values(["ticker", "date"])

        benchmark_df = benchmark_df.sort_values("date")

        trading_days_per_month = 21

        horizon = self.prediction_horizon_months * trading_days_per_month

        # Future stock return
        stock_df["future_stock_price"] = stock_df.groupby("ticker")["adj_close"].shift(
            -horizon
        )

        stock_df["future_stock_return"] = (
            stock_df["future_stock_price"] / stock_df["adj_close"] - 1.0
        )

        # Future benchmark return
        benchmark_df["future_benchmark_price"] = benchmark_df["adj_close"].shift(
            -horizon
        )

        benchmark_df["future_benchmark_return"] = (
            benchmark_df["future_benchmark_price"] / benchmark_df["adj_close"] - 1.0
        )

        benchmark_returns = benchmark_df[
            [
                "date",
                "future_benchmark_return",
            ]
        ]

        stock_df = stock_df.merge(
            benchmark_returns,
            on="date",
            how="left",
        )

        stock_df["target"] = (
            stock_df["future_stock_return"] - stock_df["future_benchmark_return"]
        )

        return stock_df
