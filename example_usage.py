"""
Example usage script for the Indian Market Data Collector.

This script demonstrates various ways to use the data collection framework.
Run this to verify your installation and see sample usage patterns.

Usage:
    python example_usage.py
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from fetchers.intraday_fetcher import IntradayDataFetcher, YahooFinanceSource
from utils.logger import setup_logger, logger
from utils.file_manager import FileManager


def example_1_basic_usage():
    """Example 1: Basic usage - fetch data for one symbol and timeframe."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Usage - Single Symbol, Single Timeframe")
    print("="*70)

    # Initialize fetcher
    fetcher = IntradayDataFetcher()

    # Fetch NIFTY 50 data for 5-minute timeframe
    results = fetcher.fetch_symbol_data(
        symbol='nifty50',
        timeframes=['5min'],
        days_back=30,
        save_data=True
    )

    # Check results
    if results['5min'] is not None:
        df = results['5min']
        print(f"\n✓ Successfully fetched {len(df)} rows of NIFTY 50 5-minute data")
        print(f"\nFirst 5 rows:")
        print(df.head())
    else:
        print("\n✗ Failed to fetch data")


def example_2_multiple_timeframes():
    """Example 2: Fetch multiple timeframes for a single symbol."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Multiple Timeframes for Single Symbol")
    print("="*70)

    fetcher = IntradayDataFetcher()

    # Fetch multiple timeframes
    results = fetcher.fetch_symbol_data(
        symbol='banknifty',
        timeframes=['1min', '5min', '15min'],
        days_back=7,  # Last 7 days for 1-minute data
        save_data=True
    )

    # Summary
    print("\nResults Summary:")
    for timeframe, df in results.items():
        if df is not None:
            print(f"  ✓ {timeframe:6s}: {len(df):5d} rows")
        else:
            print(f"  ✗ {timeframe:6s}: No data")


def example_3_all_indices():
    """Example 3: Fetch data for all indices."""
    print("\n" + "="*70)
    print("EXAMPLE 3: All Indices, Single Timeframe")
    print("="*70)

    fetcher = IntradayDataFetcher()

    # Fetch all indices
    all_results = fetcher.fetch_all_data(
        symbols=['nifty50', 'banknifty', 'sensex'],
        timeframes=['15min'],
        days_back=60
    )

    # Generate summary
    summary = fetcher.get_summary(all_results)
    print("\nSummary Report:")
    print(summary.to_string(index=False))


def example_4_custom_date_range():
    """Example 4: Using custom date ranges."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Custom Date Range")
    print("="*70)

    # Initialize components
    data_source = YahooFinanceSource(max_retries=3, retry_delay=2)

    # Define custom date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=14)

    print(f"Fetching data from {start_date.date()} to {end_date.date()}")

    # Fetch data directly using data source
    df = data_source.fetch_intraday_data(
        symbol='nifty50',
        interval='5min',
        start_date=start_date,
        end_date=end_date
    )

    if df is not None:
        print(f"\n✓ Fetched {len(df)} rows")
        print(f"\nData info:")
        print(df.info())
    else:
        print("\n✗ No data fetched")


def example_5_data_validation():
    """Example 5: Data validation and quality checks."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Data Validation and Quality Checks")
    print("="*70)

    fetcher = IntradayDataFetcher()
    file_manager = FileManager()

    # Fetch data
    results = fetcher.fetch_symbol_data(
        symbol='sensex',
        timeframes=['5min'],
        days_back=30,
        save_data=False  # Don't save, just validate
    )

    if results['5min'] is not None:
        df = results['5min']

        print(f"\n📊 Dataset Statistics:")
        print(f"   Total rows: {len(df)}")
        print(f"   Date range: {df['datetime'].iloc[0]} to {df['datetime'].iloc[-1]}")
        print(f"   Memory usage: {df.memory_usage(deep=True).sum() / 1024:.2f} KB")

        print(f"\n📈 Price Statistics:")
        print(df[['open', 'high', 'low', 'close']].describe())

        print(f"\n✓ Data Validation:")
        is_valid = file_manager.validate_dataframe(df)
        if is_valid:
            print("   All validation checks passed!")
        else:
            print("   Some validation issues found (check logs)")

        # Check for data quality
        print(f"\n🔍 Quality Checks:")
        print(f"   Null values: {df.isnull().sum().sum()}")
        print(f"   Duplicate timestamps: {df['datetime'].duplicated().sum()}")

        # OHLC validation
        invalid_ohlc = (
            (df['high'] < df['low']) |
            (df['high'] < df['open']) |
            (df['high'] < df['close']) |
            (df['low'] > df['open']) |
            (df['low'] > df['close'])
        ).sum()
        print(f"   Invalid OHLC rows: {invalid_ohlc}")


def example_6_loading_saved_data():
    """Example 6: Loading and analyzing saved data."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Loading and Analyzing Saved Data")
    print("="*70)

    file_manager = FileManager()

    # Get existing files
    existing_files = file_manager.get_existing_files('nifty50', '5min')

    if existing_files:
        print(f"\nFound {len(existing_files)} existing file(s) for NIFTY 50 5-minute data:")

        for file_path in existing_files:
            print(f"\n  📁 {file_path.name}")

            # Load data
            df = file_manager.load_data(file_path)

            if df is not None:
                print(f"     Rows: {len(df)}")
                print(f"     Date range: {df['datetime'].iloc[0]} to {df['datetime'].iloc[-1]}")
                print(f"     File size: {file_path.stat().st_size / 1024:.2f} KB")

                # Calculate some basic statistics
                avg_volume = df['volume'].mean() if 'volume' in df.columns else 0
                price_range = df['high'].max() - df['low'].min()

                print(f"     Avg volume: {avg_volume:,.0f}")
                print(f"     Price range: {price_range:.2f}")
    else:
        print("\n⚠️  No existing files found. Run the data collector first:")
        print("   python src/main.py --symbols nifty50 --timeframes 5min")


def main():
    """Run all examples."""
    print("\n" + "="*70)
    print(" INDIAN MARKET DATA COLLECTOR - EXAMPLE USAGE SCRIPT")
    print(" Educational purposes only")
    print("="*70)

    # Setup logging
    setup_logger(name="example_script", log_to_file=False)

    try:
        # Run examples
        print("\nThis script demonstrates various usage patterns.")
        print("Each example is independent and can be run separately.\n")

        # Example 1: Basic usage
        example_1_basic_usage()

        # Example 2: Multiple timeframes
        example_2_multiple_timeframes()

        # Example 3: All indices
        example_3_all_indices()

        # Example 4: Custom date range
        example_4_custom_date_range()

        # Example 5: Data validation
        example_5_data_validation()

        # Example 6: Loading saved data
        example_6_loading_saved_data()

        print("\n" + "="*70)
        print("✅ ALL EXAMPLES COMPLETED")
        print("="*70)
        print("\nNext steps:")
        print("1. Check the 'data/' directory for saved CSV files")
        print("2. Review the README.md for detailed documentation")
        print("3. Run 'python src/main.py --help' for command-line options")
        print("4. Customize the fetcher for your specific needs")
        print("\n")

    except KeyboardInterrupt:
        print("\n\n⚠️  Examples interrupted by user")

    except Exception as e:
        print(f"\n\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
