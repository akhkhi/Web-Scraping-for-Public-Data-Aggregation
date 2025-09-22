#!/usr/bin/env python3
"""
Simple test script to validate the web scraping functionality.
"""

import os
import sys
import tempfile
from web_scraper import WebScraper


def test_data_cleaning():
    """Test the data cleaning functionality."""
    print("Testing data cleaning...")
    
    scraper = WebScraper()
    
    # Test data with various inconsistencies
    test_data = [
        {
            'full_name': '  John  Smith  ',
            'city': 'New York',
            'graduation_year': '2023'
        },
        {
            'person_name': 'Maria Garcia',
            'location': 'Los Angeles, CA',
            'year_completed': 'May 2022'
        },
        {
            'name': 'David Johnson',
            'place': 'Chicago',
            'date': '12/15/2023'
        }
    ]
    
    cleaned = scraper.clean_data(test_data)
    
    # Validate cleaning
    assert len(cleaned) == 3, f"Expected 3 records, got {len(cleaned)}"
    assert all('Name' in record for record in cleaned), "All records should have 'Name' field"
    assert all('Location' in record for record in cleaned), "All records should have 'Location' field"
    assert all('Year' in record for record in cleaned), "All records should have 'Year' field"
    
    print("✓ Data cleaning test passed")
    return cleaned


def test_csv_export():
    """Test CSV export functionality."""
    print("Testing CSV export...")
    
    scraper = WebScraper()
    
    test_data = [
        {'Name': 'John Smith', 'Location': 'New York, NY', 'Year': '2023'},
        {'Name': 'Maria Garcia', 'Location': 'Los Angeles, CA', 'Year': '2022'}
    ]
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        temp_csv = f.name
    
    try:
        scraper.save_to_csv(test_data, temp_csv)
        
        # Verify file was created and has content
        assert os.path.exists(temp_csv), "CSV file should be created"
        
        with open(temp_csv, 'r') as f:
            content = f.read()
            assert 'Name,Location,Year' in content, "CSV should have headers"
            assert 'John Smith' in content, "CSV should contain data"
            assert 'Maria Garcia' in content, "CSV should contain data"
        
        print("✓ CSV export test passed")
        
    finally:
        # Clean up
        if os.path.exists(temp_csv):
            os.unlink(temp_csv)


def test_json_export():
    """Test JSON export functionality."""
    print("Testing JSON export...")
    
    scraper = WebScraper()
    
    test_data = [
        {'Name': 'John Smith', 'Location': 'New York, NY', 'Year': '2023'},
        {'Name': 'Maria Garcia', 'Location': 'Los Angeles, CA', 'Year': '2022'}
    ]
    
    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_json = f.name
    
    try:
        scraper.save_to_json(test_data, temp_json)
        
        # Verify file was created and has valid JSON
        assert os.path.exists(temp_json), "JSON file should be created"
        
        import json
        with open(temp_json, 'r') as f:
            loaded_data = json.load(f)
            assert len(loaded_data) == 2, "JSON should contain 2 records"
            assert loaded_data[0]['Name'] == 'John Smith', "JSON should contain correct data"
        
        print("✓ JSON export test passed")
        
    finally:
        # Clean up
        if os.path.exists(temp_json):
            os.unlink(temp_json)


def test_html_parsing():
    """Test HTML parsing with mock HTML."""
    print("Testing HTML parsing...")
    
    from bs4 import BeautifulSoup
    
    scraper = WebScraper()
    
    # Mock HTML table
    html_content = """
    <html>
    <body>
        <table>
            <tr>
                <th>Name</th>
                <th>Location</th>
                <th>Year</th>
            </tr>
            <tr>
                <td>John Smith</td>
                <td>New York, NY</td>
                <td>2023</td>
            </tr>
            <tr>
                <td>Maria Garcia</td>
                <td>Los Angeles, CA</td>
                <td>2022</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    soup = BeautifulSoup(html_content, 'html.parser')
    extracted_data = scraper.extract_table_data(soup)
    
    assert len(extracted_data) == 2, f"Expected 2 records, got {len(extracted_data)}"
    assert extracted_data[0]['Name'] == 'John Smith', "First record should be John Smith"
    assert extracted_data[1]['Location'] == 'Los Angeles, CA', "Second record location should match"
    
    print("✓ HTML parsing test passed")


def run_all_tests():
    """Run all tests."""
    print("Running Web Scraper Tests")
    print("=" * 30)
    
    try:
        test_data_cleaning()
        test_csv_export()
        test_json_export()
        test_html_parsing()
        
        print("\n" + "=" * 30)
        print("✅ All tests passed!")
        print("\nFunctionality verified:")
        print("✓ Data extraction and cleaning")
        print("✓ CSV file generation")
        print("✓ JSON file generation")
        print("✓ HTML table parsing")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)