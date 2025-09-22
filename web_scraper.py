#!/usr/bin/env python3
"""
Web Scraping for Public Data Aggregation

A Python script using requests and BeautifulSoup to automate the collection of public data.
This script extracts tabular data (Name, Location, Year) from target websites and 
structures it into clean CSV files for easy analysis.
"""

import requests
import csv
import json
import re
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from datetime import datetime
import time


class WebScraper:
    """A class for web scraping public data from websites."""
    
    def __init__(self, delay=1.0, timeout=10):
        """
        Initialize the WebScraper.
        
        Args:
            delay (float): Delay between requests to be respectful to servers
            timeout (int): Request timeout in seconds
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.delay = delay
        self.timeout = timeout
        self.logger = self._setup_logger()
    
    def _setup_logger(self):
        """Set up logging for the scraper."""
        logger = logging.getLogger('WebScraper')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def fetch_page(self, url):
        """
        Fetch a web page and return BeautifulSoup object.
        
        Args:
            url (str): URL to fetch
            
        Returns:
            BeautifulSoup: Parsed HTML content
        """
        try:
            self.logger.info(f"Fetching page: {url}")
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # Add delay to be respectful
            time.sleep(self.delay)
            
            return BeautifulSoup(response.content, 'html.parser')
            
        except requests.RequestException as e:
            self.logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_table_data(self, soup, table_selector=None):
        """
        Extract tabular data from HTML.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            table_selector (str): CSS selector for table (optional)
            
        Returns:
            list: List of dictionaries containing extracted data
        """
        data = []
        
        # Find tables
        if table_selector:
            tables = soup.select(table_selector)
        else:
            tables = soup.find_all('table')
        
        if not tables:
            self.logger.warning("No tables found on the page")
            return data
        
        for table in tables:
            # Extract headers
            headers = []
            header_row = table.find('tr')
            if header_row:
                for th in header_row.find_all(['th', 'td']):
                    headers.append(th.get_text(strip=True))
            
            # Extract data rows
            rows = table.find_all('tr')[1:] if headers else table.find_all('tr')
            
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 3:  # Ensure we have at least 3 columns
                    row_data = {}
                    for i, cell in enumerate(cells):
                        text = cell.get_text(strip=True)
                        if headers and i < len(headers):
                            row_data[headers[i]] = text
                        else:
                            # Default column names if no headers
                            if i == 0:
                                row_data['Name'] = text
                            elif i == 1:
                                row_data['Location'] = text
                            elif i == 2:
                                row_data['Year'] = text
                            else:
                                row_data[f'Column_{i+1}'] = text
                    
                    if row_data:
                        data.append(row_data)
        
        return data
    
    def extract_list_data(self, soup, list_selector=None):
        """
        Extract data from lists when tables are not available.
        
        Args:
            soup (BeautifulSoup): Parsed HTML content
            list_selector (str): CSS selector for list items
            
        Returns:
            list: List of dictionaries containing extracted data
        """
        data = []
        
        # Find list items
        if list_selector:
            items = soup.select(list_selector)
        else:
            items = soup.find_all(['li', 'div', 'article'])
        
        for item in items:
            text = item.get_text(strip=True)
            if len(text) > 10:  # Filter out short items
                # Try to extract structured data using patterns
                row_data = self._parse_text_for_data(text)
                if row_data:
                    data.append(row_data)
        
        return data
    
    def _parse_text_for_data(self, text):
        """
        Parse text to extract Name, Location, Year using patterns.
        
        Args:
            text (str): Text to parse
            
        Returns:
            dict: Extracted data or None
        """
        # Pattern to match year (4 digits)
        year_pattern = r'\b(19|20)\d{2}\b'
        year_match = re.search(year_pattern, text)
        
        # Split text by common delimiters
        parts = re.split(r'[,|\-|–|—|\n|\t]', text)
        parts = [part.strip() for part in parts if part.strip()]
        
        if len(parts) >= 2:
            row_data = {
                'Name': parts[0],
                'Location': parts[1] if len(parts) > 1 else '',
                'Year': year_match.group() if year_match else (parts[2] if len(parts) > 2 else ''),
                'Full_Text': text
            }
            return row_data
        
        return None
    
    def clean_data(self, data):
        """
        Clean and process the scraped data.
        
        Args:
            data (list): Raw data to clean
            
        Returns:
            list: Cleaned data
        """
        cleaned_data = []
        
        for row in data:
            cleaned_row = {}
            for key, value in row.items():
                # Clean the text
                cleaned_value = re.sub(r'\s+', ' ', str(value)).strip()
                cleaned_value = re.sub(r'[^\w\s\-\.\,\(\)]', '', cleaned_value)
                
                # Standardize column names
                if 'name' in key.lower():
                    cleaned_row['Name'] = cleaned_value
                elif 'location' in key.lower() or 'place' in key.lower() or 'city' in key.lower():
                    cleaned_row['Location'] = cleaned_value
                elif 'year' in key.lower() or 'date' in key.lower():
                    # Extract year from date strings
                    year_match = re.search(r'\b(19|20)\d{2}\b', cleaned_value)
                    cleaned_row['Year'] = year_match.group() if year_match else cleaned_value
                else:
                    cleaned_row[key] = cleaned_value
            
            # Ensure required fields exist
            if 'Name' not in cleaned_row:
                cleaned_row['Name'] = cleaned_row.get(list(cleaned_row.keys())[0], '') if cleaned_row else ''
            if 'Location' not in cleaned_row:
                cleaned_row['Location'] = ''
            if 'Year' not in cleaned_row:
                cleaned_row['Year'] = ''
            
            # Only include rows with at least a name
            if cleaned_row['Name']:
                cleaned_data.append(cleaned_row)
        
        return cleaned_data
    
    def save_to_csv(self, data, filename):
        """
        Save data to CSV file.
        
        Args:
            data (list): Data to save
            filename (str): Output filename
        """
        if not data:
            self.logger.warning("No data to save")
            return
        
        # Get all unique keys for headers
        all_keys = set()
        for row in data:
            all_keys.update(row.keys())
        
        # Ensure Name, Location, Year are first columns
        headers = ['Name', 'Location', 'Year']
        for key in sorted(all_keys):
            if key not in headers:
                headers.append(key)
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=headers)
                writer.writeheader()
                writer.writerows(data)
            
            self.logger.info(f"Data saved to {filename} ({len(data)} rows)")
            
        except Exception as e:
            self.logger.error(f"Error saving to CSV: {e}")
    
    def save_to_json(self, data, filename):
        """
        Save data to JSON file.
        
        Args:
            data (list): Data to save
            filename (str): Output filename
        """
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)
            
            self.logger.info(f"Data saved to {filename} ({len(data)} rows)")
            
        except Exception as e:
            self.logger.error(f"Error saving to JSON: {e}")
    
    def scrape_website(self, url, table_selector=None, list_selector=None, output_prefix='scraped_data'):
        """
        Main method to scrape a website and save data.
        
        Args:
            url (str): URL to scrape
            table_selector (str): CSS selector for tables
            list_selector (str): CSS selector for list items
            output_prefix (str): Prefix for output files
            
        Returns:
            list: Cleaned data
        """
        self.logger.info(f"Starting scraping of {url}")
        
        # Fetch the page
        soup = self.fetch_page(url)
        if not soup:
            return []
        
        # Extract data
        data = []
        
        # Try tables first
        table_data = self.extract_table_data(soup, table_selector)
        if table_data:
            data.extend(table_data)
            self.logger.info(f"Extracted {len(table_data)} rows from tables")
        
        # Try lists if no table data
        if not data:
            list_data = self.extract_list_data(soup, list_selector)
            data.extend(list_data)
            self.logger.info(f"Extracted {len(list_data)} rows from lists")
        
        # Clean the data
        cleaned_data = self.clean_data(data)
        self.logger.info(f"Cleaned data: {len(cleaned_data)} rows")
        
        # Save to files
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"{output_prefix}_{timestamp}.csv"
        json_filename = f"{output_prefix}_{timestamp}.json"
        
        self.save_to_csv(cleaned_data, csv_filename)
        self.save_to_json(cleaned_data, json_filename)
        
        return cleaned_data


def main():
    """
    Demonstration of the web scraping functionality.
    """
    scraper = WebScraper(delay=1.0)
    
    # Example: Scraping a website with public data
    # This is a demonstration URL - replace with actual public data source
    demo_urls = [
        # Example of a site with tabular data
        "https://httpbin.org/html",  # Demo site for testing
    ]
    
    for url in demo_urls:
        try:
            print(f"\n=== Scraping {url} ===")
            data = scraper.scrape_website(url, output_prefix='public_data')
            
            if data:
                print(f"Successfully extracted {len(data)} records")
                print("\nSample data:")
                for i, record in enumerate(data[:3]):  # Show first 3 records
                    print(f"Record {i+1}: {record}")
            else:
                print("No data extracted")
                
        except Exception as e:
            print(f"Error scraping {url}: {e}")


if __name__ == "__main__":
    main()