# B2B Events Scraper

## Overview

This project is a web scraper designed to collect detailed information about B2B (Business-to-Business) events from various websites. The data is compiled and stored in a CSV file for easy access and analysis.

## Data Collected

For each event, the following details are collected:
- **Event Name**
- **Event Date(s)**
- **Location**
- **Description**
- **Key Speakers**
- **Agenda/Schedule**
- **Registration Details**
- **Pricing**
- **Categories**
- **Audience Type**
- **Website URL**

## Prerequisites

Ensure you have the following installed:
- Python 3.x
- `requests` library
- `beautifulsoup4` library

You can install the required libraries using pip:
```bash
pip install requests beautifulsoup4
```

## Running the Code

1. **Clone the repository or download the script:**

   Download the script to your local machine.

2. **Ensure the event URLs are up-to-date:**

   Check and update the event URLs in the `event_urls` list within the script to ensure they point to the correct event pages you wish to scrape.

3. **Run the script:**

   Execute the script using Python:
   ```bash
   python b2b_events_scraper.py
   ```

4. **Output:**

   The script will generate a CSV file named `b2b_events.csv` containing the collected event data.

## File Structure

The script uses the following functions to scrape data:

- **get_soup(url):** Sends a GET request to the provided URL and returns a BeautifulSoup object for parsing the HTML content.
- **scrape_b2b_marketingleaders(soup):** Extracts event details from `b2bmarketingleaders.com.au`.
- **scrape_pavilion(soup):** Extracts event details from `joinpavilion.com`.
- **scrape_eventbrite(soup):** Extracts event details from `eventbrite.com`.
- **scrape_marketing_ai(soup):** Extracts event details from `marketingaiinstitute.com`.
- **scrape_saastr(soup):** Extracts event details from `saastrannual2024.com`.
- **scrape_event_data(url):** Determines the appropriate scraping function based on the URL and returns the event data.

Each function is tailored to handle the specific HTML structure of its corresponding website, ensuring accurate data extraction.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to create a pull request or open an issue in the repository.


---

By following these instructions, you should be able to run the B2B Events Scraper and collect detailed information about B2B events into a CSV file.
