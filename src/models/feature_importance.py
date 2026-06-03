import pandas as pd

from src.models.model_factory import ModelFactory
from src.models.model_trainer import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
)
from src.utils.config import CONFIG


class FeatureImportanceAnalyzer:
    """
    Analyze feature importance from tree-based models.
    """

    def __init__(self) -> None:
        self.models = {
            "random_forest": ModelFactory.create_random_forest(),
            "xgboost": ModelFactory.create_xgboost(),
        }

        self.train_end_date = pd.to_datetime(CONFIG.train_end_date)

    def calculate_feature_importance(
        self,
        dataframe: pd.DataFrame,
    ) -> pd.DataFrame:

        dataframe = dataframe.copy()

        dataframe["date"] = pd.to_datetime(dataframe["date"])

        train_df = dataframe[dataframe["date"] <= self.train_end_date]

        x_train = train_df[FEATURE_COLUMNS]
        y_train = train_df[TARGET_COLUMN]

        importance_rows = []

        for model_name, model in self.models.items():
            model.fit(
                x_train,
                y_train,
            )

            for feature_name, importance in zip(
                FEATURE_COLUMNS,
                model.feature_importances_,
                strict=False,
            ):
                importance_rows.append(
                    {
                        "model_name": model_name,
                        "feature": feature_name,
                        "importance": importance,
                    }
                )

        importance_df = pd.DataFrame(importance_rows)

        importance_df["importance_pct"] = (
            importance_df.groupby("model_name")["importance"].transform(
                lambda values: values / values.sum()
            )
            * 100
        )

        importance_df = importance_df.sort_values(
            ["model_name", "importance_pct"],
            ascending=[True, False],
        )

        return importance_df

    def save_results(
        self,
        dataframe: pd.DataFrame,
    ) -> str:

        CONFIG.tables_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = CONFIG.tables_dir / "feature_importance.csv"

        dataframe.to_csv(
            output_path,
            index=False,
        )

        return str(output_path)
