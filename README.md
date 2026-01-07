# 🕸️ Automated NBA Stats Scraper

A robust web scraping pipeline designed to collect granular basketball data from NBA.com. This tool was built to feed the **Machine Learning Prediction Model** used in my [NBA Outcome Predictor project](https://github.com/eren-baykara/NBA-Match-Outcome-Predictor).

## 🚀 Purpose
Data is the fuel for any AI model. Standard datasets often lack specific details like "First Half Performance" or "Bench Scoring Impact." I built this scraper to:
1.  **Automate Data Collection:** Eliminate manual downloading of CSVs.
2.  **Handle Dynamic Content:** Use **Selenium** to render JavaScript-heavy tables.
3.  **Process Pagination:** Automatically detect and select "All Pages" from dropdowns to get full datasets.

## 🛠️ Technology
* **Python 3.9+**
* **Selenium WebDriver:** For browser automation and DOM interaction.
* **Pandas:** For HTML table parsing and CSV export.
* **Webdriver Manager:** Auto-manages Chrome driver versions.

## ⚙️ How It Works
The script iterates through a configuration dictionary of URLs (`Quarter 1`, `Bench Stats`, `Box Scores`), waits for the dynamic tables to load, handles the "View All" logic, and sanitizes the output into structured CSV files ready for Machine Learning pipelines.

---
*Disclaimer: This tool is for educational and personal research purposes only.*
