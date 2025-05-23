# Importing Required Libraries
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options
import time
import csv

# Setting Up WebDriver Options
edge_driver_path = r"C:\Users\tijsd\Downloads\edgedriver_win64\msedgedriver.exe"

options = Options()
#options.add_argument("--headless")

service = Service(edge_driver_path)
driver = webdriver.Edge(service =service, options=options)


# Defining Base URL and Output Variables
base_url = "https://www.trustpilot.com/review/www.shein.com"

# Scraping Reviews from Multiple Pages
all_reviews =[]
for page in range (1, 50):
    print (f"Scraping page{page}...")
    if page == 1:
        url = base_url
    else: 
        url =f"{base_url}?page={page}"
    print (f"Opening {url}...")
    driver.get(url)
    time.sleep(6)

# Extracting Review Titles and Bodies
    review_blocks = driver.find_elements(By.CLASS_NAME, "styles_reviewContent__SCYfD")
    print (f"Found {len(review_blocks)} reviews on page {page}")

    for block in review_blocks:
        try:
            title = block.find_element(By.TAG_NAME, "h2").text.strip()
        except:
            title = ""
        try:
            body = block.find_element(By.TAG_NAME, "p").text.strip()
        except:
            body = ""

        all_reviews.append((title, body))
print( f"Number of reviews found: {len(all_reviews)}")

# Saving Reviews to CSV File
with open("shein_reviews_selenium1.csv", "w", newline ="", encoding= "utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Body"])
    writer.writerows(all_reviews)

# Closing the WebDriver
driver.quit()

#The styles card classstyles_reviewContent__SCYfD change every now and then, so you might need to update the class names and tags in the code.
# The code is set to scrape 50 pages, but you can adjust the range in the for loop to scrape more or fewer pages.