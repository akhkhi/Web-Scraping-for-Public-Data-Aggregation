# Web Scraping for Public Data Aggregation

A Python-based web scraping solution that automates the collection of public data from websites using `requests` and `BeautifulSoup`. This tool extracts tabular data (Name, Location, Year) from target websites and processes it into clean CSV files for easy analysis.

## Features

✅ **Automated Data Collection**: Uses `requests` and `BeautifulSoup` to scrape public websites  
✅ **Tabular Data Extraction**: Extracts structured data including Name, Location, Year, and other fields  
✅ **Data Processing & Cleaning**: Cleans and standardizes scraped data  
✅ **CSV Export**: Outputs data in clean, analyzable CSV format  
✅ **JSON Export**: Additional JSON format for flexible data usage  
✅ **Error Handling**: Robust error handling and logging  
✅ **Respectful Scraping**: Includes delays and proper headers to be respectful to servers  

## Requirements

- Python 3.6+
- requests
- beautifulsoup4
- csv (built-in)
- json (built-in)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/akhkhi/Web-Scraping-for-Public-Data-Aggregation.git
cd Web-Scraping-for-Public-Data-Aggregation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

Or on Ubuntu/Debian systems:
```bash
sudo apt install python3-bs4
```

## Usage

### Basic Usage

```python
from web_scraper import WebScraper

# Initialize the scraper
scraper = WebScraper(delay=1.0)

# Scrape a website
data = scraper.scrape_website('https://example.com', output_prefix='my_data')
```

### Running the Example

```bash
python3 example_usage.py
```

This will demonstrate:
- Data extraction and cleaning
- CSV/JSON file generation
- Sample data processing

### Custom Scraping

```python
from web_scraper import WebScraper

scraper = WebScraper()

# Fetch and parse a webpage
soup = scraper.fetch_page('https://example.com')

# Extract table data
table_data = scraper.extract_table_data(soup)

# Clean the data
cleaned_data = scraper.clean_data(table_data)

# Save to files
scraper.save_to_csv(cleaned_data, 'output.csv')
scraper.save_to_json(cleaned_data, 'output.json')
```

## File Structure

```
Web-Scraping-for-Public-Data-Aggregation/
├── web_scraper.py          # Main scraping class
├── example_usage.py        # Example usage and demonstrations
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── .gitignore            # Git ignore rules
└── output/               # Generated CSV/JSON files (ignored by git)
    ├── sample_public_data.csv
    ├── sample_cleaned_data.csv
    └── *.json files
```

## Data Structure

The scraper extracts and standardizes data into the following format:

### CSV Output
```csv
Name,Location,Year,Additional_Columns...
John Smith,"New York, NY",2023,Technology
Maria Garcia,"Los Angeles, CA",2022,Healthcare
David Johnson,"Chicago, IL",2023,Education
```

### JSON Output
```json
[
  {
    "Name": "John Smith",
    "Location": "New York, NY", 
    "Year": "2023",
    "Category": "Technology"
  },
  {
    "Name": "Maria Garcia",
    "Location": "Los Angeles, CA",
    "Year": "2022", 
    "Category": "Healthcare"
  }
]
```

## Class Methods

### WebScraper Class

- `__init__(delay=1.0, timeout=10)`: Initialize scraper with configurable delays
- `fetch_page(url)`: Fetch and parse a webpage
- `extract_table_data(soup, table_selector=None)`: Extract data from HTML tables
- `extract_list_data(soup, list_selector=None)`: Extract data from HTML lists
- `clean_data(data)`: Clean and standardize extracted data
- `save_to_csv(data, filename)`: Export data to CSV format
- `save_to_json(data, filename)`: Export data to JSON format
- `scrape_website(url, ...)`: Complete scraping workflow

## Data Cleaning Features

The scraper automatically:
- Removes extra whitespace and special characters
- Standardizes column names (Name, Location, Year)
- Extracts years from date strings using regex patterns
- Handles various data formats and inconsistencies
- Filters out empty or invalid records

## Respectful Scraping Practices

- Configurable delays between requests (default: 1 second)
- Proper User-Agent headers
- Request timeouts to prevent hanging
- Error handling for network issues
- Logging for monitoring and debugging

## Example Use Cases

1. **Public Records**: Scraping government databases, directories
2. **Research Data**: Academic publications, conference proceedings  
3. **Business Directories**: Company listings, contact information
4. **Event Data**: Conference attendees, award recipients
5. **Historical Data**: Archive websites, timeline data

## Error Handling

The scraper includes comprehensive error handling:
- Network timeouts and connection errors
- Invalid HTML parsing
- Missing data fields
- File I/O errors
- Logging for debugging

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Disclaimer

This tool is designed for scraping publicly available data. Please ensure you:
- Respect robots.txt files
- Follow website terms of service
- Use appropriate delays between requests
- Only scrape public, non-copyrighted data
- Comply with applicable laws and regulations

## Support

For issues, questions, or contributions, please open an issue on GitHub.