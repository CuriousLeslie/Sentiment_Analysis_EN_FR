# 📊 EDA for Cleaned Sentiment Review Datasets
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter

# Load the cleaned datasets
df_amazon = pd.read_csv("amazon_cleaned.csv")
df_yelp = pd.read_csv("yelp_cleaned.csv")
df_shein_fr = pd.read_csv("shein_rated_fr_cleaned.csv")

dataframes = [df_amazon, df_yelp, df_shein_fr]
names = ["Amazon", "Yelp", "Shein"]

# -----------------------------
# Basic Overview and Label Counts
# -----------------------------
for df, name in zip(dataframes, names):
    print(f"\n{name} - Shape: {df.shape}")
    print(f"{name} - Total Reviews: {len(df)}")
    print(df["label"].value_counts())
    print(df["label"].value_counts(normalize=True).round(2))

# -----------------------------
# Word Count Summary Stats
# -----------------------------
for df, name in zip(dataframes, names):
    # Ensure clean_text is string and handle NaNs safely
    df["clean_text"] = df["clean_text"].astype(str).fillna("")
    df["word_count"] = df["clean_text"].apply(lambda x: len(x.split()))
    print(f"\n{name} - Average words per review: {df['word_count'].mean():.2f}")
    print(f"{name} - Min words: {df['word_count'].min()}, Max words: {df['word_count'].max()}")

# -----------------------------
# Raw vs Clean Word Count Analysis + Histogram
# -----------------------------
for df, name in zip(dataframes, names):
    df["text"] = df["text"].astype(str).fillna("")
    df["clean_text"] = df["clean_text"].astype(str).fillna("")
    df["raw_word_count"] = df["text"].apply(lambda x: len(x.split()))
    df["clean_word_count"] = df["clean_text"].apply(lambda x: len(x.split()))
    df["words_removed"] = df["raw_word_count"] - df["clean_word_count"]

    print(f"\n{name} - Avg Raw Words: {df['raw_word_count'].mean():.2f}")
    print(f"{name} - Avg Clean Words: {df['clean_word_count'].mean():.2f}")
    print(f"{name} - Avg Words Removed: {df['words_removed'].mean():.2f}")

    plt.figure(figsize=(10, 4))
    sns.histplot(df["raw_word_count"], bins=50, color="skyblue", label="Raw", kde=True)
    sns.histplot(df["clean_word_count"], bins=50, color="orange", label="Clean", kde=True, alpha=0.7)
    plt.title(f"{name} - Word Count Distribution (Raw vs Clean)")
    plt.xlabel("Number of Words")
    plt.ylabel("Number of Reviews")
    plt.legend()
    plt.tight_layout()
    plt.show()

# -----------------------------
# Top Words in Each Review Dataset
# -----------------------------
for df, name in zip(dataframes, names):
    all_words = " ".join(df["clean_text"].astype(str)).split()
    top_words = Counter(all_words).most_common(20)

    print(f"\nTop 20 most common words in {name} reviews (after cleaning):")
    for word, count in top_words:
        print(f"{word}: {count}")
