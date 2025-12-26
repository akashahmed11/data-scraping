# Quick Start Guide

Get up and running with the Indian Market Data Collector in 5 minutes!

## 1. Install Dependencies

```bash
pip install -r requirements.txt
```

## 2. Run the Data Collector

### Collect All Data (Default)

```bash
python src/main.py
```

This will:
- Fetch NIFTY 50, BANK NIFTY, and SENSEX
- Download 1min, 3min, 5min, 10min, and 15min data
- Save to `./data/` directory
- Create logs in `./logs/` directory

### Quick Examples

**Get only NIFTY 50 data:**
```bash
python src/main.py --symbols nifty50
```

**Get only 5-minute and 15-minute data:**
```bash
python src/main.py --timeframes 5min 15min
```

**Get last 7 days of 1-minute data:**
```bash
python src/main.py --timeframes 1min --days-back 7
```

**Combine options:**
```bash
python src/main.py --symbols nifty50 banknifty --timeframes 5min 15min --days-back 30
```

## 3. Check Your Data

After running, check the `data/` directory:

```
data/
├── nifty50/
│   ├── 1min/
│   │   └── nifty50_1min_20240120_20240126.csv
│   ├── 5min/
│   │   └── nifty50_5min_20231120_20240126.csv
│   └── ...
├── banknifty/
└── sensex/
```

## 4. Load and Use the Data

### Python Example

```python
import pandas as pd

# Load data
df = pd.read_csv('data/nifty50/5min/nifty50_5min_20231120_20240126.csv',
                 parse_dates=['datetime'])

# View data
print(df.head())
print(f"Total rows: {len(df)}")
print(f"Date range: {df['datetime'].min()} to {df['datetime'].max()}")

# Basic analysis
print(df[['open', 'high', 'low', 'close']].describe())
```

### Output
```
                    datetime      open      high       low     close  volume  symbol timeframe
0  2023-11-20 09:15:00+0530  19500.25  19520.50  19495.00  19510.75  123456  nifty50     5min
1  2023-11-20 09:20:00+0530  19510.75  19535.25  19505.50  19528.00  145678  nifty50     5min
...
```

## 5. View Logs

Check the `logs/` directory for detailed execution logs:

```bash
cat logs/market_data_20240126_153045.log
```

## Common Use Cases

### Research & Backtesting

```bash
# Get 60 days of 5-minute data for all indices
python src/main.py --timeframes 5min --days-back 60
```

### High-Frequency Analysis

```bash
# Get latest 7 days of 1-minute data
python src/main.py --timeframes 1min --days-back 7
```

### Multi-Timeframe Analysis

```bash
# Get multiple timeframes for correlation analysis
python src/main.py --timeframes 5min 15min 30min 60min
```

## Troubleshooting

### Issue: No data returned

**Solution:** Yahoo Finance only provides limited historical intraday data:
- 1-minute: Last 7 days
- 5/15-minute: Last 60 days

Try reducing `--days-back`:
```bash
python src/main.py --timeframes 1min --days-back 7
```

### Issue: Import errors

**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: Permission denied

**Solution:** Ensure you have write permissions in the project directory.

## Next Steps

1. Read the full [README.md](README.md) for detailed documentation
2. Explore [config.example.py](config.example.py) for advanced configuration
3. Check example analysis notebooks (if available)
4. Customize data sources by extending `DataSourceBase` class

## Important Reminders

- 📚 **Educational Use Only** - Not for live trading
- ⚠️ **Data Limitations** - Yahoo Finance free tier has restrictions
- ✅ **Validate Data** - Always verify data quality before analysis
- 📖 **Terms of Service** - Comply with data provider's ToS

---

**Happy Learning! 🚀**

For detailed documentation, see [README.md](README.md)
