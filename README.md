Sentiment Analysis of Customer Reviews: A Self-Taught Journey into NLP
This project marks a significant milestone in my self-directed learning journey into the world of data science and Natural Language Processing (NLP). Coming from a background in Political Science, I embarked on this project to develop and showcase practical skills in a new domain, from data acquisition and wrangling to machine learning model development.

The project implements a complete pipeline for sentiment analysis of customer reviews. It leverages Python and key data science libraries to classify reviews as positive or negative, with a focus on Shein reviews (English and French) and incorporating datasets from Amazon and Yelp to build a more robust model.

1.Project Goals:
To apply and demonstrate self-taught skills in web scraping, data cleaning, text preprocessing, and machine learning.
To build an end-to-end NLP project, from raw data collection to a predictive model.
To explore the nuances of sentiment in multilingual customer feedback.
To gain practical experience with industry-standard data science tools and workflows.

2.Key Features:
  *Web Scraping:
Dynamically scrapes customer reviews (titles, bodies, ratings) from Trustpilot using Selenium. Includes dedicated scrapers for Shein (English and French, rated and unrated reviews).
  *Data Cleaning & Preprocessing:
Loads reviews from various CSV files (Shein, Amazon, Yelp).
Converts star ratings into binary sentiment labels (positive/negative), treating 3-star reviews as neutral and excluding them.
Cleans text data by converting to lowercase, removing punctuation, and eliminating stopwords for both English and French.
Combines multiple cleaned datasets into a unified dataset for model training.
  *Exploratory Data Analysis (EDA):
Performs EDA on cleaned datasets to understand review characteristics, including label distribution, word counts (raw vs. clean), and most frequent words.
Visualizes word count distributions using histograms.
  *Sentiment Analysis Model:
Utilizes TfidfVectorizer for text feature extraction.
Trains a Logistic Regression classifier for sentiment prediction.
Optimizes hyperparameters using GridSearchCV.
Evaluates model performance using accuracy, classification reports, and confusion matrices.
Saves and loads the trained model and vectorizer using joblib for reusability.
  *Prediction on Unrated Reviews:
Applies the trained sentiment model to predict sentiment labels for previously unrated Shein reviews (both French and English).

3.Workflow:
  *Scraping: scrape_shein_ratings_fr.py, selenium_shein_scraper.py, shein_fr_reviews_no_ratings.py collect review data.
  *Cleaning & Labeling: label_and_clean_reviews.py processes the raw data, cleans text, assigns sentiment labels, and creates a combined dataset (Combined_dfs.csv).
  *EDA: Sent_analysis_eda.py provides insights into the cleaned datasets.
  *Model Training: MLproject1_SentAnal.py trains and evaluates the sentiment analysis model using the combined dataset.
  *Prediction: Predicting_unrated_revs.py uses the saved model to predict sentiment on new, unrated reviews.

4.Technologies Used:
-Python 3.12
-Web Scraping: Selenium
-Data Handling & Analysis: Pandas, NumPy
-NLP & Text Processing: NLTK, Scikit-learn (TfidfVectorizer)
-Machine Learning: Scikit-learn (LogisticRegression, GridSearchCV, metrics)
-Model Persistence: Joblib
-Visualization: Matplotlib, Seaborn

5.Datasets:
The project works with customer reviews from:
Shein (English and French, scraped from Trustpilot)
Amazon (English)
Yelp (English)
