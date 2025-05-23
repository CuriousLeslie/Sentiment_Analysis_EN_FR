
# Importing Required Librariesfrom selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
import csv
import re



edge_driver_path = r"C:\Users\tijsd\Documents\PYTHON LESLIE\msedgedriver.exe"

options = Options()
options.add_argument("--headless")

service = Service(edge_driver_path)
driver = webdriver.Edge(service =service, options=options)

# Setting Up WebDriver Options

base_url = "https://fr.trustpilot.com/review/www.shein.com"

all_reviews =[]
# Scraping Reviews from Multiple Pages
for page in range (101, 169):
    print (f"Scraping page{page + 100}...")
    url =f"{base_url}?page={page}"


    driver.get(url)
    time.sleep(6)

    review_blocks = driver.find_elements(By.CLASS_NAME, "styles_reviewContent__SCYfD")
    print (f"Found {len(review_blocks)} reviews on page {page}")

    # Extracting Review Titles and Bodies
    for block in review_blocks:
        try:
            title = block.find_element(By.TAG_NAME, "h2").text.strip()
        except:
            title = ""
        try:
            body = block.find_element(By.TAG_NAME, "p").text.strip()
        except:
            body = ""
        
        all_reviews.append((title, body,))
print( f"Number of reviews found: {len(all_reviews)}")

# Saving Reviews to CSV File
with open("shein_FR_revs_no_ratings.csv", "w", newline ="", encoding= "utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Titre", "Texte",])
    writer.writerows(all_reviews)

# Closing the WebDriver
driver.quit()

#The styles card class "styles_reviewContent__SCYfD" change every now and then, so you might need to update the class names and tags in the code.
