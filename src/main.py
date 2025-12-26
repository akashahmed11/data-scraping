"""
Main orchestration script for Indian market data collection.

This is an EDUCATIONAL-ONLY project for learning and research purposes.
NOT intended for commercial use or live trading.

Usage:
    python src/main.py [options]

Examples:
    # Fetch all indices, all timeframes (default)
    python src/main.py

    # Fetch specific symbols
    python src/main.py --symbols nifty50 banknifty

    # Fetch specific timeframes
    python src/main.py --timeframes 1min 5min 15min

    # Customize date range
    python src/main.py --days-back 30

    # Verbose logging
    python src/main.py --verbose
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent))

from fetchers.intraday_fetcher import IntradayDataFetcher, YahooFinanceSource
from utils.logger import setup_logger, logger
from utils.file_manager import FileManager


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Fetch intraday market data for Indian indices (Educational purposes only)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument(
        '--symbols',
        nargs='+',
        default=None,
        choices=['nifty50', 'banknifty', 'sensex'],
        help='Symbols to fetch (default: all)'
    )

    parser.add_argument(
        '--timeframes',
        nargs='+',
        default=None,
        choices=['1min', '3min', '5min', '10min', '15min', '30min', '60min'],
        help='Timeframes to fetch (default: 1min 3min 5min 10min 15min)'
    )

    parser.add_argument(
        '--days-back',
        type=int,
        default=60,
        help='Number of days to fetch (default: 60). Note: Yahoo Finance limits apply.'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )

    parser.add_argument(
        '--no-save',
        action='store_true',
        help='Fetch data but do not save to files (for testing)'
    )

    parser.add_argument(
        '--output-dir',
        type=Path,
        default=None,
        help='Custom output directory for data (default: ./data)'
    )

    return parser.parse_args()


def print_banner():
    """Print welcome banner."""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        INDIAN MARKET DATA COLLECTOR (Educational Only)        ║
║                                                                ║
║  Collects intraday minute-level data for Indian indices:      ║
║    • NIFTY 50                                                  ║
║    • BANK NIFTY                                                ║
║    • SENSEX                                                    ║
║                                                                ║
║  ⚠️  FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY                ║
║  ⚠️  NOT FOR COMMERCIAL USE OR LIVE TRADING                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)


def print_summary(summary_df, elapsed_time):
    """Print execution summary."""
    print("\n" + "="*70)
    print("EXECUTION SUMMARY")
    print("="*70)

    if summary_df.empty:
        print("No data collected.")
        return

    # Group by status
    success_count = len(summary_df[summary_df['status'] == 'SUCCESS'])
    failed_count = len(summary_df[summary_df['status'] == 'FAILED'])
    total_rows = summary_df[summary_df['status'] == 'SUCCESS']['rows'].sum()

    print(f"\n✓ Successful fetches: {success_count}")
    print(f"✗ Failed fetches:     {failed_count}")
    print(f"📊 Total data rows:    {total_rows:,}")
    print(f"⏱️  Execution time:     {elapsed_time:.2f} seconds")

    print("\nDetailed breakdown:")
    print("-" * 70)
    print(summary_df.to_string(index=False))
    print("-" * 70)


def main():
    """Main execution function."""
    # Parse arguments
    args = parse_arguments()

    # Print banner
    print_banner()

    # Setup logging
    log_level = 'DEBUG' if args.verbose else 'INFO'
    import logging
    global logger
    logger = setup_logger(
        name="market_data_collector",
        log_level=logging.DEBUG if args.verbose else logging.INFO,
        log_to_file=True
    )

    # Log execution parameters
    logger.info("="*60)
    logger.info("STARTING DATA COLLECTION")
    logger.info("="*60)
    logger.info(f"Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"Symbols: {args.symbols or 'ALL'}")
    logger.info(f"Timeframes: {args.timeframes or 'DEFAULT (1min, 3min, 5min, 10min, 15min)'}")
    logger.info(f"Days Back: {args.days_back}")
    logger.info(f"Output Directory: {args.output_dir or './data'}")
    logger.info(f"Save Data: {not args.no_save}")
    logger.info("="*60)

    # Disclaimer
    logger.warning("⚠️  This is an EDUCATIONAL-ONLY project. Data is for learning purposes.")
    logger.warning("⚠️  Yahoo Finance free tier has limitations on historical intraday data:")
    logger.warning("   - 1min data: Last 7 days only")
    logger.warning("   - 5min/15min data: Last 60 days")
    logger.warning("   - Data availability may vary by symbol")

    try:
        # Initialize components
        file_manager = FileManager(base_data_dir=args.output_dir)
        data_source = YahooFinanceSource(max_retries=3, retry_delay=2)
        fetcher = IntradayDataFetcher(
            data_source=data_source,
            file_manager=file_manager
        )

        # Record start time
        start_time = datetime.now()

        # Fetch data
        results = fetcher.fetch_all_data(
            symbols=args.symbols,
            timeframes=args.timeframes,
            days_back=args.days_back
        )

        # Calculate elapsed time
        elapsed_time = (datetime.now() - start_time).total_seconds()

        # Generate summary
        summary_df = fetcher.get_summary(results)

        # Print summary
        print_summary(summary_df, elapsed_time)

        # Save summary report
        if not args.no_save:
            summary_path = Path(args.output_dir or 'data') / f"summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            summary_df.to_csv(summary_path, index=False)
            logger.info(f"\n📄 Summary report saved to: {summary_path}")

        logger.info("\n✅ DATA COLLECTION COMPLETED SUCCESSFULLY")

        return 0

    except KeyboardInterrupt:
        logger.warning("\n⚠️  Data collection interrupted by user")
        return 1

    except Exception as e:
        logger.error(f"\n❌ Fatal error during data collection: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
