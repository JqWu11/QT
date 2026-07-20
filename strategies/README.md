# Trading Strategy Backtest Framework

A simple yet effective trading algorithm for backtesting strategies on historical price data.

## Quick Start

### Strategy Overview

**Moving Average Crossover with RSI Confirmation**

This is a trend-following strategy that generates trading signals based on:
- **Fast Moving Average (10-day)** - Follows recent price trends
- **Slow Moving Average (30-day)** - Identifies longer-term trends  
- **RSI (14-day)** - Confirms entry signals aren't overbought

### How It Works

```
BUY Signal:
- Fast MA crosses ABOVE Slow MA (bullish crossover)
- AND RSI < 70 (not overbought)

SELL Signal:
- Fast MA crosses BELOW Slow MA (bearish crossover)
```

## Installation

All dependencies are already installed in the virtual environment. If needed:

```bash
# Already done, but for reference:
pip install pandas numpy yfinance
```

## Usage

### Option 1: Run the Built-in Example (No Data Download Needed)

```bash
/Users/j_wu/Desktop/Files/QT/.venv/bin/python strategies/simple_ma_crossover.py
```

This runs a backtest on simulated data with 252 trading days (1 year).

### Option 2: Backtest Real Stock Data

```python
from strategies.usage_examples import backtest_with_real_data

# Backtest Apple stock from 2023-2024
backtest_with_real_data('AAPL', '2023-01-01', '2024-01-01')

# Try other tickers: MSFT, SPY, GOOGL, TSLA, etc.
backtest_with_real_data('SPY', '2022-01-01', '2024-01-01')
```

### Option 3: Custom Parameters

```python
from strategies.usage_examples import backtest_with_custom_params

# Test with different moving average periods
backtest_with_custom_params('AAPL', fast_ma=5, slow_ma=20, rsi_period=14)
```

### Option 4: Parameter Optimization

```python
from strategies.usage_examples import optimize_parameters

# Find the best parameter combination
results = optimize_parameters('AAPL')
```

## Understanding the Output

```
Initial Capital: $10,000.00          # Starting money
Final Capital: $9,997.17             # Ending money after all trades
Total Return: $-2.83 (-0.03%)        # Profit/Loss

Total Trades: 10                     # Buy + Sell trades
Buy Trades: 5                        # Entry signals
Sell Trades: 5                       # Exit signals
Winning Trades: 2                    # Trades with profit
Losing Trades: 3                     # Trades with loss
Win Rate: 40.00%                     # Percentage of winning trades
```

## Files

- **`simple_ma_crossover.py`** - Main strategy implementation
  - `MACrossoverStrategy` class - Core backtester
  - RSI calculation function
  - Performance statistics

- **`usage_examples.py`** - Example usage patterns
  - Real data backtesting
  - Parameter optimization
  - Multi-ticker comparison

## Key Concepts

### Moving Average Crossover
- **Fast MA (10)**: Responds quickly to price changes
- **Slow MA (30)**: Filters out noise, shows main trend
- **Crossover**: Signal for trend change

### RSI (Relative Strength Index)
- **Range**: 0-100
- **Overbought**: > 70 (too high, likely to pull back)
- **Oversold**: < 30 (too low, likely to bounce up)
- **Use**: Filters false signals when Fast MA crosses above Slow MA

### Why This Strategy?
1. **Simple to understand** - Just two moving averages
2. **Effective trend follower** - Catches sustained price movements
3. **RSI filter** - Reduces false signals in choppy markets
4. **Beginner-friendly** - Great for learning backtesting

## Backtesting Tips

### What to Test
- Different ticker symbols (stocks, ETFs, crypto)
- Different time periods (bull markets, bear markets, sideways)
- Different parameter combinations
- Long-term vs short-term trends

### Parameter Tuning
| Parameter | Lower Values | Higher Values |
|-----------|-------------|--------------|
| Fast MA | More trades, faster response | Fewer trades, less sensitive |
| Slow MA | More trend changes detected | Fewer false signals |
| RSI Period | More sensitive | Smoother readings |

### Realistic Expectations
- **Win rates 40-60%** are actually good (profit comes from bigger winners)
- **Results vary by market condition** - test different periods
- **Past performance ≠ future results** - especially important in real trading

## Next Steps

1. **Test different tickers**: Try `TSLA`, `GOOGL`, `IWM`, `QQQ`
2. **Optimize parameters**: Find best settings for your preferred stock
3. **Add features**: Stop losses, position sizing, multiple timeframes
4. **Forward test**: Paper trade (simulated) before real money

## Extending the Strategy

To modify the strategy, edit `MACrossoverStrategy` class:

```python
# Add stop loss
if close - entry_price < -100:  # If down $100
    sell_signal = True

# Add position sizing
shares = capital / close  # Buy as many shares as possible

# Add other indicators
self.data['MACD'] = ...
self.data['Bollinger_Band'] = ...
```

## References

- [Moving Averages Explained](https://www.investopedia.com/terms/m/movingaverage.asp)
- [RSI Indicator Guide](https://www.investopedia.com/terms/r/rsi.asp)
- [Backtesting Best Practices](https://www.investopedia.com/terms/b/backtesting.asp)

---

**Happy backtesting!** Remember: always thoroughly test strategies before using real money.
