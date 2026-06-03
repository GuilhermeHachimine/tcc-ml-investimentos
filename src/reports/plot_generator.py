import pandas as pd
import matplotlib.pyplot as plt

from src.utils.config import CONFIG


class PlotGenerator:
    """
    Generate plots for reports and final study.
    """

    def __init__(self) -> None:
        CONFIG.figures_dir.mkdir(parents=True, exist_ok=True)

    def plot_equity_curve(
        self,
        backtest_dataframe: pd.DataFrame,
        model_name: str,
        file_name: str,
    ) -> str:
        dataframe = backtest_dataframe.copy()
        dataframe["date"] = pd.to_datetime(dataframe["date"])

        plt.figure(figsize=(10, 6))
        plt.plot(
            dataframe["date"],
            dataframe["portfolio_cumulative_return"],
            label=f"{model_name} Portfolio",
        )
        plt.plot(
            dataframe["date"],
            dataframe["benchmark_cumulative_return"],
            label="Ibovespa",
        )
        plt.title(f"Equity Curve - {model_name}")
        plt.xlabel("Date")
        plt.ylabel("Cumulative value")
        plt.legend()
        plt.tight_layout()

        output_path = CONFIG.figures_dir / file_name
        plt.savefig(output_path, dpi=300)
        plt.close()

        return str(output_path)

    def plot_model_comparison_equity_curve(
        self,
        backtests_by_model: dict[str, pd.DataFrame],
        file_name: str,
    ) -> str:
        """
        Plot all model equity curves against Ibovespa.
        """
        plt.figure(figsize=(10, 6))

        benchmark_plotted = False

        for model_name, backtest_dataframe in backtests_by_model.items():
            dataframe = backtest_dataframe.copy()
            dataframe["date"] = pd.to_datetime(dataframe["date"])

            plt.plot(
                dataframe["date"],
                dataframe["portfolio_cumulative_return"],
                label=model_name,
            )

            if not benchmark_plotted:
                plt.plot(
                    dataframe["date"],
                    dataframe["benchmark_cumulative_return"],
                    label="Ibovespa",
                    linestyle="--",
                )
                benchmark_plotted = True

        plt.title("Equity Curve Comparison - Models vs Ibovespa")
        plt.xlabel("Date")
        plt.ylabel("Cumulative value")
        plt.legend()
        plt.tight_layout()

        output_path = CONFIG.figures_dir / file_name
        plt.savefig(output_path, dpi=300)
        plt.close()

        return str(output_path)

    def plot_feature_importance(
        self,
        importance_dataframe: pd.DataFrame,
        model_name: str,
        file_name: str,
    ) -> str:
        dataframe = importance_dataframe.copy()

        dataframe = dataframe[dataframe["model_name"] == model_name].sort_values(
            "importance_pct", ascending=True
        )

        plt.figure(figsize=(10, 6))
        plt.barh(
            dataframe["feature"],
            dataframe["importance_pct"],
        )
        plt.title(f"Feature Importance - {model_name}")
        plt.xlabel("Importance (%)")
        plt.ylabel("Feature")
        plt.tight_layout()

        output_path = CONFIG.figures_dir / file_name
        plt.savefig(output_path, dpi=300)
        plt.close()

        return str(output_path)
