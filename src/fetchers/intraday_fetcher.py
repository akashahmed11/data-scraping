"""
Intraday data fetcher for Indian market indices.
Provides abstraction layer for multiple data sources with retry logic and rate limiting.
"""

import time
import pandas as pd
import yfinance as yf
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from pathlib import Path
import pytz

import sys
sys.path.append(str(Path(__file__).parent.parent))

from utils.logger import logger
from utils.file_manager import FileManager


class DataSourceBase(ABC):
    """Abstract base class for data sources."""

    @abstractmethod
    def fetch_intraday_data(
        self,
        symbol: str,
        interval: str,
        start_date: datetime,
        end_date: datetime
    ) -> Optional[pd.DataFrame]:
        """
        Fetch intraday data from the data source.

        Args:
            symbol: Ticker symbol
            interval: Time interval (e.g., '1m', '5m', '15m')
            start_date: Start datetime
            end_date: End datetime

        Returns:
            DataFrame with OHLCV data or None
        """
        pass

    @abstractmethod
    def get_supported_intervals(self) -> List[str]:
        """Get list of supported intervals."""
        pass


class YahooFinanceSource(DataSourceBase):
    """Yahoo Finance data source implementation."""

    # Mapping of our standard intervals to yfinance intervals
    INTERVAL_MAP = {
        '1min': '1m',
        '2min': '2m',
        '3min': None,  # Not supported - will be resampled from 1m
        '5min': '5m',
        '10min': None,  # Not supported - will be resampled from 5m
        '15min': '15m',
        '30min': '30m',
        '60min': '60m',
        '90min': '90m',
    }

    # Yahoo Finance ticker symbols for Indian indices
    SYMBOL_MAP = {
        'nifty50': '^NSEI',      # NIFTY 50
        'banknifty': '^NSEBANK',  # BANK NIFTY
        'sensex': '^BSESN',      # SENSEX
    }

    def __init__(self, max_retries: int = 3, retry_delay: int = 2):
        """
        Initialize Yahoo Finance source.

        Args:
            max_retries: Maximum number of retry attempts
            retry_delay: Delay between retries in seconds
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay

    def get_yahoo_symbol(self, symbol: str) -> Optional[str]:
        """Convert our symbol to Yahoo Finance symbol."""
        return self.SYMBOL_MAP.get(symbol.lower())

    def get_supported_intervals(self) -> List[str]:
        """Get list of supported intervals."""
        return list(self.INTERVAL_MAP.keys())

    def resample_data(self, df: pd.DataFrame, target_interval: str) -> pd.DataFrame:
        """
        Resample data to target interval.

        Args:
            df: DataFrame with OHLCV data
            target_interval: Target interval (e.g., '3min', '10min')

        Returns:
            Resampled DataFrame
        """
        # Extract numeric value from interval
        minutes = int(target_interval.replace('min', ''))

        df = df.copy()
        df.set_index('datetime', inplace=True)

        # Resample
        resampled = df.resample(f'{minutes}T').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }).dropna()

        resampled.reset_index(inplace=True)
        return resampled

    def fetch_intraday_data(
        self,
        symbol: str,
        interval: str,
        start_date: datetime,
        end_date: datetime
    ) -> Optional[pd.DataFrame]:
        """
        Fetch intraday data from Yahoo Finance.

        Args:
            symbol: Our standard symbol
            interval: Time interval
            start_date: Start datetime
            end_date: End datetime

        Returns:
            DataFrame with OHLCV data or None
        """
        yahoo_symbol = self.get_yahoo_symbol(symbol)
        if not yahoo_symbol:
            logger.error(f"Unknown symbol: {symbol}")
            return None

        yahoo_interval = self.INTERVAL_MAP.get(interval)

        # For unsupported intervals, fetch finer data and resample
        if yahoo_interval is None:
            logger.info(f"Interval {interval} not directly supported. Will resample from finer interval.")
            if interval in ['3min']:
                base_interval = '1min'
                yahoo_interval = '1m'
            elif interval in ['10min']:
                base_interval = '5min'
                yahoo_interval = '5m'
            else:
                logger.error(f"Cannot resample to interval: {interval}")
                return None
            needs_resampling = True
        else:
            needs_resampling = False

        logger.info(f"Fetching {symbol} ({yahoo_symbol}) data for interval {interval} ({yahoo_interval})")

        for attempt in range(self.max_retries):
            try:
                ticker = yf.Ticker(yahoo_symbol)

                # Fetch data
                df = ticker.history(
                    interval=yahoo_interval,
                    start=start_date,
                    end=end_date,
                    prepost=False,
                    auto_adjust=False
                )

                if df.empty:
                    logger.warning(f"No data returned for {symbol} at {interval}")
                    return None

                # Reset index to get datetime as column
                df.reset_index(inplace=True)

                # Rename columns to our standard format
                column_map = {
                    'Datetime': 'datetime',
                    'Date': 'datetime',
                    'Open': 'open',
                    'High': 'high',
                    'Low': 'low',
                    'Close': 'close',
                    'Volume': 'volume'
                }
                df.rename(columns=column_map, inplace=True)

                # Keep only required columns
                keep_cols = ['datetime', 'open', 'high', 'low', 'close', 'volume']
                df = df[[col for col in keep_cols if col in df.columns]]

                # Ensure datetime is timezone-aware (IST)
                ist = pytz.timezone('Asia/Kolkata')
                if df['datetime'].dt.tz is None:
                    df['datetime'] = df['datetime'].dt.tz_localize('UTC').dt.tz_convert(ist)
                else:
                    df['datetime'] = df['datetime'].dt.tz_convert(ist)

                # Resample if needed
                if needs_resampling:
                    df = self.resample_data(df, interval)

                # Add metadata columns
                df['symbol'] = symbol
                df['timeframe'] = interval

                # Keep datetime as datetime object for validation
                # It will be converted to string in file_manager before CSV save

                logger.info(f"Successfully fetched {len(df)} rows for {symbol} at {interval}")
                return df

            except Exception as e:
                logger.warning(f"Attempt {attempt + 1}/{self.max_retries} failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                else:
                    logger.error(f"Failed to fetch data after {self.max_retries} attempts")
                    return None

        return None


class IntradayDataFetcher:
    """
    Main class for fetching intraday market data.
    Orchestrates data fetching across multiple sources, timeframes, and symbols.
    """

    # Default configuration for Indian indices
    INDICES_CONFIG = {
        'nifty50': {
            'name': 'NIFTY 50',
            'exchange': 'NSE',
        },
        'banknifty': {
            'name': 'BANK NIFTY',
            'exchange': 'NSE',
        },
        'sensex': {
            'name': 'SENSEX',
            'exchange': 'BSE',
        }
    }

    # Standard timeframes to fetch
    STANDARD_TIMEFRAMES = ['1min', '3min', '5min', '10min', '15min']

    def __init__(
        self,
        data_source: Optional[DataSourceBase] = None,
        file_manager: Optional[FileManager] = None
    ):
        """
        Initialize IntradayDataFetcher.

        Args:
            data_source: Data source implementation (defaults to YahooFinanceSource)
            file_manager: File manager instance
        """
        self.data_source = data_source or YahooFinanceSource()
        self.file_manager = file_manager or FileManager()

        logger.info(f"Initialized IntradayDataFetcher with {type(self.data_source).__name__}")

    def get_date_range(self, days_back: int = 60) -> Tuple[datetime, datetime]:
        """
        Get date range for data fetching.

        Args:
            days_back: Number of days to look back from today

        Returns:
            Tuple of (start_date, end_date)
        """
        # Yahoo Finance free tier limitations:
        # - 1m data: last 7 days
        # - 5m, 15m data: last 60 days
        # - Adjust based on your needs

        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)

        return start_date, end_date

    def fetch_symbol_data(
        self,
        symbol: str,
        timeframes: Optional[List[str]] = None,
        days_back: int = 60,
        save_data: bool = True
    ) -> Dict[str, Optional[pd.DataFrame]]:
        """
        Fetch data for a single symbol across multiple timeframes.

        Args:
            symbol: Index symbol
            timeframes: List of timeframes (defaults to STANDARD_TIMEFRAMES)
            days_back: Number of days to fetch
            save_data: Whether to save data to CSV

        Returns:
            Dictionary mapping timeframe to DataFrame
        """
        if timeframes is None:
            timeframes = self.STANDARD_TIMEFRAMES

        results = {}
        start_date, end_date = self.get_date_range(days_back)

        logger.info(f"Fetching data for {symbol} from {start_date.date()} to {end_date.date()}")

        for timeframe in timeframes:
            logger.info(f"Processing {symbol} - {timeframe}")

            try:
                # Fetch data
                df = self.data_source.fetch_intraday_data(
                    symbol=symbol,
                    interval=timeframe,
                    start_date=start_date,
                    end_date=end_date
                )

                if df is not None and not df.empty:
                    results[timeframe] = df

                    # Save to file
                    if save_data:
                        file_path = self.file_manager.save_data(
                            df=df,
                            symbol=symbol,
                            timeframe=timeframe,
                            start_date=start_date,
                            end_date=end_date
                        )

                        if file_path:
                            logger.info(f"✓ Saved {symbol} {timeframe} data to {file_path.name}")
                        else:
                            logger.error(f"✗ Failed to save {symbol} {timeframe} data")
                else:
                    logger.warning(f"✗ No data fetched for {symbol} {timeframe}")
                    results[timeframe] = None

                # Rate limiting - be respectful to data source
                time.sleep(1)

            except Exception as e:
                logger.error(f"Error fetching {symbol} {timeframe}: {e}", exc_info=True)
                results[timeframe] = None

        return results

    def fetch_all_data(
        self,
        symbols: Optional[List[str]] = None,
        timeframes: Optional[List[str]] = None,
        days_back: int = 60
    ) -> Dict[str, Dict[str, Optional[pd.DataFrame]]]:
        """
        Fetch data for all symbols and timeframes.

        Args:
            symbols: List of symbols (defaults to all configured indices)
            timeframes: List of timeframes (defaults to STANDARD_TIMEFRAMES)
            days_back: Number of days to fetch

        Returns:
            Nested dictionary: {symbol: {timeframe: DataFrame}}
        """
        if symbols is None:
            symbols = list(self.INDICES_CONFIG.keys())

        if timeframes is None:
            timeframes = self.STANDARD_TIMEFRAMES

        logger.info(f"Starting data collection for {len(symbols)} symbols, {len(timeframes)} timeframes")
        logger.info(f"Symbols: {symbols}")
        logger.info(f"Timeframes: {timeframes}")

        all_results = {}

        for symbol in symbols:
            logger.info(f"\n{'='*60}")
            logger.info(f"Processing {symbol.upper()}")
            logger.info(f"{'='*60}")

            results = self.fetch_symbol_data(
                symbol=symbol,
                timeframes=timeframes,
                days_back=days_back,
                save_data=True
            )

            all_results[symbol] = results

            # Summary for this symbol
            success_count = sum(1 for df in results.values() if df is not None)
            logger.info(f"Completed {symbol}: {success_count}/{len(timeframes)} timeframes successful")

        return all_results

    def get_summary(self, results: Dict[str, Dict[str, Optional[pd.DataFrame]]]) -> pd.DataFrame:
        """
        Generate summary statistics for fetched data.

        Args:
            results: Results from fetch_all_data

        Returns:
            Summary DataFrame
        """
        summary_data = []

        for symbol, timeframe_data in results.items():
            for timeframe, df in timeframe_data.items():
                if df is not None:
                    summary_data.append({
                        'symbol': symbol,
                        'timeframe': timeframe,
                        'rows': len(df),
                        'start_date': df['datetime'].iloc[0] if len(df) > 0 else None,
                        'end_date': df['datetime'].iloc[-1] if len(df) > 0 else None,
                        'status': 'SUCCESS'
                    })
                else:
                    summary_data.append({
                        'symbol': symbol,
                        'timeframe': timeframe,
                        'rows': 0,
                        'start_date': None,
                        'end_date': None,
                        'status': 'FAILED'
                    })

        return pd.DataFrame(summary_data)
