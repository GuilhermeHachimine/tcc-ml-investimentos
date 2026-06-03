from pathlib import Path

import pandas as pd
import yfinance as yf

from src.data.ibov_universe import get_stock_universe
from src.utils.config import CONFIG


class YahooDataLoader:
    """
    Download and store historical market data from Yahoo Finance.
    """

    def __init__(self) -> None:
        self.start_date = CONFIG.start_date
        self.end_date = CONFIG.end_date
        self.raw_data_dir = CONFIG.raw_data_dir

    def download_ticker_data(self, ticker: str) -> pd.DataFrame:
        """
        Download historical data for a single ticker and standardize columns.
        """
        dataframe = yf.download(
            ticker,
            start=self.start_date,
            end=self.end_date,
            auto_adjust=False,
            progress=False,
        )

        return self._standardize_yfinance_dataframe(
            dataframe=dataframe,
            ticker=ticker,
        )

    def _standardize_yfinance_dataframe(
        self,
        dataframe: pd.DataFrame,
        ticker: str,
    ) -> pd.DataFrame:
        """
        Convert yfinance output into a standard flat schema.
        """
        if dataframe.empty:
            raise ValueError(f"No data returned for ticker: {ticker}")

        if isinstance(dataframe.columns, pd.MultiIndex):
            dataframe.columns = dataframe.columns.get_level_values(0)

        dataframe = dataframe.reset_index()

        dataframe = dataframe.rename(
            columns={
                "Date": "date",
                "Open": "open",
                "High": "high",
                "Low": "low",
                "Close": "close",
                "Adj Close": "adj_close",
                "Volume": "volume",
            }
        )

        dataframe["ticker"] = ticker

        expected_columns = [
            "date",
            "ticker",
            "open",
            "high",
            "low",
            "close",
            "adj_close",
            "volume",
        ]

        return dataframe[expected_columns]

    def download_many_tickers(
        self,
        tickers: list[str],
    ) -> tuple[pd.DataFrame, list[str]]:
        """
        Download historical data for multiple tickers.

        Returns
        -------
        tuple[pd.DataFrame, list[str]]
            Consolidated price dataframe and list of failed tickers.
        """
        dataframes: list[pd.DataFrame] = []
        failed_tickers: list[str] = []

        for ticker in tickers:
            try:
                ticker_dataframe = self.download_ticker_data(ticker)
                dataframes.append(ticker_dataframe)
                print(f"Downloaded {ticker}: {ticker_dataframe.shape[0]} rows")
            except Exception as error:
                failed_tickers.append(ticker)
                print(f"Failed to download {ticker}: {error}")

        if not dataframes:
            raise ValueError("No ticker data was downloaded.")

        consolidated_dataframe = pd.concat(
            dataframes,
            ignore_index=True,
        )

        return consolidated_dataframe, failed_tickers

    def download_universe(
        self,
        tickers: list[str] | None = None,
    ) -> tuple[pd.DataFrame, list[str]]:
        """
        Download historical data for the IBOV stock universe.
        """
        selected_tickers = tickers or get_stock_universe()

        return self.download_many_tickers(
            tickers=selected_tickers,
        )

    def download_benchmark(self) -> pd.DataFrame:
        """
        Download Ibovespa benchmark historical data.
        """
        return self.download_ticker_data(
            ticker=CONFIG.benchmark_ticker,
        )

    def save_dataset(
        self,
        dataframe: pd.DataFrame,
        file_stem: str,
        save_csv: bool = True,
        save_parquet: bool = True,
    ) -> dict[str, Path]:
        """
        Save a dataset in CSV and/or Parquet format.
        """
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

        output_paths: dict[str, Path] = {}

        if save_csv:
            csv_path = self.raw_data_dir / f"{file_stem}.csv"
            dataframe.to_csv(csv_path, index=False)
            output_paths["csv"] = csv_path

        if save_parquet:
            parquet_path = self.raw_data_dir / f"{file_stem}.parquet"
            dataframe.to_parquet(parquet_path, index=False)
            output_paths["parquet"] = parquet_path

        return output_paths

    def download_and_save_universe(
        self,
        tickers: list[str] | None = None,
        file_stem: str = "ibov_prices",
    ) -> tuple[pd.DataFrame, list[str], dict[str, Path]]:
        """
        Download and save the IBOV universe historical data.
        """
        dataframe, failed_tickers = self.download_universe(
            tickers=tickers,
        )

        output_paths = self.save_dataset(
            dataframe=dataframe,
            file_stem=file_stem,
        )

        return dataframe, failed_tickers, output_paths

    def download_and_save_benchmark(
        self,
        file_stem: str = "ibovespa_benchmark",
    ) -> tuple[pd.DataFrame, dict[str, Path]]:
        """
        Download and save the Ibovespa benchmark historical data.
        """
        dataframe = self.download_benchmark()

        output_paths = self.save_dataset(
            dataframe=dataframe,
            file_stem=file_stem,
        )

        return dataframe, output_paths
