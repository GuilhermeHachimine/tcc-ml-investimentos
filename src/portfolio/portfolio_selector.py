import pandas as pd

from src.utils.config import CONFIG


class PortfolioSelector:
    """
    Select top-ranked assets based on model predictions.

    The portfolio is formed at the last available trading day of each month.
    """

    def __init__(
        self,
        top_n_assets: int | None = None,
    ) -> None:
        self.top_n_assets = top_n_assets or CONFIG.top_n_assets

    def select_top_assets(
        self,
        predictions: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Select top N assets by prediction on each monthly rebalance date.
        """
        selected = predictions.copy()
        selected["date"] = pd.to_datetime(selected["date"])

        selected = self._filter_monthly_rebalance_dates(selected)

        selected = selected.sort_values(
            ["date", "prediction"],
            ascending=[True, False],
        )

        selected["rank"] = selected.groupby("date")["prediction"].rank(
            method="first", ascending=False
        )

        selected = selected[selected["rank"] <= self.top_n_assets].copy()

        selected["portfolio_weight"] = 1.0 / self.top_n_assets

        return selected.reset_index(drop=True)

    def _filter_monthly_rebalance_dates(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Keep only the last available trading date of each month.
        """
        filtered = dataframe.copy()

        filtered["year_month"] = filtered["date"].dt.to_period("M")

        rebalance_dates = filtered.groupby("year_month")["date"].max().reset_index()

        filtered = filtered.merge(
            rebalance_dates,
            on=["year_month", "date"],
            how="inner",
        )

        filtered = filtered.drop(columns=["year_month"])

        return filtered
