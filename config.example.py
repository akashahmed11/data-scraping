"""
Example configuration file for the market data collector.
Copy this file to config.py and customize as needed.

This file shows all available configuration options.
"""

from pathlib import Path

# ============================================================================
# DATA SOURCE CONFIGURATION
# ============================================================================

# Data source to use ('yahoo', or implement your own)
DATA_SOURCE = 'yahoo'

# Yahoo Finance specific settings
YAHOO_FINANCE_CONFIG = {
    'max_retries': 3,           # Maximum retry attempts for failed requests
    'retry_delay': 2,           # Delay in seconds between retries
    'rate_limit_delay': 1,      # Delay in seconds between requests
}

# ============================================================================
# SYMBOLS CONFIGURATION
# ============================================================================

# Indices to fetch
ENABLED_INDICES = [
    'nifty50',
    'banknifty',
    'sensex',
]

# Custom symbol mapping (if you want to add more symbols)
CUSTOM_SYMBOLS = {
    # 'niftyit': {
    #     'name': 'NIFTY IT',
    #     'yahoo_ticker': '^CNXIT',
    #     'exchange': 'NSE',
    # },
}

# ============================================================================
# TIMEFRAME CONFIGURATION
# ============================================================================

# Timeframes to fetch
ENABLED_TIMEFRAMES = [
    '1min',
    '3min',
    '5min',
    '10min',
    '15min',
]

# All available timeframes
ALL_TIMEFRAMES = [
    '1min',
    '2min',
    '3min',
    '5min',
    '10min',
    '15min',
    '30min',
    '60min',
    '90min',
]

# ============================================================================
# DATE RANGE CONFIGURATION
# ============================================================================

# Default number of days to look back
DEFAULT_DAYS_BACK = 60

# Specific date ranges for different timeframes (optional)
TIMEFRAME_DATE_RANGES = {
    '1min': 7,      # Yahoo Finance: last 7 days for 1min
    '5min': 60,     # Yahoo Finance: last 60 days for 5min
    '15min': 60,    # Yahoo Finance: last 60 days for 15min
}

# ============================================================================
# FILE STORAGE CONFIGURATION
# ============================================================================

# Base directory for data storage
DATA_DIR = Path(__file__).parent / 'data'

# Base directory for logs
LOG_DIR = Path(__file__).parent / 'logs'

# CSV file settings
CSV_CONFIG = {
    'index': False,             # Don't write DataFrame index to CSV
    'encoding': 'utf-8',        # Character encoding
    'date_format': '%Y-%m-%d %H:%M:%S%z',  # Date format in CSV
}

# File naming pattern
# Available variables: {symbol}, {timeframe}, {start_date}, {end_date}
FILE_NAME_PATTERN = '{symbol}_{timeframe}_{start_date}_{end_date}.csv'

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

# Logging level ('DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL')
LOG_LEVEL = 'INFO'

# Enable file logging
LOG_TO_FILE = True

# Log file rotation (optional)
LOG_ROTATION = {
    'max_bytes': 10 * 1024 * 1024,  # 10 MB
    'backup_count': 5,               # Keep 5 old log files
}

# ============================================================================
# DATA VALIDATION CONFIGURATION
# ============================================================================

# Validation rules
VALIDATION_CONFIG = {
    'check_ohlc_relationships': True,  # Validate High >= Low, etc.
    'check_null_values': True,          # Check for missing values
    'check_duplicates': True,           # Check for duplicate timestamps
    'allow_gaps': True,                 # Allow gaps in time series
}

# Minimum rows threshold (skip saving if below this)
MIN_ROWS_THRESHOLD = 1

# ============================================================================
# PERFORMANCE CONFIGURATION
# ============================================================================

# Enable parallel downloads (experimental)
ENABLE_PARALLEL = False

# Maximum concurrent requests (if parallel enabled)
MAX_WORKERS = 3

# Request timeout in seconds
REQUEST_TIMEOUT = 30

# ============================================================================
# ADVANCED OPTIONS
# ============================================================================

# Append to existing files instead of overwriting
APPEND_MODE = False

# Skip download if file already exists
SKIP_EXISTING = False

# Generate summary report after each run
GENERATE_SUMMARY = True

# Timezone for data (Indian Standard Time)
TIMEZONE = 'Asia/Kolkata'

# ============================================================================
# NOTIFICATION CONFIGURATION (Optional)
# ============================================================================

# Enable notifications (email, Slack, etc.)
ENABLE_NOTIFICATIONS = False

# Email notification settings (if enabled)
EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender': 'your_email@gmail.com',
    'password': 'your_password',  # Use app-specific password
    'recipients': ['recipient@example.com'],
}

# ============================================================================
# EXAMPLES OF USAGE
# ============================================================================

"""
To use this configuration in your code:

from config import (
    ENABLED_INDICES,
    ENABLED_TIMEFRAMES,
    DATA_DIR,
    LOG_LEVEL
)

# In main.py:
fetcher.fetch_all_data(
    symbols=ENABLED_INDICES,
    timeframes=ENABLED_TIMEFRAMES,
    days_back=DEFAULT_DAYS_BACK
)
"""
