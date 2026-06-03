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

        dataframe = self._standardize_yfinance_dataframe(
            dataframe=dataframe,
            ticker=ticker,
        )

        return dataframe

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

        dataframe = dataframe[expected_columns]

        return dataframe

    def save_ticker_data(
        self,
        dataframe: pd.DataFrame,
        ticker: str,
    ) -> Path:
        """
        Save ticker data into data/raw.
        """
        self.raw_data_dir.mkdir(parents=True, exist_ok=True)

        output_path = self.raw_data_dir / f"{ticker}.csv"

        dataframe.to_csv(
            output_path,
            index=False,
        )

        return output_path

    def download_and_save_ticker(
        self,
        ticker: str,
    ) -> pd.DataFrame:
        """
        Download and save a single ticker.
        """
        dataframe = self.download_ticker_data(ticker)

        self.save_ticker_data(
            dataframe=dataframe,
            ticker=ticker,
        )

        return dataframe

    def download_benchmark(self) -> pd.DataFrame:
        """
        Download Ibovespa benchmark.
        """
        return self.download_ticker_data(
            CONFIG.benchmark_ticker
        )

    def get_universe(self) -> list[str]:
        """
        Return the IBOV stock universe.
        """
        return get_stock_universe()