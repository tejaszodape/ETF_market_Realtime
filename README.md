# FinVise ETF Intelligence Terminal

> **Live, production-grade ETF Market Analysis Dashboard for Indian Markets**
> Built with Django · Powered by **Twelve Data API** · AI commentary via Claude

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Django](https://img.shields.io/badge/Django-4.2-green)
![Data](https://img.shields.io/badge/Data-Twelve%20Data%20API-orange)

---

## 🌐 Live URL
> _(Deploy using instructions below — paste URL here)_

## 📦 GitHub Repository
> _(Push this code and paste URL here)_

---

## 📊 ETF Universe — Why These 5?

| # | ETF | Ticker | Category | Benchmark | Rationale |
|---|-----|--------|----------|-----------|-----------|
| 1 | Nippon India ETF Nifty BeES | `NIFTYBEES` | Broad Market | Nifty 50 | **The anchor** — baseline macro indicator; oldest Indian ETF |
| 2 | Nippon India ETF Bank BeES | `BANKBEES` | Sectoral · Banking | Nifty Bank | **Rate-sensitive play** — RBI policy signals, credit cycles |
| 3 | Nippon India ETF Nifty IT | `ITBEES` | Sectoral · Technology | Nifty IT | **USD/INR proxy** — tracks global tech sentiment + rupee |
| 4 | Nippon India ETF Gold BeES | `GOLDBEES` | Commodity · Gold | Gold Price | **Safe-haven hedge** — low/negative correlation to equities |
| 5 | Nippon India ETF Junior BeES | `JUNIORBEES` | Midcap · Next 50 | Nifty Next 50 | **Alpha play** — higher beta, earnings growth optionality |

**Diversity rationale:** Broad market + two uncorrelated sectors + commodity + midcap growth — this selection captures 5 distinct risk/return profiles and investment theses, enabling meaningful cross-asset analysis.

---

## ✨ Features

### Core Functionality
- **Live OHLCV Candlestick Chart** — Twelve Data API, 4 timeframes (1W/1M/3M/6M)
- **Trend Detection** — Bullish / Bearish / Sideways / Consolidating via EMA crossover + momentum
- **Chart Pattern Detection** — 8 patterns: Double Top/Bottom, H&S, Inv. H&S, Ascending/Descending Triangle, Bull/Bear Flag, Cup & Handle
- **Support & Resistance** — Pivot-based local extrema clustering, drawn as price lines on chart
- **Volume Analysis** — Colour-coded histogram synchronized with price chart
- **Signal Anomaly Flags** — Volume spikes, RSI extremes, gap detection, 52-week proximity alerts

### Technical Indicators (all via Twelve Data API)
| Indicator | Parameters | Use |
|-----------|-----------|-----|
| EMA | 20, 50 | Trend direction & crossover |
| RSI | Period 14 | Momentum & overbought/sold zones |
| MACD | 12, 26, 9 | Trend momentum & divergence |
| Bollinger Bands | 20, ±2σ | Volatility & breakout signals |
| Stochastic | 14, 3 | Overbought/oversold confirmation |

### AI/ML Layer
- **Analyst Commentary Panel** — Dynamically generated from live data every time you switch ETF or timeframe
- **Claude API integration** — If `ANTHROPIC_API_KEY` is set, commentary is LLM-generated
- **Rule-based NLP fallback** — Full commentary engine that generates analyst-quality notes without any LLM key
- **Category-aware context** — Banking commentary mentions rate environment; Gold mentions macro; IT mentions USD/INR

### UX / Engineering
- **NSE market status** — Live/Pre-Market/Closed/Weekend with IST clock
- **Benchmark comparison chart** — Normalized base-100 performance overlay
- **Responsive** — Mobile, tablet, desktop
- **Graceful degradation** — Rate limit handling, API error handling, fallback commentary
- **Bloomberg terminal aesthetic** — IBM Plex Mono, industrial dark theme, amber accent

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd etf_project

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env
# .env is pre-configured with the Twelve Data API key
# Optionally add: ANTHROPIC_API_KEY=sk-ant-...

# 5. Run
python manage.py runserver

# 6. Open browser
open http://localhost:8000
```

---

## ☁️ Deploy to Render (Recommended — Free Tier)

1. Push this repo to GitHub (public)
2. Go to [render.com](https://render.com) → **New Web Service**
3. Connect your repo — Render auto-detects `render.yaml`
4. Click **Deploy**
5. *(Optional)* Add `ANTHROPIC_API_KEY` in Render → Environment variables for AI commentary
6. Paste your live URL in the submission email

### Alternative: Railway

```bash
# Install Railway CLI
npm i -g @railway/cli
railway login
railway init
railway up
```

---

## 🏗 Architecture

```
etf_project/
├── etf_dashboard/              # Django project config
│   ├── settings.py             # All settings + API key env vars
│   ├── urls.py                 # Root URL router
│   └── wsgi.py
│
├── etf_app/                    # Main application
│   ├── etf_config.py           # ETF universe (5 ETFs + benchmarks + metadata)
│   ├── twelve_data.py          # Twelve Data API client (all live data calls)
│   ├── technical_analysis.py   # S/R detection, trend ID, 8-pattern detector, anomaly flags
│   ├── ai_analysis.py          # Claude API + rule-based commentary engine
│   ├── views.py                # 5 REST endpoints + dashboard render
│   ├── urls.py
│   └── templates/etf_app/
│       └── dashboard.html      # Full SPA — TradingView charts + Chart.js indicators
│
├── requirements.txt
├── render.yaml                 # One-click Render deploy
├── railway.toml                # Railway deploy
├── Procfile                    # Gunicorn
└── README.md
```

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Main dashboard (SPA) |
| `/api/etf-data/?ticker=X&timeframe=Y` | GET | Full OHLCV + all indicators + analysis |
| `/api/commentary/?ticker=X&timeframe=Y` | GET | AI analyst commentary (separate async call) |
| `/api/market-status/` | GET | NSE market open/closed status |
| `/api/sidebar-prices/` | GET | Lightweight price+change for all 5 ETFs |

---

## 🔑 Environment Variables

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `TWELVE_DATA_API_KEY` | **Yes** | `8d5ca07f...` | All market data |
| `ANTHROPIC_API_KEY` | No | — | Claude AI commentary |
| `DJANGO_SECRET_KEY` | Yes (prod) | Auto in render.yaml | Django security |
| `DEBUG` | No | `True` | Set `False` in production |
| `ALLOWED_HOSTS` | Yes (prod) | `localhost,...` | Comma-separated hostnames |

---

## 📐 Technical Stack

| Layer | Technology |
|-------|-----------|
| Backend | Django 4.2 (Python 3.10+) |
| Data API | Twelve Data (time_series, quote, rsi, ema, macd, bbands, stoch) |
| Charts | TradingView Lightweight Charts v4 (OHLCV) + Chart.js v4 (indicators) |
| AI | Anthropic Claude Sonnet 4 API + custom rule-based NLP engine |
| Static files | WhiteNoise |
| Deployment | Gunicorn + Render/Railway |
| Fonts | IBM Plex Mono + IBM Plex Sans |

---

## ⚠️ Notes

- **No static files or hard-coded prices** — every data point is fetched live from Twelve Data API at request time
- **Rate limits** — Twelve Data free tier: 800 API credits/day, 8 credits/minute. The dashboard makes ~7-9 API calls per ETF load. If rate-limited, error messages are shown gracefully (no blank charts or crashes)
- **Market hours** — Outside NSE hours (9:15–15:30 IST, Mon–Fri), the dashboard shows the most recently available data and displays "Market Closed · Latest data shown"
- **API keys** — Never committed to the repository. Managed via environment variables only
