import time
import os
from io import StringIO
from typing import Dict

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Constants
TIMEOUT = 25
BASE_URL = "https://www.nba.com"

def setup_driver():
    """Initializes and returns a Chrome WebDriver with specific options."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    # chrome_options.add_argument("--headless") # Uncomment for background execution
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        print(f"Error initializing driver: {e}")
        return None

def scrape_data(driver, dataset_name: str, url: str):
    """
    Navigates to the URL, handles dynamic content loading, and extracts the data table.
    """
    print(f"\n>>> Processing: {dataset_name}")
    print(f"    URL: {url}")
    
    driver.get(url)
    wait = WebDriverWait(driver, TIMEOUT)

    try:
        # Wait for the table to be present in the DOM
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "table")))
        time.sleep(3) # Allow extra time for JS rendering
        
        # Attempt to select "All" from dropdown if it exists (Pagination handling)
        try:
            selects = driver.find_elements(By.TAG_NAME, "select")
            for sel in selects:
                if not sel.is_displayed(): continue
                select_obj = Select(sel)
                options = [opt.text for opt in select_obj.options]
                if "All" in options:
                    select_obj.select_by_visible_text("All")
                    print("    Pagination: 'All' selected.")
                    time.sleep(5) # Wait for table reload
                    break
        except Exception:
            pass # Dropdown interaction failed or not present, continuing with default view

        # Extract Table HTML
        page_source = driver.page_source
        
        # Fallback to Selenium extraction if Pandas read_html fails directly
        try:
            tables = pd.read_html(StringIO(page_source))
        except ValueError:
            print("    Standard parsing failed, trying Selenium element extraction...")
            table_element = driver.find_element(By.TAG_NAME, "table")
            table_html = table_element.get_attribute('outerHTML')
            tables = pd.read_html(StringIO(table_html))

        if tables:
            # The data table is usually the largest one on the page
            target_df = max(tables, key=lambda df: df.shape[0] * df.shape[1])
            
            # Cleanup: Remove unnamed columns
            target_df = target_df.loc[:, ~target_df.columns.str.contains('^Unnamed')]
            
            if not target_df.empty:
                filename = f"{dataset_name}.csv"
                target_df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"    ✅ Success: Saved {filename} ({len(target_df)} rows)")
            else:
                print(f"    ⚠️ Warning: DataFrame is empty for {dataset_name}")
        else:
            print(f"    ❌ Error: No tables found for {dataset_name}")

    except Exception as e:
        print(f"    ❌ Critical Error during scraping {dataset_name}: {e}")

def main():
    links = {
        "Box-Scores": "https://www.nba.com/stats/teams/boxscores",
        "First-Half": "https://www.nba.com/stats/teams/traditional?StarterBench=&GameSegment=First+Half",
        "Quarter-1": "https://www.nba.com/stats/teams/boxscores-traditional?Period=1",
        "Quarter-2": "https://www.nba.com/stats/teams/boxscores-traditional?Period=2",
        "Quarter-3": "https://www.nba.com/stats/teams/boxscores-traditional?Period=3",
        "Quarter-4": "https://www.nba.com/stats/teams/boxscores-traditional?Period=4",
        "Bench-Stats": "https://www.nba.com/stats/teams/traditional?StarterBench=Bench",
    }

    print("Initializing Scraper...")
    driver = setup_driver()
    
    if driver:
        # Initial handshake with the site
        driver.get(BASE_URL)
        time.sleep(2)
        
        for name, url in links.items():
            scrape_data(driver, name, url)
        
        driver.quit()
        print("\n>>> All tasks completed successfully.")

if __name__ == "__main__":
    main()
