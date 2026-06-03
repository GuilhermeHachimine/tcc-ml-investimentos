from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class ProjectConfig:
    # Project paths
    project_root: Path = Path(__file__).resolve().parents[2]
    raw_data_dir: Path = project_root / "data" / "raw"
    processed_data_dir: Path = project_root / "data" / "processed"
    external_data_dir: Path = project_root / "data" / "external"
    reports_dir: Path = project_root / "reports"
    figures_dir: Path = reports_dir / "figures"
    tables_dir: Path = reports_dir / "tables"

    # Study period
    start_date: str = "2015-01-01"
    end_date: str = "2025-12-31"
    train_end_date: str = "2020-12-31"

    # Market benchmark
    benchmark_ticker: str = "^BVSP"

    # Portfolio strategy
    prediction_horizon_months: int = 1
    rebalance_frequency: str = "M"
    top_n_assets: int = 10
    sensitivity_top_n_assets: tuple[int, ...] = (15, 20)

    # Backtest
    initial_capital: float = 1.0
    risk_free_rate: float = 0.0

    # Reproducibility
    random_state: int = 42

    # MLflow
    mlflow_experiment_name: str = "tcc_ml_stock_selection"


CONFIG = ProjectConfig()