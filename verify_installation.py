"""
Installation verification script.

Run this script to verify that all dependencies are installed correctly
and the project structure is set up properly.

Usage:
    python verify_installation.py
"""

import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    print("Checking Python version...")
    version = sys.version_info

    if version.major == 3 and version.minor >= 8:
        print(f"  ✓ Python {version.major}.{version.minor}.{version.micro} (Compatible)")
        return True
    else:
        print(f"  ✗ Python {version.major}.{version.minor}.{version.micro} (Requires Python 3.8+)")
        return False


def check_dependencies():
    """Check if all required dependencies are installed."""
    print("\nChecking dependencies...")

    dependencies = {
        'pandas': 'pandas',
        'yfinance': 'yfinance',
        'pytz': 'pytz',
        'requests': 'requests',
        'aiohttp': 'aiohttp',
    }

    all_installed = True

    for module_name, import_name in dependencies.items():
        try:
            __import__(import_name)
            # Get version if possible
            try:
                mod = __import__(import_name)
                version = getattr(mod, '__version__', 'unknown')
                print(f"  ✓ {module_name:15s} - version {version}")
            except:
                print(f"  ✓ {module_name:15s} - installed")
        except ImportError:
            print(f"  ✗ {module_name:15s} - NOT INSTALLED")
            all_installed = False

    return all_installed


def check_project_structure():
    """Check if project structure is correct."""
    print("\nChecking project structure...")

    required_paths = [
        'src',
        'src/fetchers',
        'src/utils',
        'src/main.py',
        'src/fetchers/intraday_fetcher.py',
        'src/utils/logger.py',
        'src/utils/file_manager.py',
        'requirements.txt',
        'README.md',
    ]

    all_exist = True
    base_path = Path(__file__).parent

    for path_str in required_paths:
        path = base_path / path_str
        if path.exists():
            print(f"  ✓ {path_str}")
        else:
            print(f"  ✗ {path_str} - MISSING")
            all_exist = False

    return all_exist


def check_data_directories():
    """Check if data directories exist or can be created."""
    print("\nChecking data directories...")

    base_path = Path(__file__).parent / 'data'

    indices = ['nifty50', 'banknifty', 'sensex']
    timeframes = ['1min', '3min', '5min', '10min', '15min', 'all_available_minutes']

    all_created = True

    try:
        for index in indices:
            for timeframe in timeframes:
                dir_path = base_path / index / timeframe
                dir_path.mkdir(parents=True, exist_ok=True)

        print(f"  ✓ All data directories created/verified")
        print(f"  Location: {base_path}")

    except Exception as e:
        print(f"  ✗ Error creating directories: {e}")
        all_created = False

    return all_created


def test_imports():
    """Test importing project modules."""
    print("\nTesting project imports...")

    sys.path.append(str(Path(__file__).parent / 'src'))

    imports = [
        ('utils.logger', 'logger'),
        ('utils.file_manager', 'FileManager'),
        ('fetchers.intraday_fetcher', 'IntradayDataFetcher'),
        ('fetchers.intraday_fetcher', 'YahooFinanceSource'),
    ]

    all_imported = True

    for module_name, class_name in imports:
        try:
            module = __import__(module_name, fromlist=[class_name])
            getattr(module, class_name)
            print(f"  ✓ {module_name}.{class_name}")
        except Exception as e:
            print(f"  ✗ {module_name}.{class_name} - {e}")
            all_imported = False

    return all_imported


def test_basic_functionality():
    """Test basic functionality."""
    print("\nTesting basic functionality...")

    sys.path.append(str(Path(__file__).parent / 'src'))

    try:
        from utils.logger import logger
        logger.info("Logger test message")
        print("  ✓ Logger working")
    except Exception as e:
        print(f"  ✗ Logger failed: {e}")
        return False

    try:
        from utils.file_manager import FileManager
        fm = FileManager()
        print("  ✓ FileManager initialized")
    except Exception as e:
        print(f"  ✗ FileManager failed: {e}")
        return False

    try:
        from fetchers.intraday_fetcher import YahooFinanceSource
        source = YahooFinanceSource()
        intervals = source.get_supported_intervals()
        print(f"  ✓ YahooFinanceSource initialized ({len(intervals)} intervals supported)")
    except Exception as e:
        print(f"  ✗ YahooFinanceSource failed: {e}")
        return False

    return True


def main():
    """Run all verification checks."""
    print("="*70)
    print(" INDIAN MARKET DATA COLLECTOR - INSTALLATION VERIFICATION")
    print("="*70)

    results = []

    # Run checks
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("Project Structure", check_project_structure()))
    results.append(("Data Directories", check_data_directories()))
    results.append(("Module Imports", test_imports()))
    results.append(("Basic Functionality", test_basic_functionality()))

    # Summary
    print("\n" + "="*70)
    print(" VERIFICATION SUMMARY")
    print("="*70)

    all_passed = True
    for check_name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{check_name:25s}: {status}")
        if not passed:
            all_passed = False

    print("="*70)

    if all_passed:
        print("\n🎉 All checks passed! Installation is complete and working.")
        print("\nNext steps:")
        print("1. Run: python src/main.py --help")
        print("2. Try: python example_usage.py")
        print("3. Read: README.md for detailed documentation")
        return 0
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nTroubleshooting:")
        print("1. Install dependencies: pip install -r requirements.txt")
        print("2. Check Python version: python --version (need 3.8+)")
        print("3. Verify project structure matches README.md")
        return 1


if __name__ == "__main__":
    sys.exit(main())
