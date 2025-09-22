#!/usr/bin/env python3
"""
Simple Web Scraper for Public Data Aggregation
A minimal example that scrapes public quotes data
"""

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime


def scrape_quotes():
    """Scrape quotes from a public quotes website"""
    url = "http://quotes.toscrape.com/"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        quotes = []
        
        for quote in soup.find_all('div', class_='quote'):
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
            
            quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })
        
        return quotes
    
    except requests.RequestException as e:
        print(f"Error fetching data from web: {e}")
        print("Using fallback demo data...")
        return get_demo_data()


def get_demo_data():
    """Return demo data when web scraping is not available"""
    return [
        {
            'text': 'The world as we have created it is a process of our thinking. It cannot be changed without changing our thinking.',
            'author': 'Albert Einstein',
            'tags': ['change', 'deep-thoughts', 'thinking', 'world']
        },
        {
            'text': 'It is our choices, Harry, that show what we truly are, far more than our abilities.',
            'author': 'J.K. Rowling',
            'tags': ['abilities', 'choices']
        },
        {
            'text': 'There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.',
            'author': 'Albert Einstein',
            'tags': ['inspirational', 'life', 'live', 'miracle', 'miracles']
        },
        {
            'text': 'The person, be it gentleman or lady, who has not pleasure in a good novel, must be intolerably stupid.',
            'author': 'Jane Austen',
            'tags': ['aliteracy', 'books', 'classic', 'humor']
        },
        {
            'text': 'A woman is like a tea bag; you never know how strong it is until it\'s in hot water.',
            'author': 'Eleanor Roosevelt',
            'tags': ['misattributed-eleanor-roosevelt']
        }
    ]


def save_data(data, filename='scraped_data.json'):
    """Save scraped data to a JSON file"""
    output = {
        'timestamp': datetime.now().isoformat(),
        'total_items': len(data),
        'data': data
    }
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(data)} items to {filename}")


def main():
    """Main function to run the scraper"""
    print("Starting simple web scraper...")
    
    # Scrape quotes data
    quotes = scrape_quotes()
    
    if quotes:
        print(f"Successfully scraped {len(quotes)} quotes")
        
        # Display first few quotes
        print("\nFirst 3 quotes:")
        for i, quote in enumerate(quotes[:3], 1):
            print(f"{i}. \"{quote['text']}\" - {quote['author']}")
        
        # Save to file
        save_data(quotes)
    else:
        print("No data was scraped")


if __name__ == "__main__":
    main()