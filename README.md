# Stock Price Prediction Website

A beautiful web application that uses machine learning (LSTM neural network) to predict stock prices for any ticker symbol for the next month based on historical data.

## Features

- 📈 Interactive chart showing historical and predicted prices
- 🔍 Enter any stock ticker symbol (e.g., AAPL, MSFT, TSLA, GOOGL)
- 🤖 **Prophet Model** - Facebook's advanced time series forecasting tool
- 📊 Real-time statistics (current price, predicted price, expected change, models used)
- 🎨 Modern, responsive UI with gradient design
- ⚡ Automatic data fetching from Yahoo Finance (uses entire stock history)
- 📉 Predicts the next 90 days (3 months) of stock prices

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

**Note on Prophet**: Prophet is required for this application. If you encounter installation issues:
- On Windows, you may need to install Visual C++ Build Tools first
- See Prophet installation guide: https://facebook.github.io/prophet/docs/installation.html

## Usage

1. Run the Flask application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Enter any stock ticker symbol (e.g., AAPL, MSFT, TSLA) and click "Predict"

## How It Works

- The application fetches **all available historical data** from Yahoo Finance (not just 1 year)
- Uses **Prophet** - Facebook's time series forecasting tool:
  - Handles trends, seasonality (weekly and yearly), and changepoints automatically
  - Optimized parameters based on data length
  - Uses linear growth model for stock price forecasting
- The model is trained on the **last 20 years** of daily closing prices (or all available data if less than 20 years)
- Prophet automatically detects patterns, trends, and seasonal effects in the data
- It predicts the next **90 days (3 months)** of stock prices
- The model adapts changepoint detection based on the length of historical data

## Disclaimer

⚠️ **This is a machine learning prediction and should not be considered as financial advice.** Stock prices are influenced by many factors and past performance does not guarantee future results.

## Technologies Used

- **Backend**: Flask (Python)
- **Machine Learning**: TensorFlow/Keras (LSTM)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Chart.js with date-fns adapter
- **Data Processing**: Pandas, NumPy, Scikit-learn
