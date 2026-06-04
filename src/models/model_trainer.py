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

    def train_simple_split(
        self,
        dataframe: pd.DataFrame,
    ) -> list[TrainResult]:
        dataframe = dataframe.copy()
        dataframe["date"] = pd.to_datetime(dataframe["date"])

        train_df = dataframe[dataframe["date"] <= self.train_end_date].copy()
        test_df = dataframe[dataframe["date"] > self.train_end_date].copy()

        models = ModelFactory.create_all_models()

        return self._train_and_predict(
            train_df=train_df,
            test_df=test_df,
            models=models,
        )

    def train_walk_forward_by_year(
        self,
        dataframe: pd.DataFrame,
        first_test_year: int = 2021,
    ) -> list[TrainResult]:
        """
        Train models using expanding-window walk-forward validation.

        For each test year:
        - train on all data before that year;
        - predict only that year;
        - concatenate predictions across years.
        """
        dataframe = dataframe.copy()
        dataframe["date"] = pd.to_datetime(dataframe["date"])

        max_year = dataframe["date"].dt.year.max()
        all_predictions_by_model: dict[str, list[pd.DataFrame]] = {
            "decision_tree": [],
            "random_forest": [],
            "xgboost": [],
        }

        for test_year in range(first_test_year, max_year + 1):
            train_df = dataframe[dataframe["date"].dt.year < test_year].copy()
            test_df = dataframe[dataframe["date"].dt.year == test_year].copy()

            if train_df.empty or test_df.empty:
                continue

            models = ModelFactory.create_all_models()

            yearly_results = self._train_and_predict(
                train_df=train_df,
                test_df=test_df,
                models=models,
            )

            for result in yearly_results:
                predictions = result.predictions.copy()
                predictions["walk_forward_test_year"] = test_year
                all_predictions_by_model[result.model_name].append(predictions)

        final_results: list[TrainResult] = []

        for model_name, prediction_frames in all_predictions_by_model.items():
            if not prediction_frames:
                continue

            predictions = pd.concat(
                prediction_frames,
                ignore_index=True,
            )

            y_true = predictions[TARGET_COLUMN]
            y_pred = predictions["prediction"]

            final_results.append(
                TrainResult(
                    model_name=model_name,
                    mae=mean_absolute_error(y_true, y_pred),
                    rmse=np.sqrt(mean_squared_error(y_true, y_pred)),
                    r2=r2_score(y_true, y_pred),
                    predictions=predictions,
                )
            )

        return final_results

    def _train_and_predict(
        self,
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
        models: dict[str, object],
    ) -> list[TrainResult]:
        x_train = train_df[FEATURE_COLUMNS]
        y_train = train_df[TARGET_COLUMN]

        x_test = test_df[FEATURE_COLUMNS]
        y_test = test_df[TARGET_COLUMN]

        results: list[TrainResult] = []

        for model_name, model in models.items():
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
