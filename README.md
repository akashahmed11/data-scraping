# Indian Market Data Collector

**Educational-Only Market Data Collection Project**

A clean, modular Python project for collecting historical intraday minute-level data for major Indian stock market indices.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Educational](https://img.shields.io/badge/Purpose-Educational-green.svg)](DISCLAIMER.md)
[![Data Source](https://img.shields.io/badge/Data-Yahoo%20Finance-purple.svg)](https://finance.yahoo.com)

---

## 📋 Important Legal Documents

**PLEASE READ BEFORE USING:**

- 📄 **[LICENSE](LICENSE)** - MIT License with data usage terms
- ⚠️ **[DISCLAIMER.md](DISCLAIMER.md)** - Comprehensive legal disclaimer and terms
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute to this project

---

## ⚠️ IMPORTANT DISCLAIMER

**This project is strictly for EDUCATIONAL, RESEARCH, and ACADEMIC purposes only.**

- NOT intended for commercial use
- NOT intended for live trading or investment decisions
- Data may be incomplete, delayed, or inaccurate
- Always verify data from official sources before any financial decisions
- Use at your own risk

By using this software, you acknowledge that:
1. Market data collection must comply with data provider's Terms of Service
2. You are responsible for ensuring your usage complies with applicable laws
3. The authors assume no liability for any financial losses
4. This is a learning tool, not a production trading system

---

## 📊 Supported Indices

This project collects data for the following Indian market indices:

1. **NIFTY 50** (`^NSEI`) - NSE's benchmark index
2. **BANK NIFTY** (`^NSEBANK`) - NSE's banking sector index
3. **SENSEX** (`^BSESN`) - BSE's benchmark index

---

## 🕒 Supported Timeframes

The following minute-level timeframes are supported:

- **1 minute** (`1min`)
- **3 minutes** (`3min`) - Resampled from 1min data
- **5 minutes** (`5min`)
- **10 minutes** (`10min`) - Resampled from 5min data
- **15 minutes** (`15min`)
- **30 minutes** (`30min`)
- **60 minutes** (`60min`)

Each timeframe is stored in separate CSV files for organized data management.

---

## 📁 Project Structure

```
project_root/
│
├── data/                          # All collected data (auto-created)
│   ├── nifty50/
│   │   ├── 1min/
│   │   ├── 3min/
│   │   ├── 5min/
│   │   ├── 10min/
│   │   ├── 15min/
│   │   └── all_available_minutes/
│   │
│   ├── banknifty/
│   │   ├── 1min/
│   │   ├── 3min/
│   │   ├── 5min/
│   │   ├── 10min/
│   │   ├── 15min/
│   │   └── all_available_minutes/
│   │
│   └── sensex/
│       ├── 1min/
│       ├── 3min/
│       ├── 5min/
│       ├── 10min/
│       ├── 15min/
│       └── all_available_minutes/
│
├── src/                           # Source code
│   ├── fetchers/
│   │   ├── __init__.py
│   │   └── intraday_fetcher.py   # Data fetching logic
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── logger.py              # Logging utilities
│   │   └── file_manager.py        # File I/O operations
│   ├── __init__.py
│   └── main.py                    # Main orchestration script
│
├── logs/                          # Log files (auto-created)
├── requirements.txt               # Python dependencies
└── README.md                      # This file
```

---

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection for data fetching

### Step 1: Clone or Download

```bash
cd /path/to/your/project
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- `pandas` - Data manipulation
- `yfinance` - Yahoo Finance API client
- `pytz` - Timezone handling
- `requests` - HTTP requests
- `aiohttp` - Async HTTP requests
- `pydantic` - Data validation

---

## 💻 Usage

### Basic Usage

Fetch all indices with all default timeframes:

```bash
python src/main.py
```

### Advanced Options

#### Fetch Specific Symbols

```bash
# Only NIFTY 50 and BANK NIFTY
python src/main.py --symbols nifty50 banknifty

# Only SENSEX
python src/main.py --symbols sensex
```

#### Fetch Specific Timeframes

```bash
# Only 1min and 5min data
python src/main.py --timeframes 1min 5min

# Only 15min data for all indices
python src/main.py --timeframes 15min
```

#### Customize Date Range

```bash
# Last 30 days (default is 60)
python src/main.py --days-back 30

# Last 7 days (useful for 1min data)
python src/main.py --timeframes 1min --days-back 7
```

#### Combine Options

```bash
# NIFTY 50 only, 1min and 5min, last 7 days
python src/main.py --symbols nifty50 --timeframes 1min 5min --days-back 7
```

#### Enable Verbose Logging

```bash
python src/main.py --verbose
```

#### Custom Output Directory

```bash
python src/main.py --output-dir /path/to/custom/data/folder
```

### Command Line Help

```bash
python src/main.py --help
```

---

## 📈 Data Format

All data is saved in CSV format with the following standardized columns:

| Column     | Type      | Description                                    |
|------------|-----------|------------------------------------------------|
| `datetime` | string    | ISO 8601 format, timezone-aware IST            |
| `open`     | float     | Opening price                                  |
| `high`     | float     | Highest price in the interval                  |
| `low`      | float     | Lowest price in the interval                   |
| `close`    | float     | Closing price                                  |
| `volume`   | int       | Trading volume (if available)                  |
| `symbol`   | string    | Index symbol (nifty50, banknifty, sensex)      |
| `timeframe`| string    | Timeframe (1min, 5min, etc.)                   |

### Example CSV Content

```csv
datetime,open,high,low,close,volume,symbol,timeframe
2024-01-15 09:15:00+0530,21500.50,21520.75,21495.25,21510.00,1234567,nifty50,1min
2024-01-15 09:16:00+0530,21510.00,21530.50,21505.00,21525.25,1345678,nifty50,1min
```

---

## 🔧 How It Works

### Data Source

This project uses **Yahoo Finance** as the primary free data source via the `yfinance` library.

#### Yahoo Finance Limitations

Yahoo Finance free tier has important limitations:

- **1-minute data**: Available for the **last 7 days only**
- **5-minute and 15-minute data**: Available for the **last 60 days**
- Historical data beyond these periods is not available for free
- Data may have gaps, especially during market holidays or low-volume periods
- No official SLA or data quality guarantees

### Data Fetching Process

1. **Symbol Mapping**: Our standard symbols are mapped to Yahoo Finance tickers
   - `nifty50` → `^NSEI`
   - `banknifty` → `^NSEBANK`
   - `sensex` → `^BSESN`

2. **Interval Handling**: Some intervals are resampled from finer data
   - `3min` is resampled from `1min` data
   - `10min` is resampled from `5min` data

3. **Data Validation**: Each DataFrame is validated for:
   - Required columns
   - Data types
   - OHLC relationships (High ≥ Low, etc.)
   - Null values

4. **File Organization**: Data is automatically saved to the correct directory structure

5. **Retry Logic**: Failed requests are retried up to 3 times with exponential backoff

6. **Rate Limiting**: 1-second delay between requests to respect API limits

---

## 🏗️ Architecture

### Modular Design

The project is built with clean separation of concerns:

1. **Data Sources** (`src/fetchers/intraday_fetcher.py`)
   - Abstract base class `DataSourceBase` for easy extension
   - `YahooFinanceSource` implementation
   - Easy to add new data sources (NSE API, paid providers, etc.)

2. **File Management** (`src/utils/file_manager.py`)
   - Handles all file I/O operations
   - Data validation and integrity checks
   - Standardized file naming
   - No hardcoded paths (uses `pathlib`)

3. **Logging** (`src/utils/logger.py`)
   - Colored console output
   - File-based logging
   - Configurable log levels

4. **Orchestration** (`src/main.py`)
   - Command-line interface
   - Progress tracking
   - Summary reports

### Extensibility

Adding a new data source is simple:

```python
from src.fetchers.intraday_fetcher import DataSourceBase

class MyCustomSource(DataSourceBase):
    def fetch_intraday_data(self, symbol, interval, start_date, end_date):
        # Your implementation
        pass

    def get_supported_intervals(self):
        return ['1min', '5min', '15min']

# Use it
fetcher = IntradayDataFetcher(data_source=MyCustomSource())
```

---

## 📊 Output Files

### Data Files

Filenames follow this pattern:

```
{symbol}_{timeframe}_{start_date}_{end_date}.csv
```

Examples:
- `nifty50_1min_20240101_20240107.csv`
- `banknifty_5min_20240101_20240201.csv`
- `sensex_15min_latest.csv`

### Summary Reports

After each run, a summary CSV is generated:

```
summary_YYYYMMDD_HHMMSS.csv
```

Contains:
- Symbol
- Timeframe
- Number of rows
- Start and end dates
- Success/failure status

---

## 🛠️ Customization

### Modify Symbols

Edit `INDICES_CONFIG` in `src/fetchers/intraday_fetcher.py`:

```python
INDICES_CONFIG = {
    'nifty50': {...},
    'banknifty': {...},
    'your_custom_index': {
        'name': 'Your Index',
        'exchange': 'NSE',
    }
}
```

### Modify Default Timeframes

Edit `STANDARD_TIMEFRAMES` in `src/fetchers/intraday_fetcher.py`:

```python
STANDARD_TIMEFRAMES = ['1min', '5min', '15min', '30min']
```

### Change Default Date Range

Modify `days_back` parameter in `main.py` or use `--days-back` flag.

---

## ⚖️ Legal Considerations

### Data Usage Rights

- **Yahoo Finance**: Review [Yahoo's Terms of Service](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html)
- Data is provided "as-is" without guarantees
- Respect rate limits and fair use policies

### Scraping Ethics

- This project uses official APIs, not web scraping
- Rate limiting is implemented to avoid server overload
- Educational use typically falls under fair use

### Trading Disclaimer

- Data is not suitable for live trading
- May contain errors, gaps, or delays
- Always use official broker data for actual trading

---

## 🐛 Troubleshooting

### Common Issues

#### 1. No Data Returned

**Problem**: Empty DataFrames or "No data returned" messages

**Solutions**:
- Check date range (Yahoo Finance limits apply)
- For 1min data, use `--days-back 7` or less
- Verify symbol names are correct
- Check internet connection

#### 2. Import Errors

**Problem**: `ModuleNotFoundError`

**Solutions**:
```bash
pip install -r requirements.txt
```

#### 3. Permission Errors

**Problem**: Cannot create directories or files

**Solutions**:
- Check write permissions in project directory
- Run with appropriate user permissions
- Use `--output-dir` to specify writable location

#### 4. Rate Limiting

**Problem**: Too many requests errors

**Solutions**:
- Built-in rate limiting should prevent this
- If issues persist, increase delay in `YahooFinanceSource`

### Debug Mode

Enable verbose logging to see detailed information:

```bash
python src/main.py --verbose
```

Check log files in `./logs/` directory for detailed error traces.

---

## 🔮 Future Enhancements

Potential improvements for this educational project:

1. **Additional Data Sources**
   - NSE official API integration
   - BSE data integration
   - Support for other free data providers

2. **Data Quality**
   - Automated data quality checks
   - Gap detection and filling
   - Outlier detection

3. **Performance**
   - Parallel downloads using async/await
   - Incremental updates (only fetch new data)
   - Caching mechanisms

4. **Analysis Tools**
   - Built-in data visualization
   - Basic technical indicators
   - Data exploration notebooks

5. **Additional Features**
   - Support for individual stocks (not just indices)
   - Options chain data
   - Fundamental data integration

---

## 📚 Resources

### Learning Materials

- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Yahoo Finance API (yfinance)](https://github.com/ranaroussi/yfinance)
- [NSE India Official](https://www.nseindia.com/)
- [BSE India Official](https://www.bseindia.com/)

### Related Projects

- [NSEpy](https://github.com/swapniljariwala/nsepy) - NSE Python library
- [jugaad-data](https://github.com/jugaad-py/jugaad-data) - Alternative NSE data

### Financial Data APIs (Paid)

- [Alpha Vantage](https://www.alphavantage.co/)
- [Polygon.io](https://polygon.io/)
- [TrueData](https://www.truedata.in/)
- [Upstox API](https://upstox.com/developer/)

---

## 🤝 Contributing

This is an educational project. Contributions for learning purposes are welcome:

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

Focus areas:
- Additional data sources
- Improved error handling
- Better documentation
- Unit tests
- Performance optimizations

---

## 📄 License

This project is released for educational purposes. Users are responsible for:
- Complying with data provider Terms of Service
- Using data ethically and legally
- Not using for unauthorized commercial purposes

---

## 🙏 Acknowledgments

- **Yahoo Finance** for providing free market data access
- **Pandas** community for excellent data tools
- **Python** community for the amazing ecosystem

---

## 📧 Support

For issues related to:
- **Code bugs**: Check logs and error messages
- **Data availability**: Contact data provider (Yahoo Finance)
- **Feature requests**: Educational contributions welcome

---

## 🎓 Educational Value

This project demonstrates:
- Clean Python architecture
- Modular design patterns
- Error handling and retry logic
- File I/O operations
- API integration
- Data validation
- Logging best practices
- Command-line interfaces

Use it to learn about:
- Financial data structures
- Time series data handling
- Data engineering workflows
- Production-grade Python code

---

**Remember: This is a learning tool. Always verify data and comply with all applicable laws and terms of service.**

**Happy Learning! 📊🎓**
