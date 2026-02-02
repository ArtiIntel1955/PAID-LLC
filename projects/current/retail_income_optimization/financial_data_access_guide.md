# Financial Data Access Guide for Public Companies

Based on best practices for accessing financial data from publicly traded companies, here are the three most reliable methods:

## 1. The "Golden Standard" (SEC EDGAR)

If you need data on US-listed companies (10-Ks, 10-Qs), the SEC's EDGAR system is the source of truth. It is free and public.

### The Agent Approach:
- Do not have your agent "scrape" the website; the SEC will block the IP
- Instead, use the SEC JSON API which provides structured data for company facts and submissions

### Key Tool:
- Use the sec-api library (Python) or the direct SEC.gov RESTful API

### Best for:
- Audited financial statements
- Balance sheets
- Insider trading filings

## 2. Free-Tier Financial APIs (Structured & Fast)

If the SEC data is too "raw," use an API that has already cleaned and organized the data into JSON. These all have free tiers that are perfect for agents:

### Provider Options:

| Provider | Free Tier Limit | Best Feature |
|----------|----------------|--------------|
| Alpha Vantage | 25 requests/day | Best documentation for beginner agents |
| Financial Modeling Prep | 250 requests/day | Great for "Company Profiles" and quick stock quotes |
| Finnhub.io | 60 requests/minute | Excellent for real-time news and "Earnings Surprise" data |
| Twelve Data | 800 requests/day | Global market coverage beyond just the US |

## 3. The "Unofficial" Powerhouse (Yahoo Finance)

Yahoo Finance doesn't have an "official" free API anymore, but the developer community has built incredibly stable libraries that "wrap" their public data.

### The Tool:
- yfinance (Python library)

### Why it works:
- Allows pulling historical prices, dividends, and basic analyst recommendations with just two lines of code

### Warning:
- Since it isn't an official API, it can occasionally break if Yahoo changes their website layout

## Comparison of Financial Data Architectures

## Troubleshooting: Why your agent is failing

If your agent is still having trouble, check these three common "silent" killers:

### 1. User-Agent Header:
- Many financial sites (like the SEC) require declaring a "User-Agent" header (e.g., Sample Company AdminContact@example.com)
- If left blank, the agent will get a 403 Forbidden error

### 2. Context Window:
- 10-K filings are massive
- If your agent is trying to read the whole file, it will run out of "memory"
- Use RAG (Retrieval-Augmented Generation) to only feed the agent the specific tables it needs

### 3. Ticker vs. CIK:
- Some systems use stock symbols (AAPL)
- The SEC uses CIK numbers (0000320193)
- Your agent might need a "mapping" function to switch between them