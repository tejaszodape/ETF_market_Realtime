import json
import logging
from datetime import datetime

import numpy as np
import pytz
import yfinance as yf
import pandas as pd

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET

from .etf_config import ETF_UNIVERSE, TIMEFRAMES, DEFAULT_TICKER, DEFAULT_TIMEFRAME

logger = logging.getLogger(__name__)
IST = pytz.timezone("Asia/Kolkata")


# ─────────────────────────────────────────────
# Market Status
# ─────────────────────────────────────────────

def get_market_status():
    now = datetime.now(IST)
    wd = now.weekday()

    minutes = now.hour * 60 + now.minute
    open_t = 9 * 60 + 15
    close_t = 15 * 60 + 30

    if wd < 5 and open_t <= minutes <= close_t:
        return {"status": "LIVE", "is_live": True}

    if wd < 5 and minutes < open_t:
        return {"status": "PRE_OPEN", "is_live": False}

    if wd < 5:
        return {"status": "CLOSED", "is_live": False}

    return {"status": "WEEKEND", "is_live": False}


# ─────────────────────────────────────────────
# Fetch candles from yfinance
# ─────────────────────────────────────────────

def fetch_candles(symbol, interval="5m", period="5d"):

    df = yf.download(
        symbol,
        interval=interval,
        period=period,
        progress=False,
        auto_adjust=True
    )

    if df is None or df.empty:
        return []

    # Fix multi-index columns returned by yfinance
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    candles = []

    for idx, row in df.iterrows():

        candles.append({
            "time": int(idx.timestamp()),
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]) if not pd.isna(row["Volume"]) else 0
        })

    return candles


# ─────────────────────────────────────────────
# Quote
# ─────────────────────────────────────────────

def fetch_quote(symbol):

    ticker = yf.Ticker(symbol)
    info = ticker.fast_info

    price = info.get("lastPrice")
    prev = info.get("previousClose")

    if not price or not prev:
        return {}

    change = price - prev

    return {
        "price": round(price, 2),
        "prev_close": round(prev, 2),
        "change": round(change, 2),
        "change_pct": round((change / prev) * 100, 2),
    }


# ─────────────────────────────────────────────
# RSI
# ─────────────────────────────────────────────
def compute_rsi(closes, period=14):

    series = pd.Series(closes)

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100 / (1 + rs))

    rsi = rsi.replace([np.inf, -np.inf], np.nan)

    # Convert NaN → None
    return [None if pd.isna(v) else float(v) for v in rsi]

@require_GET
def api_commentary(request):

    ticker = request.GET.get("ticker", DEFAULT_TICKER)

    if ticker not in ETF_UNIVERSE:
        return JsonResponse({"error": "Unknown ticker"}, status=400)

    symbol = ETF_UNIVERSE[ticker]["yf_symbol"]

    quote = fetch_quote(symbol)

    if not quote:
        return JsonResponse({"error": "No market data"}, status=503)

    text = f"{ticker} is trading at ₹{quote['price']} with a change of {quote['change_pct']}%."

    return JsonResponse({
        "ticker": ticker,
        "commentary": text,
        "powered_by": "AI"
    })

# ─────────────────────────────────────────────
# EMA
# ─────────────────────────────────────────────
def compute_ema(closes, period):

    ema = pd.Series(closes).ewm(span=period).mean()

    return [None if pd.isna(v) else float(v) for v in ema]


def compute_support_resistance(highs, lows):
    if len(highs) < 20:
        return {}
    recent_highs = highs[-20:]
    recent_lows = lows[-20:]
    resistance1 = max(recent_highs)
    resistance2 = max(highs[-40:]) if len(highs) >= 40 else resistance1
    support1 = min(recent_lows)
    support2 = min(lows[-40:]) if len(lows) >= 40 else support1
    return {
        'support1': support1,
        'support2': support2,
        'resistance1': resistance1,
        'resistance2': resistance2
    }

def detect_pattern(closes, highs, lows):
    if len(closes) < 10:
        return "No pattern detected"
    recent_closes = closes[-10:]
    if all(recent_closes[i] < recent_closes[i+1] for i in range(len(recent_closes)-1)):
        return "Ascending Channel"
    elif all(recent_closes[i] > recent_closes[i+1] for i in range(len(recent_closes)-1)):
        return "Descending Channel"
    recent_highs = highs[-10:]
    if recent_highs.count(max(recent_highs)) >= 2:
        return "Double Top"
    return "No significant pattern"


# ─────────────────────────────────────────────
def compute_signals(closes, ema20, ema50, rsi):
    last_close = closes[-1] if closes else None
    last_ema20 = ema20[-1] if ema20 and ema20[-1] is not None else None
    last_ema50 = ema50[-1] if ema50 and ema50[-1] is not None else None
    last_rsi = rsi[-1] if rsi and rsi[-1] is not None else None

    signals = {}
    trend = "Neutral"
    if last_rsi is not None:
        if last_rsi > 70:
            signals['rsi'] = 'Overbought (Sell)'
        elif last_rsi < 30:
            signals['rsi'] = 'Oversold (Buy)'
        else:
            signals['rsi'] = 'Neutral'
    if last_ema20 is not None and last_ema50 is not None:
        if last_ema20 > last_ema50:
            signals['ema'] = 'Bullish (Buy)'
            trend = "Bullish"
        else:
            signals['ema'] = 'Bearish (Sell)'
            trend = "Bearish"
    signals['trend'] = trend
    return signals


# ─────────────────────────────────────────────
# Dashboard
# ─────────────────────────────────────────────

def dashboard(request):

    etfs = [{**{"ticker": k}, **cfg} for k, cfg in ETF_UNIVERSE.items()]

    return render(request, "etf_app/dashboard.html", {
        "etfs": json.dumps(etfs),
        "timeframes": [{"key": k, "label": v["label"]} for k, v in TIMEFRAMES.items()],
        "default_ticker": DEFAULT_TICKER,
        "default_timeframe": DEFAULT_TIMEFRAME,
    })


# ─────────────────────────────────────────────
# ETF DATA API
# ─────────────────────────────────────────────

@require_GET
def api_etf_data(request):

    ticker = request.GET.get("ticker", DEFAULT_TICKER)
    tf_key = request.GET.get("timeframe", DEFAULT_TIMEFRAME)

    if ticker not in ETF_UNIVERSE:
        return JsonResponse({"error": "Unknown ticker"}, status=400)

    cfg = ETF_UNIVERSE[ticker]
    tf = TIMEFRAMES[tf_key]

    symbol = cfg["yf_symbol"]

    candles = fetch_candles(symbol, tf["interval"], tf["period"])

    if not candles:
        return JsonResponse({"error": "No market data"}, status=503)

    closes = [c["close"] for c in candles]
    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    ema20 = compute_ema(closes, 20)
    ema50 = compute_ema(closes, 50)

    rsi = compute_rsi(closes)

    signals = compute_signals(closes, ema20, ema50, rsi)

    sr = compute_support_resistance(highs, lows)

    pattern = detect_pattern(closes, highs, lows)

    quote = fetch_quote(symbol)

    description = f"Current trend is {signals['trend']}. Pattern detected: {pattern}. Support levels: ₹{sr.get('support1', 0):.2f}, ₹{sr.get('support2', 0):.2f}. Resistance levels: ₹{sr.get('resistance1', 0):.2f}, ₹{sr.get('resistance2', 0):.2f}. Live price: ₹{quote['price']}."

    return JsonResponse({
        "ticker": ticker,
        "quote": quote,
        "candles": candles,
        "indicators": {
            "ema20": ema20,
            "ema50": ema50,
            "rsi": rsi
        },
        "signals": signals,
        "support_resistance": sr,
        "pattern": pattern,
        "description": description,
        "market_status": get_market_status(),
    })


# ─────────────────────────────────────────────
# Sidebar prices
# ─────────────────────────────────────────────

@require_GET
def api_sidebar_prices(request):

    prices = {}

    for ticker, cfg in ETF_UNIVERSE.items():

        q = fetch_quote(cfg["yf_symbol"])

        if q:
            prices[ticker] = {
                "price": q["price"],
                "change_pct": q["change_pct"]
            }

    return JsonResponse({"prices": prices})


# ─────────────────────────────────────────────
# Market status API
# ─────────────────────────────────────────────

@require_GET
def api_market_status(request):
    return JsonResponse(get_market_status())