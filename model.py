import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import yfinance as yf
import warnings
warnings.filterwarnings('ignore')

# Try importing Prophet
try:
    from prophet import Prophet
    PROPHET_AVAILABLE = True
except ImportError:
    PROPHET_AVAILABLE = False
    raise ImportError("Prophet is required. Install with: pip install prophet")

class StockPredictor:
    def __init__(self, ticker=None):
        self.ticker = ticker
        self.current_ticker = None
        self.prophet_model = None
        self.models_used = []  # Track which models are being used
        
    def fetch_stock_data(self, ticker):
        """Fetch stock data from Yahoo Finance, limited to last 10 years"""
        try:
            stock = yf.Ticker(ticker)
            # Get all available historical data
            df = stock.history(period="max")
            
            if df.empty:
                raise ValueError(f"No data found for ticker {ticker}")
            
            # Reset index to make Date a column
            df.reset_index(inplace=True)
            
            # Rename columns to match expected format
            if 'Date' not in df.columns and 'Datetime' in df.columns:
                df.rename(columns={'Datetime': 'Date'}, inplace=True)
            
            # Ensure we have Close price
            if 'Close' not in df.columns:
                raise ValueError("No Close price data available")
            
            # Sort by date
            df = df.sort_values('Date')
            df = df.reset_index(drop=True)
            
            # Limit to last 10 years if data spans more than 10 years
            end_date = df['Date'].max()
            start_date = end_date - timedelta(days=365 * 10)  # 10 years
            
            # Filter to last 10 years
            df = df[df['Date'] >= start_date].copy()
            df = df.reset_index(drop=True)
            
            # Keep only Date and Close columns
            df = df[['Date', 'Close']].copy()
            
            # Remove timezone if present (Prophet doesn't support timezone-aware datetimes)
            if df['Date'].dtype == 'datetime64[ns, UTC]' or hasattr(df['Date'].dtype, 'tz'):
                df['Date'] = pd.to_datetime(df['Date']).dt.tz_localize(None)
            elif hasattr(df['Date'].iloc[0], 'tz') and df['Date'].iloc[0].tz is not None:
                df['Date'] = df['Date'].dt.tz_localize(None)
            
            return df
        except Exception as e:
            raise ValueError(f"Error fetching data for {ticker}: {str(e)}")
        
    def load_data(self, ticker=None):
        """Load and prepare the stock data"""
        if ticker is None:
            ticker = self.ticker
        
        if ticker is None:
            raise ValueError("Ticker symbol is required")
        
        df = self.fetch_stock_data(ticker)
        self.current_ticker = ticker
        return df
    
    def train_prophet(self, ticker=None):
        """Train Prophet model with improved settings"""
        if not PROPHET_AVAILABLE:
            raise ImportError("Prophet is required. Install with: pip install prophet")
        
        df = self.load_data(ticker)
        
        # Prepare data for Prophet (requires 'ds' and 'y' columns)
        # Ensure dates are timezone-naive (Prophet doesn't support timezone-aware datetimes)
        dates = pd.to_datetime(df['Date'])
        if dates.dt.tz is not None:
            dates = dates.dt.tz_localize(None)
        
        prophet_df = pd.DataFrame({
            'ds': dates,
            'y': df['Close']
        })
        
        # Determine optimal parameters based on data length
        data_length_days = (df['Date'].max() - df['Date'].min()).days
        
        # Adjust changepoints based on data length
        if data_length_days > 2000:  # More than ~5.5 years
            n_changepoints = 30
        elif data_length_days > 1000:  # More than ~2.7 years
            n_changepoints = 25
        else:
            n_changepoints = 20
        
        # Create and fit Prophet model with optimized parameters
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=True,
            yearly_seasonality=True,  # Enable yearly seasonality
            changepoint_prior_scale=0.05,  # More conservative changepoints
            seasonality_prior_scale=10.0,
            changepoint_range=0.95,  # Use 95% of data for trend
            n_changepoints=n_changepoints,
            interval_width=0.8,
            growth='linear'  # Use linear growth model
        )
        
        try:
            model.fit(prophet_df)
            self.prophet_model = model
            self.models_used = ['Prophet']
            return model
        except Exception as e:
            raise ValueError(f"Prophet training failed: {e}")
    
    def predict_prophet(self, days=90):
        """Predict using Prophet model"""
        if self.prophet_model is None or not PROPHET_AVAILABLE:
            raise ValueError("Prophet model not trained. Call train_prophet() first.")
        
        try:
            future = self.prophet_model.make_future_dataframe(periods=days)
            forecast = self.prophet_model.predict(future)
            
            # Get only the future predictions
            predictions = forecast['yhat'].tail(days).values
            
            # Ensure non-negative
            predictions = np.maximum(predictions, 0.01)
            
            return predictions
        except Exception as e:
            raise ValueError(f"Prophet prediction failed: {e}")
    
    def predict_future(self, days=90, ticker=None):
        """Predict future stock prices using Prophet"""
        # Train Prophet model
        self.train_prophet(ticker)
        
        # Get predictions
        predictions = self.predict_prophet(days)
        
        # Generate future dates (business days only)
        df = self.load_data(ticker)
        last_date = df['Date'].iloc[-1]
        future_dates = pd.bdate_range(start=last_date + timedelta(days=1), periods=days)
        
        # Ensure we have the same number of dates as predictions
        if len(future_dates) > len(predictions):
            future_dates = future_dates[:len(predictions)]
        elif len(future_dates) < len(predictions):
            additional_days = len(predictions) - len(future_dates)
            last_future_date = future_dates[-1]
            additional_dates = pd.bdate_range(start=last_future_date + timedelta(days=1), periods=additional_days)
            future_dates = future_dates.union(additional_dates)
        
        return list(future_dates[:len(predictions)]), predictions

if __name__ == '__main__':
    predictor = StockPredictor()
    dates, predictions = predictor.predict_future(90, 'AAPL')
    print("Predictions generated successfully!")
    print(f"Models used: {', '.join(predictor.models_used)}")
    print(f"First prediction: ${predictions[0]:.2f}")
    print(f"Last prediction: ${predictions[-1]:.2f}")
