from flask import Flask, render_template, jsonify, request
from model import StockPredictor
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    """Get historical data for a given ticker"""
    ticker = request.args.get('ticker', '').upper().strip()
    
    if not ticker:
        return jsonify({
            'success': False,
            'error': 'Ticker symbol is required'
        }), 400
    
    try:
        pred = StockPredictor(ticker=ticker)
        df = pred.load_data(ticker)
        
        # Convert to list format for JSON
        historical_data = []
        for _, row in df.iterrows():
            historical_data.append({
                'date': row['Date'].strftime('%Y-%m-%d'),
                'close': float(row['Close'])
            })
        
        return jsonify({
            'historical': historical_data,
            'success': True,
            'ticker': ticker
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict')
def predict():
    """Get predictions for next 3 months (~90 days)"""
    ticker = request.args.get('ticker', '').upper().strip()
    
    if not ticker:
        return jsonify({
            'success': False,
            'error': 'Ticker symbol is required'
        }), 400
    
    try:
        pred = StockPredictor(ticker=ticker)
        dates, predictions = pred.predict_future(days=90, ticker=ticker)
        
        # Convert to list format for JSON
        prediction_data = []
        for date, price in zip(dates, predictions):
            prediction_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'close': float(price)
            })
        
        return jsonify({
            'predictions': prediction_data,
            'success': True,
            'ticker': ticker,
            'models_used': pred.models_used  # Return which models were used
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
