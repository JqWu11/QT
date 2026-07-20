"""
Usage Guide: MA Crossover Strategy

This guide shows how to use the strategy with real market data
"""

from simple_ma_crossover import MACrossoverStrategy
import pandas as pd
import yfinance as yf

# OPTION 1: Use the built-in example (no dependencies needed)
# Just run: python simple_ma_crossover.py

# OPTION 2: Backtest with real data from Yahoo Finance
def backtest_with_real_data(ticker='AAPL', start='2023-01-01', end='2024-01-01'):
    """
    Backtest strategy with real stock data
    
    Args:
        ticker: Stock ticker symbol (e.g., 'AAPL', 'MSFT', 'SPY')
        start: Start date (YYYY-MM-DD)
        end: End date (YYYY-MM-DD)
    """
    # Download data
    print(f"Downloading {ticker} data from {start} to {end}...")
    data = yf.download(ticker, start=start, end=end)
    
    # Run backtest
    strategy = MACrossoverStrategy(
        data,
        fast_ma=10,
        slow_ma=30,
        rsi_period=14,
        initial_capital=10000
    )
    
    results = strategy.backtest()
    stats = strategy.get_performance_stats()
    
    # Print results
    print("\n" + "=" * 70)
    print(f"BACKTEST RESULTS - {ticker} ({start} to {end})")
    print("=" * 70)
    print(f"\nInitial Capital: ${strategy.initial_capital:,.2f}")
    print(f"Final Capital: ${stats['Final Capital']:,.2f}")
    print(f"Total Return: ${stats['Total Return $']:,.2f} ({stats['Total Return %']:.2f}%)")
    print(f"\nTotal Trades: {stats['Total Trades']}")
    print(f"Buy Trades: {stats['Buy Trades']}")
    print(f"Sell Trades: {stats['Sell Trades']}")
    print(f"Winning Trades: {stats['Winning Trades']}")
    print(f"Losing Trades: {stats['Losing Trades']}")
    print(f"Win Rate: {stats['Win Rate %']:.2f}%")
    
    print("\n" + "=" * 70)
    print("RECENT TRADES (Last 10):")
    print("=" * 70)
    for trade in strategy.trades[-10:]:
        profit_str = f"${trade.get('Profit', 0):,.2f}" if 'Profit' in trade else "N/A"
        print(f"{trade['Date'].strftime('%Y-%m-%d')} | {trade['Type']:4s} | ${trade['Price']:,.2f} | {profit_str}")
    
    return results, stats, strategy


# OPTION 3: Customize parameters
def backtest_with_custom_params(ticker='SPY', fast_ma=5, slow_ma=20, rsi_period=14):
    """
    Backtest with custom moving average periods
    
    Args:
        ticker: Stock ticker
        fast_ma: Fast MA period (lower = more trades, higher sensitivity)
        slow_ma: Slow MA period (higher = more stable, fewer false signals)
        rsi_period: RSI period (14 is standard)
    """
    data = yf.download(ticker, start='2023-01-01', end='2024-01-01')
    
    strategy = MACrossoverStrategy(
        data,
        fast_ma=fast_ma,
        slow_ma=slow_ma,
        rsi_period=rsi_period,
        initial_capital=10000
    )
    
    results = strategy.backtest()
    stats = strategy.get_performance_stats()
    
    print(f"Strategy: Fast MA={fast_ma}, Slow MA={slow_ma}, RSI={rsi_period}")
    print(f"Return: {stats['Total Return %']:.2f}% | Win Rate: {stats['Win Rate %']:.2f}% | Trades: {stats['Total Trades']}")
    
    return results, stats


# OPTION 4: Compare multiple parameter sets
def optimize_parameters(ticker='AAPL'):
    """
    Test different parameter combinations to find the best ones
    """
    data = yf.download(ticker, start='2023-01-01', end='2024-01-01')
    
    fast_ma_options = [5, 10, 15]
    slow_ma_options = [20, 30, 50]
    
    results_df = []
    
    print(f"\nOptimizing {ticker}...\n")
    print(f"{'Fast MA':<10} {'Slow MA':<10} {'Return %':<15} {'Win Rate %':<15} {'Trades':<10}")
    print("-" * 60)
    
    for fast_ma in fast_ma_options:
        for slow_ma in slow_ma_options:
            if fast_ma >= slow_ma:  # Skip invalid combinations
                continue
                
            strategy = MACrossoverStrategy(data, fast_ma=fast_ma, slow_ma=slow_ma)
            strategy.backtest()
            stats = strategy.get_performance_stats()
            
            results_df.append({
                'Fast MA': fast_ma,
                'Slow MA': slow_ma,
                'Return %': stats['Total Return %'],
                'Win Rate %': stats['Win Rate %'],
                'Trades': stats['Total Trades']
            })
            
            print(f"{fast_ma:<10} {slow_ma:<10} {stats['Total Return %']:>13.2f}% {stats['Win Rate %']:>13.2f}% {stats['Total Trades']:>10}")
    
    # Find best performing combination
    best = max(results_df, key=lambda x: x['Return %'])
    print(f"\nBest combination: Fast MA={best['Fast MA']}, Slow MA={best['Slow MA']} (Return: {best['Return %']:.2f}%)")
    
    return results_df


# Example runs
if __name__ == "__main__":
    # Uncomment the one you want to run:
    
    # 1. Run the built-in example with simulated data:
    # python simple_ma_crossover.py
    
    # 2. Backtest real stock data:
    # backtest_with_real_data('AAPL', '2023-01-01', '2024-01-01')
    
    # 3. Test custom parameters:
    # backtest_with_custom_params('SPY', fast_ma=5, slow_ma=20)
    
    # 4. Optimize parameters (find best combination):
    # optimize_parameters('AAPL')
    
    print("Uncomment an example in __main__ to run it!")
