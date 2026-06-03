"""
Load the fixed Ibovespa stock universe used in the study.

The stock universe is based on the official B3 "Ações por Índice" file,
downloaded on 2026-06-03. The study uses a fixed universe composed of assets
that participate in the IBOV index in the May-August 2026 theoretical portfolio.

Methodological note:
Using a fixed universe improves reproducibility, but may introduce survivorship
bias. This limitation should be documented in the final study.
"""

from pathlib import Path

import pandas as pd

from src.utils.config import CONFIG


B3_INDEX_FILE_NAME = "AcoesIndices_2026-06-03.csv"
IBOV_INDEX_CODE = "IBOV"
YFINANCE_SUFFIX = ".SA"


def get_b3_index_file_path(file_name: str = B3_INDEX_FILE_NAME) -> Path:
    """Return the expected path for the B3 index membership file."""
    return CONFIG.external_data_dir / file_name


def load_b3_index_membership(file_path: Path | None = None) -> pd.DataFrame:
    """
    Load and normalize the B3 index membership CSV file.

    The downloaded B3 file contains two metadata rows before the actual table.
    Rows are structured as:
    company_name;share_type;ticker;index_memberships;
    """
    selected_file_path = file_path or get_b3_index_file_path()

    if not selected_file_path.exists():
        raise FileNotFoundError(
            f"B3 index membership file not found: {selected_file_path}"
        )

    dataframe = pd.read_csv(
        selected_file_path,
        sep=";",
        encoding="latin1",
        skiprows=3,
        header=None,
        names=["company_name", "share_type", "ticker", "index_memberships", "empty"],
    )

    dataframe = dataframe.drop(columns=["empty"])
    dataframe = dataframe.dropna(subset=["ticker", "index_memberships"])

    return dataframe


def get_stock_universe(
    index_code: str = IBOV_INDEX_CODE,
    file_path: Path | None = None,
    add_yfinance_suffix: bool = True,
) -> list[str]:
    """
    Return the fixed stock universe for a given B3 index.

    Parameters
    ----------
    index_code:
        B3 index code used to filter the membership file. The default is IBOV.
    file_path:
        Optional custom path to the B3 CSV file.
    add_yfinance_suffix:
        If True, appends ".SA" to each ticker for yfinance compatibility.

    Returns
    -------
    list[str]
        Sorted list of tickers in the requested index.
    """
    dataframe = load_b3_index_membership(file_path=file_path)

    filtered_dataframe = dataframe[
        dataframe["index_memberships"]
        .fillna("")
        .str.split(",")
        .apply(lambda indexes: index_code in [item.strip() for item in indexes])
    ].copy()

    tickers = (
        filtered_dataframe["ticker"]
        .dropna()
        .astype(str)
        .str.strip()
        .drop_duplicates()
        .sort_values()
        .tolist()
    )

    if add_yfinance_suffix:
        tickers = [f"{ticker}{YFINANCE_SUFFIX}" for ticker in tickers]

    return tickers