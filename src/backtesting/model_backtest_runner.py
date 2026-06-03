import pandas as pd

from src.backtesting.backtester import Backtester
from src.models.model_trainer import ModelTrainer, TrainResult
from src.portfolio.portfolio_selector import PortfolioSelector
from src.utils.config import CONFIG


class ModelBacktestRunner:
    """
    Train all models, build portfolios and compare backtest metrics.
    """

    def __init__(self) -> None:
        self.trainer = ModelTrainer()
        self.backtester = Backtester()

    def run_simple_split_backtests(
        self,
        dataframe: pd.DataFrame,
        top_n_assets: int | None = None,
    ) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
        """
        Run simple temporal split backtests for all models.

        Returns
        -------
        tuple[pd.DataFrame, dict[str, pd.DataFrame]]
            Metrics comparison table and backtest results by model.
        """
        selected_top_n = top_n_assets or CONFIG.top_n_assets

        train_results = self.trainer.train_simple_split(
            dataframe=dataframe,
        )

        metrics_rows: list[dict] = []
        backtests_by_model: dict[str, pd.DataFrame] = {}

        for train_result in train_results:
            portfolio = PortfolioSelector(
                top_n_assets=selected_top_n,
            ).select_top_assets(
                predictions=train_result.predictions,
            )

            backtest_result = self.backtester.run_backtest(
                selected_portfolio=portfolio,
            )

            metrics = self.backtester.calculate_performance_metrics(
                backtest_result=backtest_result,
            )

            metrics["model_name"] = train_result.model_name
            metrics["top_n_assets"] = selected_top_n
            metrics["mae"] = train_result.mae
            metrics["rmse"] = train_result.rmse
            metrics["r2"] = train_result.r2

            metrics_rows.append(metrics)
            backtests_by_model[train_result.model_name] = backtest_result

        metrics_dataframe = pd.DataFrame(metrics_rows)

        metric_order = [
            "model_name",
            "top_n_assets",
            "portfolio_total_return",
            "benchmark_total_return",
            "portfolio_volatility",
            "benchmark_volatility",
            "portfolio_sharpe",
            "benchmark_sharpe",
            "portfolio_max_drawdown",
            "benchmark_max_drawdown",
            "hit_rate",
            "mae",
            "rmse",
            "r2",
        ]

        metrics_dataframe = metrics_dataframe[metric_order]

        return metrics_dataframe, backtests_by_model

    def save_results(
        self,
        metrics_dataframe: pd.DataFrame,
        backtests_by_model: dict[str, pd.DataFrame],
        file_prefix: str = "simple_split_top10",
    ) -> dict[str, str]:
        """
        Save metrics and backtest results to reports/tables.
        """
        CONFIG.tables_dir.mkdir(parents=True, exist_ok=True)

        output_paths: dict[str, str] = {}

        metrics_path = CONFIG.tables_dir / f"{file_prefix}_metrics.csv"

        metrics_dataframe.to_csv(
            metrics_path,
            index=False,
        )

        output_paths["metrics"] = str(metrics_path)

        for model_name, backtest_dataframe in backtests_by_model.items():
            backtest_path = (
                CONFIG.tables_dir / f"{file_prefix}_{model_name}_backtest.csv"
            )

            backtest_dataframe.to_csv(
                backtest_path,
                index=False,
            )

            output_paths[f"{model_name}_backtest"] = str(backtest_path)

        return output_paths
