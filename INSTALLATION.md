# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

## Step-by-Step Installation

### 1. Navigate to Project Directory

```bash
cd "/mnt/c/Users/rsharma8.SERVER0/OneDrive - Finfutech Solutions Private Limited/data_scraping"
```

### 2. Install Python Dependencies

```bash
pip3 install -r requirements.txt
```

This will install:
- pandas (data manipulation)
- yfinance (Yahoo Finance API)
- pytz (timezone handling)
- requests (HTTP requests)
- aiohttp (async HTTP)

### 3. Verify Installation

```bash
python3 verify_installation.py
```

Expected output:
```
✓ Python Version: PASS
✓ Dependencies: PASS
✓ Project Structure: PASS
✓ Data Directories: PASS
✓ Module Imports: PASS
✓ Basic Functionality: PASS
```

### 4. Run Your First Data Collection

```bash
# Collect NIFTY 50 data for 5-minute timeframe (last 30 days)
python3 src/main.py --symbols nifty50 --timeframes 5min --days-back 30
```

### 5. Check Results

```bash
# List collected data files
ls -lh data/nifty50/5min/
```

## Quick Commands

```bash
# View all command-line options
python3 src/main.py --help

# Collect all indices, all default timeframes
python3 src/main.py

# Run example scripts
python3 example_usage.py

# Read documentation
cat README.md
cat QUICKSTART.md
```

## Troubleshooting

### Issue: ModuleNotFoundError

**Solution:**
```bash
pip3 install -r requirements.txt
```

### Issue: Permission Denied

**Solution:**
```bash
# Install for user only
pip3 install --user -r requirements.txt
```

### Issue: No Data Returned

**Cause:** Yahoo Finance limitations (1min: 7 days, 5min: 60 days)

**Solution:**
```bash
# For 1-minute data, use max 7 days
python3 src/main.py --timeframes 1min --days-back 7
```

## Next Steps

1. Read [QUICKSTART.md](QUICKSTART.md) for usage examples
2. Read [README.md](README.md) for comprehensive documentation
3. Read [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for architecture overview
4. Explore [example_usage.py](example_usage.py) for code examples

---

**Ready to collect market data! 🚀**
