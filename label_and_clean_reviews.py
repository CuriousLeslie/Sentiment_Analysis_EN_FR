import pandas as pd
import nltk
from nltk.corpus import stopwords
import re
from nltk.tokenize import word_tokenize
import string
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Downloading the necessary NLTK data files
nltk.download("punkt")  #for tokenization
nltk.download("stopwords")  #for stopwords

#1. Loading reviews data sets
df_shein_en = pd.read_csv("shein_reviews_selenium.csv")
df_shein_unrated_fr = pd.read_csv("shein_FR_revs_no_ratings.csv")
df_shein_rated_fr = pd.read_csv("scrape_shein_ratings_fr.csv")
df_amazon = pd.read_csv("amazon.csv")
df_yelp =pd.read_csv("yelp_reviews_sample.csv")

for df, name in zip ([df_shein_en, df_shein_unrated_fr, df_shein_rated_fr, df_amazon, df_yelp],["SHEIN_EN", "SHEIN_FR_UNRATED", "SHEIN_FR_RATED", "AMAZON", "YELP"]):
    print (f"\n{name} = {df.shape}")
    print (f"\n{name} = {df.head()}")
    print(f"{name} = total reviews: {len(df)}")
    print (f"\n {name} = {df.isnull().sum()}")
    

#Quick overview of the datasets
print (df_shein_en.shape, df_shein_unrated_fr.shape, df_shein_rated_fr.shape, df_amazon.shape, df_yelp.shape)
print (df_shein_en.head(), df_shein_unrated_fr.head(), df_shein_rated_fr.head(), df_amazon.head(), df_yelp.head())

print (df_shein_en["Body"].isnull().sum())
print (df_shein_rated_fr[["Texte", "Etoiles"]].isnull().sum())
print (df_shein_unrated_fr["Texte"].isnull().sum())
print (df_amazon[["text", "label"]].isnull().sum())
print (df_yelp[["text", "stars"]].isnull().sum())

#Function to convert starts to labels 1 or 0
# 1 for positive, 0 for negative
# 3 stars are considered neutral and are not included in the labels
def stars_to_labels(star):
    if star >= 4:
        return 1
    elif star <= 2:
        return 0
    else:
        return None
    
# Function to clean and remove stopwords from the text
# This function takes a text and a language as input, cleans the text by removing punctuation.
# It also removes stopwords based on the specified language (French or English).
# The cleaned text is returned as a string.
def clean_and_remove_stopwords(text, language):
    text = text.lower()
    text = text.translate(str.maketrans("","", string.punctuation))
    text =re.sub(r"\s+[a-zA-Z]\s+", " ", text)
    text = re.sub(r"\s+", " ", text)
    words = word_tokenize(text)
    stop_words = stopwords.words("french") if language =="fr" else stopwords.words("english")
    words =[word for word in words if word not in stop_words]
    return " ".join(words)

 # Cleaning and labeling yelp the dataset   
print("Cleaning Yelp...")  #helps to see the progress
df_yelp =df_yelp.dropna(subset=["text", "stars"])
df_yelp["stars"]= df_yelp["stars"].astype(int)
df_yelp["label"] = df_yelp["stars"].apply(stars_to_labels)
df_yelp = df_yelp.dropna(subset=["label"])
df_yelp["label"] = df_yelp["label"].astype(int)
df_yelp = df_yelp.dropna(subset=["text"])
df_yelp["language"] = "en"

# Cleaning and labeling shein dataset with ratings  
print("Cleaning Shein french rated...") 
df_shein_rated_fr = df_shein_rated_fr.dropna(subset=["Texte", "Etoiles"])
df_shein_rated_fr["text"] = df_shein_rated_fr["Titre"] + " " + df_shein_rated_fr["Texte"]
df_shein_rated_fr["label"]= df_shein_rated_fr["Etoiles"].astype(int)
df_shein_rated_fr["label"] = df_shein_rated_fr["label"].apply(stars_to_labels)
df_shein_rated_fr = df_shein_rated_fr.dropna(subset = ["label"])
df_shein_rated_fr["label"] = df_shein_rated_fr["label"].astype(int)
df_shein_rated_fr["language"] = "fr"

#Cleaning and labeling shein dataset without ratings
print("Cleaning Shein french unrated...")
df_shein_unrated_fr = df_shein_unrated_fr.dropna(subset = ["Texte"])
df_shein_unrated_fr["text"] = df_shein_unrated_fr["Titre"]+" "+df_shein_unrated_fr["Texte"]
df_shein_unrated_fr["language"] = "fr"

#Cleaning and labeling shein dataset in english
# Shein english with no ratings
print("Cleaning Shein english unrated...")
df_shein_en = df_shein_en.dropna(subset=["Title", "Body"])
df_shein_en["text"] = df_shein_en["Title"] + " " + df_shein_en["Body"]
df_shein_en["language"] = "en"

#Cleaning and labeling amazon dataset 
print("Cleaning Amazon...")
df_amazon = df_amazon.dropna(subset=["text", "label"])
df_amazon["label"] = df_amazon["label"].astype(int)
df_amazon["language"]= "en"

#stopwords
# The stopwords are a set of common words that are often removed from text data during preprocessing.   
# In this case, the stopwords are being loaded for both French and English languages using the NLTK library.
stop_words_fr = set(stopwords.words("french"))
stop_words_en = set(stopwords.words("english"))

#applying the function to clean and remove stopwords from the text columns
# The clean_and_remove_stopwords function is applied to the "text" column of each dataset.
# The cleaned text is stored in a new column called "clean_text".

df_amazon["clean_text"] = df_amazon.apply(lambda x: clean_and_remove_stopwords(x["text"], x["language"]), axis=1)
df_yelp["clean_text"] = df_yelp.apply(lambda x: clean_and_remove_stopwords(x["text"], x["language"]), axis=1)
df_shein_rated_fr["clean_text"] = df_shein_rated_fr.apply(lambda x: clean_and_remove_stopwords(x["text"], x["language"]), axis=1)
df_shein_unrated_fr["clean_text"] = df_shein_unrated_fr.apply (lambda x: clean_and_remove_stopwords(x["text"], x["language"]), axis=1)
df_shein_en["clean_text"] = df_shein_en.apply(lambda x:clean_and_remove_stopwords(x["text"], x["language"]), axis=1)

# Saving the cleaned datasets to CSV files

df_amazon.to_csv("amazon_cleaned.csv", index=False)
df_yelp.to_csv("yelp_cleaned.csv", index=False)
df_shein_rated_fr.to_csv("shein_rated_fr_cleaned.csv", index=False)
df_shein_en.to_csv("shein_en_cleaned.csv", index=False)
df_shein_unrated_fr.to_csv("shein_unrated_fr_cleaned.csv", index=False)
print ("All datasets cleaned and saved to csv.")

Amazon_df = pd.read_csv("amazon_cleaned.csv", encoding="utf-8")
yelp_df = pd.read_csv("yelp_cleaned.csv", encoding="utf-8")
shein_df = pd.read_csv("shein_rated_fr_cleaned.csv", encoding='utf-8')

Amazon_df["Source"] = "Amazon"
yelp_df["Source"] = "yelp"
shein_df["Source"] = "Shein"

print("combining dataframes..")
combined_df = pd.concat([Amazon_df, yelp_df, shein_df], ignore_index=True)
combined_df.drop(["stars", "Titre", "Texte", "Etoiles"], axis=1, inplace=True)
combined_df = combined_df.dropna(subset=["clean_text", "label"])
combined_df["label"] = combined_df["label"].astype(int)
combined_df["clean_text"] = combined_df["clean_text"].astype(str)
combined_df.to_csv("Combined_dfs.csv", encoding ="utf-8", index=False)

print("combined dataframes..")

