from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

class_colors = {
    "Druid": "255, 125, 10",
    "Paladin": "100, 200, 50",
    "Monk": "30, 150, 200",
    "Evoker": "255, 0, 255",
    "Warrior": "200, 50, 50",
    "Priest": "0, 150, 200",
    "Shaman": "0, 112, 222"
}

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

# Read links from a file
with open('raidbot_links.txt', 'r') as file:
    links = file.readlines()

# Open a CSV file to write data
with open('output.csv', mode='w', newline='') as csv_file:
    fieldnames = ['Nickname', 'Parsed Class', 'DPS Values', 'Percentage Difference', 'Item Name', 'Item ID', 'Item Level']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    for link in links:
        driver.get(link.strip())  # Strip to remove leading/trailing whitespaces

        try:
            # Find and extract the nickname from the original page
            nickname_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h1.Heading"))
            )
            nickname = nickname_element.text.strip()
            print("Nickname:", nickname)

            # Find the specific div element containing class information
            class_info_div = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.Box"))
            )

            # Find the paragraph containing the class information within the div
            class_paragraph = class_info_div.find_element(By.CSS_SELECTOR, "p.Text")

            # Extract the text from the paragraph
            class_text = class_paragraph.text.strip()

            # List of strings to check for in the extracted text
            class_strings = [
                "Shaman",
                "Warrior",
                "Evoker",
                "Priest",
                "Warlock",
                "Mage",
                "Hunter",
                "Druid"
                # Add more strings as needed
            ]

            # Check if any of the strings are present in the extracted text and assign it to parsed_class
            parsed_class = None
            for string in class_strings:
                if string in class_text:
                    parsed_class = string
                    break

            if parsed_class:
                print("Parsed Class:", parsed_class)

                # Wait for the elements to be present in the DOM
                dps_elements = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, f"p.Text[style*='color: rgb({class_colors[parsed_class]});']"))
                )

                # Extract the text content from the elements
                dps_values = [element.text.strip().replace(',', '') for element in dps_elements]
                print("DPS values:", dps_values)

                # Convert the values to integers
                dps_values = list(map(int, dps_values))

                # Calculate percentage difference from first number to the second number
                percentage_difference = ((dps_values[0] - dps_values[1]) / dps_values[1]) * 100
                # Round the percentage to two decimal places
                percentage_difference_rounded = round(percentage_difference, 2)
                print("Percentage difference:", percentage_difference_rounded)

                # Find all links once
                links = driver.find_elements(By.XPATH, "//*[contains(@href, 'wowhead.com/item=')]")

                closest_link = None
                closest_distance = float('inf')

                for dps_element in dps_elements:
                    for link in links:
                        # Calculate vertical distance between DPS element and link
                        distance = abs(dps_element.location['y'] - link.location['y'])
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_link = link.get_attribute("href")

                if closest_link:
                    print("Closest Wowhead Link:", closest_link)
                    # Extract item name from the closest Wowhead link
                    driver.get(closest_link)
                    item_name_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "h1.heading-size-1"))
                    )
                    item_name = item_name_element.text.strip()
                    print("Item Name:", item_name)

                    # Extract item ID and item level from the URL
                    item_id = closest_link.split('/item=')[1].split('?')[0]  # Extracting item ID
                    item_level = closest_link.split('ilvl=')[1].split('&')[0]  # Extracting item level from the URL

                    print("Item ID:", item_id)
                    print("Item Level:", item_level)
                else:
                    print("No Wowhead link found near the DPS elements.")

            else:
                print("Class not found in the text.")
            row_data = {
                'Nickname': nickname,
                'Parsed Class': parsed_class,
                'DPS Values': dps_values,
                'Percentage Difference': percentage_difference_rounded,
                'Item Name': item_name,
                'Item ID': item_id,
                'Item Level': item_level
            }

            writer.writerow(row_data)  # Write data to the CSV file   

        except Exception as e:
            print("Error:", e)

# Close the browser
driver.quit()
