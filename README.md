# MagicBricks Real Estate Scraper

Scrapes live residential property listings from MagicBricks.com for Bangalore, 
handling infinite scroll loading and inconsistent data across listings.

## What it extracts
- Property title
- Price
- Carpet area or super area (with fallback logic when one is missing)
- Area type (labeled as "Carpet Area" or "Super Area")

## Tools used
- Selenium — opens the site, waits for dynamic content, handles infinite scroll
- BeautifulSoup — extracts data from each property card
- Pandas — combines results and exports to Excel

## Real-world challenges handled
- **Infinite scroll** — listings load progressively as you scroll, so the 
  scraper programmatically scrolls and waits for new content before reading 
  the page
- **Shared CSS classes** — multiple fields on the same card share identical 
  class names, so fields are targeted using their unique `data-summary` 
  attribute instead of class alone
- **Inconsistent listings** — not every property lists "Carpet Area"; some 
  only show "Super Area" instead, handled with fallback logic so no data is 
  silently lost

## Setup
pip install -r requirements.txt

## Output
Excel file with one row per property listing.

## Sample Output
See the included `.xlsx` file for a real example of scraped data, captured 
at the time of this commit. 

Note: live listings change over time, so re-running the scraper will return different results.
