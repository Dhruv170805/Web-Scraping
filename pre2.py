from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

def scrape_business_ranking():
    driver = webdriver.Chrome()

    try:
        url = "https://en.wikipedia.org/wiki/Ease_of_doing_business_index"
        print(f"Opening URL: {url}")
        driver.get(url)
        time.sleep(3)

        print("Scrolling to ranking section...")
        ranking_header = driver.find_element(By.ID, "Ranking")
        driver.execute_script("arguments[0].scrollIntoView();", ranking_header)
        time.sleep(2)

        print("Looking for the ranking table...")
        tables = driver.find_elements(By.TAG_NAME, "table")

        ranking_table = None
        for table in tables:
            if "New Zealand" in table.text and "Singapore" in table.text:
                ranking_table = table
                break

        if ranking_table is None:
            print("Could not find the ranking table!")
            return

        print("Extracting table data...")
        # Extract headers
        header_row = ranking_table.find_element(By.TAG_NAME, "tr")
        headers = [th.text.strip() for th in header_row.find_elements(By.TAG_NAME, "th")]
        print(f"Found headers: {headers}")

        data_rows = []
        rows = ranking_table.find_elements(By.TAG_NAME, "tr")[1:]

        for row in rows:

            cells = row.find_elements(By.XPATH, "./th|./td")
            row_data = []

            for cell in cells:
                text = cell.text.strip()
                if not text:
                    # fallback if cell has no direct text
                    text = cell.get_attribute("textContent").strip()
                row_data.append(text)

            # add row only if not empty
            if any(row_data):
                data_rows.append(row_data)

        print(f"Extracted {len(data_rows)} rows of data")

        if headers and data_rows:
            # Ensure consistent columns
            clean_data = []
            for row in data_rows:
                if len(row) < len(headers):
                    row += [''] * (len(headers) - len(row))
                elif len(row) > len(headers):
                    row = row[:len(headers)]
                clean_data.append(row)

            df = pd.DataFrame(clean_data, columns=headers)
            print(f"\nCOUNTRY NAMES:")
            for i in range(min(10, len(df))):
                print(f"  {i + 1}. {df.iloc[i, 0]}")

            filename = r"C:\Users\dhruv\Desktop\ease_of_doing_business.xlsx"
            df.to_excel(filename, index=False)
            print(f"✅ Data saved successfully to {filename}")
            print(f"Total countries: {len(df)}")

        else:
            print("No data found to save!")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print("Closing browser...")
        driver.quit()

# Main
if __name__ == "__main__":
    print("=== Web Scraper ===")
    time.sleep(2)
    scrape_business_ranking()
