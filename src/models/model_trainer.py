from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.models.model_factory import ModelFactory
from src.utils.config import CONFIG


FEATURE_COLUMNS = [
    "daily_return",
    "return_5d",
    "return_21d",
    "return_63d",
    "volatility_21d",
    "volatility_63d",
    "distance_to_ma_21d",
    "distance_to_ma_63d",
    "relative_volume_21d",
]

TARGET_COLUMN = "target"


@dataclass
class TrainResult:
    model_name: str
    mae: float
    rmse: float
    r2: float
    predictions: pd.DataFrame


class ModelTrainer:
    """
    Train supervised models for future excess return prediction.
    """

    def __init__(self) -> None:
        self.train_end_date = pd.to_datetime(CONFIG.train_end_date)
        self.models = ModelFactory.create_all_models()

    def train_simple_split(
        self,
        dataframe: pd.DataFrame,
    ) -> list[TrainResult]:
        dataframe = dataframe.copy()
        dataframe["date"] = pd.to_datetime(dataframe["date"])

        train_df = dataframe[dataframe["date"] <= self.train_end_date].copy()
        test_df = dataframe[dataframe["date"] > self.train_end_date].copy()

        x_train = train_df[FEATURE_COLUMNS]
        y_train = train_df[TARGET_COLUMN]

        x_test = test_df[FEATURE_COLUMNS]
        y_test = test_df[TARGET_COLUMN]

        results: list[TrainResult] = []

        for model_name, model in self.models.items():
            model.fit(x_train, y_train)

            y_pred = model.predict(x_test)

            predictions = test_df[
                [
                    "date",
                    "ticker",
                    "target",
                    "future_stock_return",
                    "future_benchmark_return",
                ]
            ].copy()

            predictions["model_name"] = model_name
            predictions["prediction"] = y_pred

            result = TrainResult(
                model_name=model_name,
                mae=mean_absolute_error(y_test, y_pred),
                rmse=np.sqrt(mean_squared_error(y_test, y_pred)),
                r2=r2_score(y_test, y_pred),
                predictions=predictions,
            )

            results.append(result)

        return results

    def print_results(
        self,
        results: list[TrainResult],
    ) -> None:
        for result in results:
            print(f"\nModel: {result.model_name}")
            print(f"MAE : {result.mae:.6f}")
            print(f"RMSE: {result.rmse:.6f}")
            print(f"R²  : {result.r2:.6f}")
