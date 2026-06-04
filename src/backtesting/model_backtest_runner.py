import pandas as pd

from src.backtesting.backtester import Backtester
from src.models.model_trainer import ModelTrainer, TrainResult
from src.portfolio.portfolio_selector import PortfolioSelector
from src.utils.config import CONFIG


class ModelBacktestRunner:
    """
    Train models, build portfolios and compare backtest metrics.
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
        """
        train_results = self.trainer.train_simple_split(
            dataframe=dataframe,
        )

        return self._run_backtests(
            train_results=train_results,
            top_n_assets=top_n_assets,
        )

    def run_walk_forward_backtests(
        self,
        dataframe: pd.DataFrame,
        top_n_assets: int | None = None,
        first_test_year: int = 2021,
    ) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
        """
        Run walk-forward backtests for all models.
        """
        train_results = self.trainer.train_walk_forward_by_year(
            dataframe=dataframe,
            first_test_year=first_test_year,
        )

        return self._run_backtests(
            train_results=train_results,
            top_n_assets=top_n_assets,
        )

    def run_sensitivity_analysis(
        self,
        dataframe: pd.DataFrame,
        top_n_values: list[int],
    ) -> pd.DataFrame:
        """
        Run simple split sensitivity analysis for multiple portfolio sizes.
        """
        train_results = self.trainer.train_simple_split(
            dataframe=dataframe,
        )

        return self._run_sensitivity_from_train_results(
            train_results=train_results,
            top_n_values=top_n_values,
        )

    def run_walk_forward_sensitivity_analysis(
        self,
        dataframe: pd.DataFrame,
        top_n_values: list[int],
        first_test_year: int = 2021,
    ) -> pd.DataFrame:
        """
        Run walk-forward sensitivity analysis for multiple portfolio sizes.
        """
        train_results = self.trainer.train_walk_forward_by_year(
            dataframe=dataframe,
            first_test_year=first_test_year,
        )

        return self._run_sensitivity_from_train_results(
            train_results=train_results,
            top_n_values=top_n_values,
        )

    def _run_backtests(
        self,
        train_results: list[TrainResult],
        top_n_assets: int | None = None,
    ) -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
        """
        Build portfolios and calculate backtests for train results.
        """
        selected_top_n = top_n_assets or CONFIG.top_n_assets

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

        metrics_dataframe = self._order_metrics_columns(pd.DataFrame(metrics_rows))

        return metrics_dataframe, backtests_by_model

    def _run_sensitivity_from_train_results(
        self,
        train_results: list[TrainResult],
        top_n_values: list[int],
    ) -> pd.DataFrame:
        """
        Run sensitivity analysis from already trained/predicted results.
        """
        metrics_rows: list[dict] = []

        for top_n_assets in top_n_values:
            for train_result in train_results:
                portfolio = PortfolioSelector(
                    top_n_assets=top_n_assets,
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
                metrics["top_n_assets"] = top_n_assets
                metrics["mae"] = train_result.mae
                metrics["rmse"] = train_result.rmse
                metrics["r2"] = train_result.r2

                metrics_rows.append(metrics)

        metrics_dataframe = self._order_metrics_columns(pd.DataFrame(metrics_rows))

        metrics_dataframe = metrics_dataframe.sort_values(
            ["model_name", "top_n_assets"]
        ).reset_index(drop=True)

        return metrics_dataframe

    def save_results(
        self,
        metrics_dataframe: pd.DataFrame,
        backtests_by_model: dict[str, pd.DataFrame],
        file_prefix: str,
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

    def save_sensitivity_results(
        self,
        metrics_dataframe: pd.DataFrame,
        file_name: str = "sensitivity_analysis.csv",
    ) -> str:
        """
        Save sensitivity analysis results.
        """
        CONFIG.tables_dir.mkdir(parents=True, exist_ok=True)

        output_path = CONFIG.tables_dir / file_name

        metrics_dataframe.to_csv(
            output_path,
            index=False,
        )

        return str(output_path)

    def _order_metrics_columns(
        self,
        metrics_dataframe: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Return metrics dataframe with a standard column order.
        """
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

        return metrics_dataframe[metric_order]
