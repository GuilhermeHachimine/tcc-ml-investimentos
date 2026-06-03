import pandas as pd

from src.utils.config import CONFIG


class PortfolioSelector:
    """
    Select top-ranked assets based on model predictions.
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
        Select top N assets by prediction for each date.
        """
        selected = predictions.copy()
        selected["date"] = pd.to_datetime(selected["date"])

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
