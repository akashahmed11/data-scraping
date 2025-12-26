# Contributing to Indian Market Data Collector

Thank you for your interest in contributing to this educational project! 🎓

---

## 🎯 Project Goals

This is an **educational project** designed to:

- Help developers learn about financial data collection
- Demonstrate clean Python architecture
- Provide tools for market data analysis learning
- Share knowledge with the community

**Remember:** This is for education only, not for live trading or commercial use.

---

## 🤝 How to Contribute

We welcome contributions in the following areas:

### 1. Code Contributions

**Good contributions:**
- Bug fixes
- Performance improvements
- Better error handling
- Code documentation
- Type hint improvements
- Test coverage
- New data sources (with proper licensing)
- Additional timeframe support
- Data validation enhancements

**Please avoid:**
- Trading strategies or signals
- Live trading features
- Anything that encourages commercial use
- Removing safety warnings or disclaimers

### 2. Documentation

- Fixing typos or errors
- Improving explanations
- Adding examples
- Translating documentation
- Creating tutorials

### 3. Testing

- Writing unit tests
- Integration testing
- Reporting bugs
- Validating data accuracy

### 4. Ideas and Discussion

- Opening issues for bugs
- Suggesting improvements
- Discussing architecture
- Sharing educational use cases

---

## 📋 Contribution Guidelines

### Before You Start

1. **Read the documentation:**
   - README.md
   - DISCLAIMER.md
   - LICENSE

2. **Check existing issues:**
   - Avoid duplicate work
   - Comment on issues you'd like to work on

3. **Understand the scope:**
   - This is an educational project
   - Keep changes aligned with learning goals

### Making Changes

1. **Fork the repository**

2. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Follow code style:**
   - Use type hints
   - Write docstrings
   - Follow PEP 8
   - Keep functions focused and modular

4. **Test your changes:**
   ```bash
   python verify_installation.py
   python example_usage.py
   ```

5. **Commit with clear messages:**
   ```bash
   git commit -m "Add: Clear description of what you added"
   git commit -m "Fix: What bug you fixed"
   git commit -m "Improve: What you improved"
   ```

6. **Push to your fork:**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request:**
   - Describe what you changed and why
   - Reference any related issues
   - Explain how you tested it

---

## 🎨 Code Style

### Python Style

- **PEP 8** compliance
- **Type hints** for all functions
- **Docstrings** for all modules, classes, and functions
- **Clear variable names** (no single letters except in loops)
- **Comments** for complex logic

### Example:

```python
def fetch_data(
    symbol: str,
    timeframe: str,
    days_back: int = 30
) -> Optional[pd.DataFrame]:
    """
    Fetch market data for a given symbol and timeframe.

    Args:
        symbol: Index symbol (e.g., 'nifty50')
        timeframe: Time interval (e.g., '5min')
        days_back: Number of days to look back

    Returns:
        DataFrame with OHLCV data, or None if fetch failed
    """
    # Implementation here
    pass
```

### File Organization

- Keep modules focused (single responsibility)
- Use meaningful file and folder names
- Update `__init__.py` when adding modules

---

## 🧪 Testing

### Manual Testing

1. Run verification script:
   ```bash
   python verify_installation.py
   ```

2. Run examples:
   ```bash
   python example_usage.py
   ```

3. Test with different parameters:
   ```bash
   python src/main.py --symbols nifty50 --timeframes 5min --days-back 7
   ```

### Automated Testing (Future)

We welcome contributions to add:
- Unit tests with pytest
- Integration tests
- CI/CD workflows

---

## 🐛 Reporting Bugs

### Before Reporting

1. Check if the bug was already reported
2. Try to reproduce it consistently
3. Test with the latest version

### Bug Report Template

```markdown
**Bug Description:**
A clear description of what the bug is.

**Steps to Reproduce:**
1. Run command '...'
2. See error '...'

**Expected Behavior:**
What you expected to happen.

**Actual Behavior:**
What actually happened.

**Environment:**
- OS: [e.g., Windows 10, Ubuntu 22.04]
- Python version: [e.g., 3.10.5]
- Package versions: [run `pip list`]

**Logs:**
```
Paste relevant logs here
```

**Additional Context:**
Any other information that might be helpful.
```

---

## 💡 Suggesting Enhancements

### Enhancement Template

```markdown
**Feature Description:**
Clear description of the enhancement.

**Use Case:**
How would this help with learning/education?

**Proposed Implementation:**
Ideas on how it could be implemented.

**Alternatives Considered:**
Other approaches you thought about.

**Educational Value:**
How does this enhance the learning experience?
```

---

## 🚫 What We Won't Accept

To maintain the educational focus, we will **NOT** accept:

❌ Live trading features
❌ Trading signals or strategies
❌ Removal of safety warnings
❌ Commercial features
❌ Anything that violates data provider ToS
❌ Malicious code
❌ Poorly documented code
❌ Code without type hints
❌ Breaking changes without discussion

---

## 📜 Legal Requirements

### For All Contributors

1. **You agree that:**
   - Your contributions are your original work
   - You have the right to contribute the code
   - Your contributions will be licensed under MIT License
   - You've read and agree to the DISCLAIMER.md

2. **For data source contributions:**
   - Ensure proper licensing
   - Verify ToS compliance
   - Add appropriate disclaimers
   - Document any limitations

3. **Maintain disclaimers:**
   - Don't remove educational-only warnings
   - Keep data source attributions
   - Preserve liability disclaimers

---

## 🌟 Recognition

Contributors will be:
- Listed in a CONTRIBUTORS.md file (if we create one)
- Credited in commit history
- Acknowledged in release notes

---

## 📞 Questions?

- **Technical questions:** Open an issue with the "question" label
- **Bug reports:** Open an issue with the "bug" label
- **Feature requests:** Open an issue with the "enhancement" label

---

## 🎓 Learning Resources

For contributors new to:

**Python:**
- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)

**Pandas:**
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [10 Minutes to Pandas](https://pandas.pydata.org/docs/user_guide/10min.html)

**Git & GitHub:**
- [Git Handbook](https://guides.github.com/introduction/git-handbook/)
- [GitHub Flow](https://guides.github.com/introduction/flow/)

**Financial Data:**
- [NSE India](https://www.nseindia.com/)
- [BSE India](https://www.bseindia.com/)

---

## ✅ Contribution Checklist

Before submitting a PR:

- [ ] Code follows PEP 8 style guide
- [ ] All functions have type hints
- [ ] All functions have docstrings
- [ ] Code is well-commented
- [ ] Tested manually with verify_installation.py
- [ ] Tested with example_usage.py
- [ ] No breaking changes (or discussed first)
- [ ] Educational disclaimers intact
- [ ] Commit messages are clear
- [ ] PR description is complete

---

## 🙏 Thank You!

Every contribution helps make this project better for learners worldwide. Thank you for:

- Taking time to contribute
- Helping others learn
- Maintaining code quality
- Respecting the educational mission

**Happy coding and learning! 🚀📊🎓**
