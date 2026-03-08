# ETF Dashboard

A comprehensive Django-based ETF analysis dashboard featuring interactive candlestick charts, real-time data updates, trend analysis, pattern detection, support and resistance levels, and a responsive design optimized for desktop, tablet, and mobile devices.

<img width="2486" height="1628" alt="image" src="https://github.com/user-attachments/assets/5dcb604e-24cb-45ae-8062-16d5259b9c95" />


## Features

### Core Functionality
- **Interactive Candlestick Charts**: Powered by Lightweight Charts library for smooth OHLCV visualization.
- **Real-Time Data Updates**: Automatically refreshes ETF data and sidebar prices every 5 seconds.
- **Multiple Timeframes**: Support for 1D, 1W, 1M, and 3M periods.
- **Volume Analysis**: Color-coded volume histograms synchronized with price charts.
- **Trend Analysis**: Detects bullish, bearish, or sideways trends based on EMA crossovers and momentum.
- **Chart Pattern Detection**: Identifies common patterns like double tops/bottoms, head and shoulders, triangles, flags, and cup & handle.
- **Support & Resistance Levels**: Calculates and displays pivot-based support and resistance lines on the chart.
- **Technical Indicators**: Includes RSI, EMA 20, and EMA 50 with buy/sell signals.
- **ETF Watchlist**: Sidebar displaying selected ETFs with live prices and changes.
- **AI Analysis**: Dynamic commentary generated based on current market data.
- **Responsive Design**: Adapts seamlessly to mobile, tablet, and desktop screens with a collapsible sidebar and mobile menu.

### Technical Stack
- **Backend**: Django 4.2 (Python 3.x)
- **Data Source**: Yahoo Finance (yfinance library)
- **Frontend**: HTML5, CSS3, JavaScript
- **Charts**: Lightweight Charts v4.1.3
- **Deployment**: Ready for Render, Railway, or other platforms with provided config files

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd etf_project\ 4
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the Django server:
   ```bash
   python manage.py runserver
   ```

5. Open your browser and navigate to `http://localhost:8000`

## Project Structure

```
etf_project 4/
├── manage.py
├── Procfile
├── README.md
├── render.yaml
├── requirements.txt
├── etf_app/
│   ├── __init__.py
│   ├── etf_config.py
│   ├── urls.py
│   ├── views.py
│   ├── __pycache__/
│   ├── static/
│   │   └── etf_app/
│   └── templates/
│       └── etf_app/
│           └── dashboard.html
└── etf_dashboard/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    ├── wsgi.py
    └── __pycache__/
```

## API Endpoints

- `/`: Main dashboard view
- `/api/etf-data/`: Returns OHLCV data, indicators, signals, and analysis for a given ETF and timeframe
- `/api/sidebar-prices/`: Provides live prices and changes for all ETFs in the watchlist
- `/api/commentary/`: Generates AI analysis commentary for the selected ETF

## Configuration

The dashboard is configured to work with a selection of popular ETFs. You can modify the ETF list in `etf_app/etf_config.py`.


## Contributing

Feel free to fork the repository and submit pull requests for improvements or bug fixes.

## License

This project is open-source. Please check the license file for details.
