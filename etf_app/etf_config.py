"""
ETF Universe — 5 carefully selected ETFs.
Data source: Yahoo Finance via yfinance (free, no API key, full NSE coverage).
Yahoo Finance uses ".NS" suffix for NSE-listed securities.
"""

ETF_UNIVERSE = {
    "NIFTYBEES": {
        "name": "Nippon India ETF Nifty BeES",
        "short_name": "Nifty BeES",
        "yf_symbol": "NIFTYBEES.NS",
        "category": "Broad Market",
        "benchmark_symbol": "^NSEI",
        "benchmark_name": "Nifty 50",
        "description": "Tracks Nifty 50 — India's flagship 50-stock large-cap benchmark. Oldest and most liquid Indian ETF.",
        "icon": "📊",
        "color": "#00D4FF",
        "accent": "rgba(0,212,255,0.15)",
    },
    "BANKBEES": {
        "name": "Nippon India ETF Bank BeES",
        "short_name": "Bank BeES",
        "yf_symbol": "BANKBEES.NS",
        "category": "Sectoral · Banking",
        "benchmark_symbol": "^NSEBANK",
        "benchmark_name": "Nifty Bank",
        "description": "Tracks Nifty Bank Index — high-beta play on India's 12 most liquid banking stocks. Highly rate-sensitive.",
        "icon": "🏦",
        "color": "#F97316",
        "accent": "rgba(249,115,22,0.15)",
    },
    "ITBEES": {
        "name": "Nippon India ETF Nifty IT",
        "short_name": "IT BeES",
        "yf_symbol": "ITBEES.NS",
        "category": "Sectoral · Technology",
        "benchmark_symbol": "^CNXIT",
        "benchmark_name": "Nifty IT",
        "description": "Tracks Nifty IT Index — pure-play exposure to TCS, Infosys, Wipro, HCL. USD/INR sensitive.",
        "icon": "💻",
        "color": "#A78BFA",
        "accent": "rgba(167,139,250,0.15)",
    },
    "GOLDBEES": {
        "name": "Nippon India ETF Gold BeES",
        "short_name": "Gold BeES",
        "yf_symbol": "GOLDBEES.NS",
        "category": "Commodity · Gold",
        "benchmark_symbol": "GC=F",
        "benchmark_name": "Gold Futures",
        "description": "Physical gold ETF — each unit ≈ 0.01g gold. Hedge against inflation, currency risk, and equity drawdowns.",
        "icon": "🥇",
        "color": "#FBBF24",
        "accent": "rgba(251,191,36,0.15)",
    },
    "JUNIORBEES": {
        "name": "Nippon India ETF Junior BeES",
        "short_name": "Junior BeES",
        "yf_symbol": "JUNIORBEES.NS",
        "category": "Midcap · Next 50",
        "benchmark_symbol": "^NSEI",
        "benchmark_name": "Nifty Next 50",
        "description": "Tracks Nifty Next 50 — the 'tomorrow's Nifty 50' basket. Higher growth potential with elevated volatility.",
        "icon": "🚀",
        "color": "#34D399",
        "accent": "rgba(52,211,153,0.15)",
    },
}

# Maps frontend timeframe key → yfinance period + interval
TIMEFRAMES = {
    "5m":  {"period": "60d",  "interval": "5m",   "label": "5 Minutes"},
    "15m": {"period": "60d",  "interval": "15m",  "label": "15 Minutes"},
    "1h":  {"period": "max", "interval": "1h",   "label": "1 Hour"},
    "1d":  {"period": "max", "interval": "1d",   "label": "1 Day"},
    "1W":  {"period": "max",  "interval": "1wk",  "label": "1 Week"},
    "1M":  {"period": "max",  "interval": "1mo",  "label": "1 Month"},
    "3M":  {"period": "max",  "interval": "1mo",  "label": "3 Months"},
    "6M":  {"period": "max",  "interval": "1mo",  "label": "6 Months"},
    "1Y":  {"period": "max", "interval": "1mo",  "label": "1 Year"},
}

DEFAULT_TICKER    = "NIFTYBEES"
DEFAULT_TIMEFRAME = "1d"
