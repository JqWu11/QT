"""
Simple Moving Average Crossover Strategy with RSI Confirmation
A beginner-friendly trading strategy for backtesting
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta


class MACrossoverStrategy:
    """
    Moving Average Crossover Strategy with RSI confirmation
    """
    
    def __init__(self, data, fast_ma=10, slow_ma=30, rsi_period=14, initial_capital=10000):
        """
        Initialize the strategy
        
        Args:
            data: DataFrame with 'Close' column and datetime index
            fast_ma: Period for fast moving average (default 10)
            slow_ma: Period for slow moving average (default 30)
            rsi_period: Period for RSI calculation (default 14)
            initial_capital: Starting capital (default 10000)
        """
        self.data = data.copy()
        self.fast_ma = fast_ma
        self.slow_ma = slow_ma
        self.rsi_period = rsi_period
        self.initial_capital = initial_capital
        self.capital = initial_capital
        self.position = 0  # 0 = no position, 1 = long position
        self.entry_price = 0
        self.trades = []  # Record all trades
        
    def calculate_rsi(self, prices, period):
        """Calculate RSI (Relative Strength Index)"""
        deltas = np.diff(prices)
        seed = deltas[:period+1]
        
        ups = seed[seed >= 0].sum() / period
        downs = -seed[seed < 0].sum() / period
        
        rs = ups / downs if downs != 0 else 0
        rsi = np.zeros_like(prices)
        rsi[:period] = 100.0 - 100.0 / (1.0 + rs)
        
        for i in range(period, len(prices)):
            delta = deltas[i-1]
            if delta > 0:
                upval = delta
                downval = 0.0
            else:
                upval = 0.0
                downval = -delta
                
            ups = (ups * (period - 1) + upval) / period
            downs = (downs * (period - 1) + downval) / period
            
            rs = ups / downs if downs != 0 else 0
            rsi[i] = 100.0 - 100.0 / (1.0 + rs)
            
        return rsi
    
    def backtest(self):
        """Run the backtest"""
        # Calculate indicators
        self.data['Fast_MA'] = self.data['Close'].rolling(window=self.fast_ma).mean()
        self.data['Slow_MA'] = self.data['Close'].rolling(window=self.slow_ma).mean()
        self.data['RSI'] = self.calculate_rsi(self.data['Close'].values, self.rsi_period)
        
        # Generate signals
        self.data['Signal'] = 0  # 0 = no action, 1 = buy, -1 = sell
        
        for i in range(1, len(self.data)):
            close = self.data['Close'].iloc[i]
            fast_ma = self.data['Fast_MA'].iloc[i]
            slow_ma = self.data['Slow_MA'].iloc[i]
            rsi = self.data['RSI'].iloc[i]
            
            fast_ma_prev = self.data['Fast_MA'].iloc[i-1]
            slow_ma_prev = self.data['Slow_MA'].iloc[i-1]
            
            # Skip if indicators not ready
            if pd.isna(fast_ma) or pd.isna(slow_ma) or pd.isna(rsi):
                continue
            
            # Buy signal: Fast MA crosses above Slow MA and RSI < 70
            if self.position == 0 and fast_ma_prev <= slow_ma_prev and fast_ma > slow_ma and rsi < 70:
                self.position = 1
                self.entry_price = close
                self.data.loc[self.data.index[i], 'Signal'] = 1
                self.trades.append({
                    'Date': self.data.index[i],
                    'Type': 'BUY',
                    'Price': close,
                    'Reason': f'MA Crossover (RSI: {rsi:.2f})'
                })
            
            # Sell signal: Fast MA crosses below Slow MA OR RSI becomes overbought
            elif self.position == 1:
                if fast_ma_prev >= slow_ma_prev and fast_ma < slow_ma:
                    profit = close - self.entry_price
                    self.capital += profit
                    self.position = 0
                    self.data.loc[self.data.index[i], 'Signal'] = -1
                    self.trades.append({
                        'Date': self.data.index[i],
                        'Type': 'SELL',
                        'Price': close,
                        'Profit': profit,
                        'Reason': 'MA Crossover'
                    })
        
        return self.data
    
    def get_performance_stats(self):
        """Calculate and return performance statistics"""
        buy_trades = [t for t in self.trades if t['Type'] == 'BUY']
        sell_trades = [t for t in self.trades if t['Type'] == 'SELL']
        
        if not sell_trades:
            return {
                'Total Trades': len(self.trades),
                'Buy Trades': len(buy_trades),
                'Sell Trades': len(sell_trades),
                'Winning Trades': 0,
                'Losing Trades': 0,
                'Win Rate': 0,
                'Total Return $': self.capital - self.initial_capital,
                'Total Return %': ((self.capital - self.initial_capital) / self.initial_capital) * 100,
                'Final Capital': self.capital
            }
        
        winning_trades = sum(1 for t in sell_trades if t.get('Profit', 0) > 0)
        losing_trades = sum(1 for t in sell_trades if t.get('Profit', 0) <= 0)
        win_rate = (winning_trades / len(sell_trades) * 100) if sell_trades else 0
        
        stats = {
            'Total Trades': len(self.trades),
            'Buy Trades': len(buy_trades),
            'Sell Trades': len(sell_trades),
            'Winning Trades': winning_trades,
            'Losing Trades': losing_trades,
            'Win Rate %': win_rate,
            'Total Return $': self.capital - self.initial_capital,
            'Total Return %': ((self.capital - self.initial_capital) / self.initial_capital) * 100,
            'Final Capital': self.capital
        }
        
        return stats


def example_backtest():
    """Example backtest with sample data"""
    # Generate sample price data (simulated stock prices)
    dates = pd.date_range(start='2023-01-01', periods=252, freq='D')
    np.random.seed(42)
    prices = 100 + np.cumsum(np.random.randn(252) * 2)
    
    # Create DataFrame
    data = pd.DataFrame({
        'Close': prices,
    }, index=dates)
    
    # Run backtest
    strategy = MACrossoverStrategy(data, fast_ma=10, slow_ma=30, initial_capital=10000)
    results = strategy.backtest()
    stats = strategy.get_performance_stats()
    
    # Print results
    print("=" * 60)
    print("BACKTEST RESULTS - MA Crossover Strategy")
    print("=" * 60)
    print(f"\nInitial Capital: ${strategy.initial_capital:,.2f}")
    print(f"Final Capital: ${stats['Final Capital']:,.2f}")
    print(f"Total Return: ${stats['Total Return $']:,.2f} ({stats['Total Return %']:.2f}%)")
    print(f"\nTotal Trades: {stats['Total Trades']}")
    print(f"Buy Trades: {stats['Buy Trades']}")
    print(f"Sell Trades: {stats['Sell Trades']}")
    print(f"Winning Trades: {stats['Winning Trades']}")
    print(f"Losing Trades: {stats['Losing Trades']}")
    print(f"Win Rate: {stats['Win Rate %']:.2f}%")
    
    print("\n" + "=" * 60)
    print("TRADE LOG (Last 10 trades):")
    print("=" * 60)
    for trade in strategy.trades[-10:]:
        print(f"{trade['Date'].strftime('%Y-%m-%d')} | {trade['Type']:4s} | ${trade['Price']:,.2f} | {trade['Reason']}")
    
    return results, stats


if __name__ == "__main__":
    results, stats = example_backtest()
