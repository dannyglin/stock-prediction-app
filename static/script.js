let stockChart = null;
let currentTicker = '';

// Format currency
function formatCurrency(value) {
    return '$' + value.toFixed(2);
}

// Format percentage
function formatPercent(value) {
    const sign = value >= 0 ? '+' : '';
    return sign + value.toFixed(2) + '%';
}

// Handle form submission
function handleSubmit(event) {
    event.preventDefault();
    const ticker = document.getElementById('tickerInput').value.trim().toUpperCase();
    
    if (!ticker) {
        alert('Please enter a stock ticker symbol');
        return;
    }
    
    currentTicker = ticker;
    loadData(ticker);
}

// Load data and predictions
async function loadData(ticker) {
    // Show loading state
    document.getElementById('tickerForm').style.display = 'none';
    document.getElementById('loading').style.display = 'block';
    document.getElementById('content').style.display = 'none';
    document.getElementById('error').style.display = 'none';
    document.getElementById('loadingText').textContent = `Fetching full history for ${ticker} and training ensemble models...`;
    
    try {
        // Load historical data
        const historicalResponse = await fetch(`/api/data?ticker=${encodeURIComponent(ticker)}`);
        const historicalData = await historicalResponse.json();
        
        if (!historicalData.success) {
            throw new Error(historicalData.error || 'Failed to fetch historical data');
        }
        
        document.getElementById('loadingText').textContent = 'Training ensemble models and generating 3-month predictions...';
        
        // Load predictions
        const predictionResponse = await fetch(`/api/predict?ticker=${encodeURIComponent(ticker)}`);
        const predictionData = await predictionResponse.json();
        
        if (!predictionData.success) {
            throw new Error(predictionData.error || 'Failed to generate predictions');
        }
        
        // Process data - convert dates to Date objects for Chart.js
        const historical = historicalData.historical.map(d => ({
            x: new Date(d.date),
            y: d.close
        }));
        
        const predictions = predictionData.predictions.map(d => ({
            x: new Date(d.date),
            y: d.close
        }));
        
        // Update stats
        const currentPrice = historical[historical.length - 1].y;
        const predictedPrice = predictions[predictions.length - 1].y;
        const change = ((predictedPrice - currentPrice) / currentPrice) * 100;
        
        document.getElementById('currentPrice').textContent = formatCurrency(currentPrice);
        document.getElementById('predictedPrice').textContent = formatCurrency(predictedPrice);
        document.getElementById('stockTicker').textContent = ticker;
        
        // Display models used
        const modelsUsed = predictionData.models_used || ['LSTM'];
        document.getElementById('modelsUsed').textContent = modelsUsed.join(' + ');
        
        const changeElement = document.getElementById('expectedChange');
        changeElement.textContent = formatPercent(change);
        changeElement.className = change >= 0 ? 'stat-value positive' : 'stat-value negative';
        
        // Create chart
        createChart(historical, predictions, ticker);
        
        // Hide loading, show content and form
        document.getElementById('loading').style.display = 'none';
        document.getElementById('content').style.display = 'block';
        document.getElementById('tickerForm').style.display = 'block';
        
    } catch (error) {
        console.error('Error loading data:', error);
        document.getElementById('loading').style.display = 'none';
        document.getElementById('error').style.display = 'block';
        document.getElementById('tickerForm').style.display = 'block';
        document.getElementById('error').innerHTML = 
            '<p>❌ Error: ' + error.message + '</p><p>Please try a different ticker symbol.</p>';
    }
}

function createChart(historical, predictions, ticker) {
    const ctx = document.getElementById('stockChart').getContext('2d');
    
    // Destroy existing chart if it exists
    if (stockChart) {
        stockChart.destroy();
    }
    
    stockChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [
                {
                    label: 'Historical Price',
                    data: historical,
                    borderColor: '#667eea',
                    backgroundColor: 'rgba(102, 126, 234, 0.1)',
                    borderWidth: 2,
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 5
                },
                {
                    label: 'Predicted Price (3 months)',
                    data: predictions,
                    borderColor: '#f093fb',
                    backgroundColor: 'rgba(240, 147, 251, 0.1)',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    fill: true,
                    tension: 0.4,
                    pointRadius: 0,
                    pointHoverRadius: 5
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'top',
                    labels: {
                        font: {
                            size: 14,
                            weight: 'bold'
                        },
                        padding: 20,
                        usePointStyle: true
                    }
                },
                tooltip: {
                    mode: 'index',
                    intersect: false,
                    callbacks: {
                        label: function(context) {
                            return context.dataset.label + ': ' + formatCurrency(context.parsed.y);
                        }
                    }
                },
                title: {
                    display: true,
                    text: ticker + ' Stock Price Prediction',
                    font: {
                        size: 18,
                        weight: 'bold'
                    },
                    padding: 20
                }
            },
            scales: {
                x: {
                    type: 'time',
                    time: {
                        unit: 'day',
                        displayFormats: {
                            day: 'MMM dd'
                        }
                    },
                    title: {
                        display: true,
                        text: 'Date',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Price ($)',
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    },
                    grid: {
                        display: true,
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return formatCurrency(value);
                        }
                    }
                }
            },
            interaction: {
                mode: 'nearest',
                axis: 'x',
                intersect: false
            }
        }
    });
}
