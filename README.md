# AI Daily Report

AI Daily Report is an AI-powered news intelligence dashboard that tracks technology and AI-related topics, analyzes news trends, generates AI insights, and ranks topics using a proprietary Hotness Score.

## Project Goal

Most AI news tools only summarize articles.

AI Daily Report focuses on identifying which topics matter most by combining:

- News Volume
- Momentum
- Market Sentiment

The system transforms raw news into actionable intelligence through AI-generated insights and a proprietary Hotness Score ranking engine.

---

## Features

### News Collection

- Collects articles from RSS feeds
- Supports multiple keywords
- Automatic article filtering
- Duplicate article removal

### AI Analysis

- AI Market Sentiment Analysis
- Keyword-specific AI Insights
- Daily Report Generation
- Trending Word Analysis

### Trend Analytics

- Historical article tracking
- Keyword growth analysis
- Article volume monitoring
- Trend visualization

### Hotness Score Engine

Each keyword receives a Hotness Score (0-100).

Hotness Score consists of:

- Volume Score (0-40)
- Momentum Score (0-40)
- Sentiment Score (0-20)

Formula:

```text
Hotness Score = Volume Score + Momentum Score + Sentiment Score
```

This allows users to identify the most important topics of the day.

### Dashboard Pages

- Overview
- Keywords
- Run Analysis
- History
- Articles
- Trend Analytics
- AI Insights

### Email Reports

- Daily report generation
- AI insight delivery
- Gmail SMTP integration

### OpenAI API Support

Users can provide their own OpenAI API key directly through the dashboard.

No API key is stored permanently.

---

## Technology Stack

### Backend

- Python
- SQLite
- OpenAI API

### Frontend

- Streamlit

### Libraries

- pandas
- openai
- feedparser
- python-dotenv

---

## Installation

Clone repository:

```bash
git clone https://github.com/YOUR_USERNAME/AI_daily_report.git
cd AI_daily_report
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run dashboard:

```bash
streamlit run dashboard.py
```

---

## Usage

1. Open the dashboard
2. Enter your OpenAI API key
3. Add keywords
4. Run analysis
5. Review AI Insights and Hotness Rankings

---

## Hotness Score Example

| Keyword | Volume | Momentum | Sentiment | Hotness |
|----------|----------|----------|----------|----------|
| NVIDIA | 40 | 35 | 20 | 95 |
| Apple | 30 | 25 | 20 | 75 |
| Gemini | 20 | 15 | 10 | 45 |

---

## Current Features

RSS News Collection

Keyword Management

SQLite Database Storage

Trend Analytics

AI Market Sentiment Analysis

Keyword-specific AI Insights

Email Reports

Hotness Score Ranking System

Streamlit Dashboard

User-provided OpenAI API Key Support

---

## Future Roadmap

- Daily Briefing Page
- Scheduled Analysis
- Automatic Email Delivery
- Streamlit Cloud Deployment
- User Accounts
- Portfolio Watchlists
- Financial Market Intelligence

---

## License

MIT License