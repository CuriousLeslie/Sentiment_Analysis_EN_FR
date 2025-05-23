from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import re
import os

# Importing Required Libraries

chrome_driver_path = r"C:\Users\tijsd\Documents\PYTHON LESLIE\chromedriver-win64\chromedriver-win64\chromedriver.exe"

# Setting Up WebDriver Options

options = Options()
options.add_argument("--headless")

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service =service, options=options)

# Defining Base URL

base_url = "https://fr.trustpilot.com/review/www.shein.com"

# Scraping Reviews from Multiple Pages

all_reviews =[]
for page in range (1, 400):
    print (f"Scraping page{page}...")
    if page == 1:
        url = base_url
    else: 
        url =f"{base_url}?page={page}"


    driver.get(url)
    time.sleep(6)

    review_blocks = driver.find_elements(By.CSS_SELECTOR, "div.styles_cardWrapper__g8amG.styles_show__Z8n7u")
    print (f"Found {len(review_blocks)} reviews on page {page}")

    # Extracting Review Titles, Bodies, and Ratings

    for block in review_blocks:
        try:
            title = block.find_element(By.TAG_NAME, "h2").text.strip()
        except:
            title = ""
        try:
            body = block.find_element(By.TAG_NAME, "p").text.strip()
        except:
            body = ""
        try:
            ratings = block.find_element(By.CSS_SELECTOR, "img[alt*='étoiles']")
            rating_text = ratings.get_attribute("alt").strip()
            match = re.search(r"Noté (\d) sur", rating_text)
            rating = int(match.group(1)) if match else None
        except:
            rating = ""

        all_reviews.append((title, body, rating))
print( f"Number of reviews found: {len(all_reviews)}")

# Saving Reviews to CSV File

with open("scrape_shein_NEW_ratings_fr.csv", "w", newline ="", encoding= "utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Titre", "Texte", "Etoiles"])
    writer.writerows(all_reviews)

# Closing the WebDriver

driver.quit()

# The styles card class "styles_cardWrapper__g8amG styles_show__Z8n7u" change every now and then, so you might need to update the class names and tags in the code.
# The CSS selector for the rating image is "img[alt*='étoiles']", which looks for an image element with an alt attribute containing the word "étoiles".