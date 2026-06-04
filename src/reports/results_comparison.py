import pandas as pd

from src.utils.config import CONFIG


class ResultsComparison:
    """
    Compare simple split and walk-forward results.
    """

    def build_comparison_table(
        self,
        simple_split_metrics: pd.DataFrame,
        walk_forward_metrics: pd.DataFrame,
    ) -> pd.DataFrame:

        simple = simple_split_metrics.copy()
        simple["validation_type"] = "simple_split"

        walk = walk_forward_metrics.copy()
        walk["validation_type"] = "walk_forward"

        comparison = pd.concat(
            [simple, walk],
            ignore_index=True,
        )

        comparison = comparison[
            [
                "model_name",
                "validation_type",
                "top_n_assets",
                "portfolio_total_return",
                "portfolio_sharpe",
                "portfolio_max_drawdown",
                "hit_rate",
                "mae",
                "rmse",
                "r2",
            ]
        ]

        comparison = comparison.sort_values(["model_name", "validation_type"])

        return comparison

    def save_results(
        self,
        comparison_dataframe: pd.DataFrame,
    ) -> str:

        CONFIG.tables_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = CONFIG.tables_dir / "validation_comparison.csv"

        comparison_dataframe.to_csv(
            output_path,
            index=False,
        )

        return str(output_path)
