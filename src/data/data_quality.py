from pathlib import Path

import pandas as pd


class DataQualityAnalyzer:
    """
    Performs basic data quality checks on market datasets.
    """

    def __init__(self, dataframe: pd.DataFrame) -> None:
        self.dataframe = dataframe.copy()

    def get_summary(self) -> dict:
        return {
            "rows": len(self.dataframe),
            "columns": len(self.dataframe.columns),
            "tickers": self.dataframe["ticker"].nunique(),
            "min_date": self.dataframe["date"].min(),
            "max_date": self.dataframe["date"].max(),
        }

    def get_null_counts(self) -> pd.Series:
        return self.dataframe.isnull().sum()

    def get_duplicate_count(self) -> int:
        return self.dataframe.duplicated(subset=["date", "ticker"]).sum()

    def get_observation_count_per_ticker(self) -> pd.DataFrame:
        return (
            self.dataframe.groupby("ticker")
            .size()
            .reset_index(name="num_rows")
            .sort_values("num_rows")
        )

    def get_short_history_tickers(
        self,
        minimum_rows: int = 2000,
    ) -> pd.DataFrame:
        ticker_counts = self.get_observation_count_per_ticker()

        return ticker_counts[ticker_counts["num_rows"] < minimum_rows].copy()
