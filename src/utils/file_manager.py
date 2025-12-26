"""
File management utilities for organizing and saving market data.
Handles CSV operations, file validation, and data integrity checks.
"""

import pandas as pd
from pathlib import Path
from typing import Optional, List
from datetime import datetime
import hashlib

from .logger import logger


class FileManager:
    """Manages file operations for market data storage."""
    
    def __init__(self, base_data_dir: Optional[Path] = None):
        """
        Initialize FileManager.

        Args:
            base_data_dir: Base directory for data storage (defaults to ./data)
        """
        self.base_data_dir = base_data_dir or Path.cwd() / "data"
        self.base_data_dir.mkdir(parents=True, exist_ok=True)

        # Standard columns for market data
        self.required_columns = [
            'datetime', 'open', 'high', 'low', 'close', 'symbol', 'timeframe'
        ]
        self.optional_columns = ['volume']

    def get_data_path(self, symbol: str, timeframe: str) -> Path:
        """
        Get the directory path for a specific symbol and timeframe.

        Args:
            symbol: Index symbol (e.g., 'nifty50', 'banknifty', 'sensex')
            timeframe: Timeframe string (e.g., '1min', '5min', '15min')

        Returns:
            Path object for the data directory
        """
        symbol_dir = self.base_data_dir / symbol.lower().replace(" ", "")
        timeframe_dir = symbol_dir / timeframe
        timeframe_dir.mkdir(parents=True, exist_ok=True)
        return timeframe_dir

    def generate_filename(
        self,
        symbol: str,
        timeframe: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> str:
        """
        Generate standardized filename for data files.

        Args:
            symbol: Index symbol
            timeframe: Timeframe string
            start_date: Start date of data
            end_date: End date of data

        Returns:
            Filename string
        """
        symbol_clean = symbol.lower().replace(" ", "_")

        if start_date and end_date:
            date_range = f"{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}"
        elif start_date:
            date_range = f"from_{start_date.strftime('%Y%m%d')}"
        elif end_date:
            date_range = f"until_{end_date.strftime('%Y%m%d')}"
        else:
            date_range = "latest"

        return f"{symbol_clean}_{timeframe}_{date_range}.csv"

    def validate_dataframe(self, df: pd.DataFrame) -> bool:
        """
        Validate dataframe structure and content.

        Args:
            df: DataFrame to validate

        Returns:
            True if valid, False otherwise
        """
        if df.empty:
            logger.warning("DataFrame is empty")
            return False

        # Check required columns
        missing_cols = set(self.required_columns) - set(df.columns)
        if missing_cols:
            logger.error(f"Missing required columns: {missing_cols}")
            return False

        # Check datetime column
        if not pd.api.types.is_datetime64_any_dtype(df['datetime']):
            logger.error("'datetime' column must be datetime type")
            return False

        # Check numeric columns
        numeric_cols = ['open', 'high', 'low', 'close']
        for col in numeric_cols:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                logger.error(f"'{col}' column must be numeric")
                return False

        # Check for null values in critical columns
        null_counts = df[self.required_columns].isnull().sum()
        if null_counts.any():
            logger.warning(f"Null values found:\n{null_counts[null_counts > 0]}")

        # Validate OHLC relationships
        invalid_ohlc = (
            (df['high'] < df['low']) |
            (df['high'] < df['open']) |
            (df['high'] < df['close']) |
            (df['low'] > df['open']) |
            (df['low'] > df['close'])
        )
        if invalid_ohlc.any():
            logger.warning(f"Found {invalid_ohlc.sum()} rows with invalid OHLC relationships")

        return True

    def save_data(
        self,
        df: pd.DataFrame,
        symbol: str,
        timeframe: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        append: bool = False
    ) -> Optional[Path]:
        """
        Save DataFrame to CSV file.

        Args:
            df: DataFrame to save
            symbol: Index symbol
            timeframe: Timeframe string
            start_date: Start date of data
            end_date: End date of data
            append: Whether to append to existing file

        Returns:
            Path to saved file, or None if save failed
        """
        if not self.validate_dataframe(df):
            logger.error("Data validation failed. Skipping save.")
            return None

        try:
            # Make a copy to avoid modifying the original
            df = df.copy()

            # Ensure datetime is sorted
            df = df.sort_values('datetime').reset_index(drop=True)

            # Get save path
            data_dir = self.get_data_path(symbol, timeframe)
            filename = self.generate_filename(symbol, timeframe, start_date, end_date)
            file_path = data_dir / filename

            # Handle append mode
            if append and file_path.exists():
                existing_df = pd.read_csv(file_path, parse_dates=['datetime'])
                df = pd.concat([existing_df, df], ignore_index=True)
                df = df.drop_duplicates(subset=['datetime'], keep='last')
                df = df.sort_values('datetime').reset_index(drop=True)
                logger.info(f"Appending to existing file: {file_path}")
            else:
                logger.info(f"Saving new file: {file_path}")

            # Convert datetime to string for CSV (after validation)
            if pd.api.types.is_datetime64_any_dtype(df['datetime']):
                df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S%z')

            # Save to CSV
            df.to_csv(file_path, index=False)

            # Verify save
            file_size = file_path.stat().st_size
            logger.info(f"Successfully saved {len(df)} rows ({file_size / 1024:.2f} KB) to {file_path}")

            return file_path

        except Exception as e:
            logger.error(f"Error saving data: {e}", exc_info=True)
            return None

    def load_data(self, file_path: Path) -> Optional[pd.DataFrame]:
        """
        Load data from CSV file.

        Args:
            file_path: Path to CSV file

        Returns:
            DataFrame or None if load failed
        """
        try:
            if not file_path.exists():
                logger.error(f"File not found: {file_path}")
                return None

            df = pd.read_csv(file_path, parse_dates=['datetime'])
            logger.info(f"Loaded {len(df)} rows from {file_path}")
            return df

        except Exception as e:
            logger.error(f"Error loading data from {file_path}: {e}", exc_info=True)
            return None

    def file_exists(self, symbol: str, timeframe: str, filename: str) -> bool:
        """
        Check if a data file exists.

        Args:
            symbol: Index symbol
            timeframe: Timeframe string
            filename: Name of file to check

        Returns:
            True if file exists, False otherwise
        """
        data_dir = self.get_data_path(symbol, timeframe)
        file_path = data_dir / filename
        return file_path.exists()

    def get_existing_files(self, symbol: str, timeframe: str) -> List[Path]:
        """
        Get list of existing data files for a symbol and timeframe.

        Args:
            symbol: Index symbol
            timeframe: Timeframe string

        Returns:
            List of Path objects
        """
        data_dir = self.get_data_path(symbol, timeframe)
        return sorted(data_dir.glob("*.csv"))

    def calculate_file_hash(self, file_path: Path) -> str:
        """
        Calculate MD5 hash of a file for integrity checking.

        Args:
            file_path: Path to file

        Returns:
            MD5 hash string
        """
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
