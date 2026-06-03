import pandas as pd


class FeatureEngineer:
    """
    Build predictive features from historical stock prices.

    All features are calculated using only current and past information.
    This avoids data leakage.
    """

    def __init__(self) -> None:
        self.return_windows = [5, 21, 63]
        self.volatility_windows = [21, 63]
        self.moving_average_windows = [21, 63]
        self.volume_window = 21

    def build_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Build stock-level features.

        Parameters
        ----------
        dataframe:
            Stock price dataframe containing date, ticker, adj_close and volume.

        Returns
        -------
        pd.DataFrame
            Dataframe with engineered features.
        """
        feature_df = dataframe.copy()

        feature_df["date"] = pd.to_datetime(feature_df["date"])

        feature_df = feature_df.sort_values(
            ["ticker", "date"]
        )

        feature_df["daily_return"] = (
            feature_df.groupby("ticker")["adj_close"]
            .pct_change()
        )

        feature_df = self._add_past_returns(feature_df)
        feature_df = self._add_volatility_features(feature_df)
        feature_df = self._add_moving_average_features(feature_df)
        feature_df = self._add_volume_features(feature_df)

        return feature_df

    def _add_past_returns(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Add past return features.
        """
        feature_df = dataframe.copy()

        for window in self.return_windows:
            feature_df[f"return_{window}d"] = (
                feature_df.groupby("ticker")["adj_close"]
                .pct_change(periods=window)
            )

        return feature_df

    def _add_volatility_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Add rolling volatility features.
        """
        feature_df = dataframe.copy()

        for window in self.volatility_windows:
            feature_df[f"volatility_{window}d"] = (
                feature_df.groupby("ticker")["daily_return"]
                .rolling(window=window)
                .std()
                .reset_index(level=0, drop=True)
            )

        return feature_df

    def _add_moving_average_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Add moving average and price-distance features.
        """
        feature_df = dataframe.copy()

        for window in self.moving_average_windows:
            moving_average_column = f"moving_average_{window}d"
            distance_column = f"distance_to_ma_{window}d"

            feature_df[moving_average_column] = (
                feature_df.groupby("ticker")["adj_close"]
                .rolling(window=window)
                .mean()
                .reset_index(level=0, drop=True)
            )

            feature_df[distance_column] = (
                feature_df["adj_close"]
                / feature_df[moving_average_column]
                - 1.0
            )

        return feature_df

    def _add_volume_features(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Add relative volume feature.
        """
        feature_df = dataframe.copy()

        feature_df["average_volume_21d"] = (
            feature_df.groupby("ticker")["volume"]
            .rolling(window=self.volume_window)
            .mean()
            .reset_index(level=0, drop=True)
        )

        feature_df["relative_volume_21d"] = (
            feature_df["volume"]
            / feature_df["average_volume_21d"]
        )

        return feature_df