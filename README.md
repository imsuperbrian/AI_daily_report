# AI Daily Report

AI Daily Report is a news monitoring and AI-powered market sentiment analysis tool built with Python, OpenAI API, SQLite, and Docker.

## Features

### News Collection

* Collect articles from multiple RSS sources
* Support news, official announcements, and community discussions

### Keyword Management

* Add keywords
* View keywords
* Delete keywords
* Store keywords in SQLite database

### AI Analysis

* OpenAI-powered market sentiment analysis
* Trending keyword detection
* Automatic report generation

### History Tracking

* Store search history
* Store article counts
* Store AI sentiment analysis results
* Query historical records

### Database

* SQLite database
* Keyword storage
* Search history storage
* CRUD operations

### Deployment

* Local execution
* Docker container support

## Application Menu

1. Add Keyword
2. View Keywords
3. Delete Keyword
4. Run Analysis
5. View History
6. Exit

## Project Structure

```text
ai_analyzer.py
ai_daily_report.py
ai_summary.py
application.py
article_processor.py
database.py
main.py
requirements.txt
README.md
```

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python3 application.py
```

## Docker

Build image:

```bash
docker build -t ai-daily-report .
```

Run container:

```bash
docker run -it \
-e OPENAI_API_KEY=$OPENAI_API_KEY \
ai-daily-report
```

## Future Development

* Streamlit Dashboard
* Trend Visualization
* Automated Scheduling
* Web Deployment
* Stock Market Analysis Extension
