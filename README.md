# Web Scraping for Public Data Aggregation

A simple Python web scraper for aggregating public data. This project demonstrates basic web scraping techniques to collect and store publicly available information.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the scraper:**
   ```bash
   python scraper.py
   ```

3. **View results:**
   - Check the console output for scraped data preview
   - Find complete data in `scraped_data.json`

## What it does

- Scrapes public quotes from quotes.toscrape.com
- Extracts quote text, author, and tags
- Saves data in JSON format with timestamp
- Simple error handling and progress feedback

## Example Output

```json
{
  "timestamp": "2023-12-07T10:30:00",
  "total_items": 10,
  "data": [
    {
      "text": "The world as we have created it...",
      "author": "Albert Einstein",
      "tags": ["change", "deep-thoughts", "thinking"]
    }
  ]
}
```

## Features

- ✅ Simple and minimal code
- ✅ No complex configuration required
- ✅ Works with public data sources
- ✅ JSON output format
- ✅ Basic error handling

## Requirements

- Python 3.6+
- Internet connection
- Libraries: requests, beautifulsoup4