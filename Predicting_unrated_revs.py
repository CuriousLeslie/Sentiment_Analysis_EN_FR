
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib

# Load the saved model
model = joblib.load("sentiment_model_logreg.pkl")
vectorizer = joblib.load("tfidf_vectorizer_logreg.pkl")

 #Load unrated Shein French and English reviews
shein_fr_unrated = pd.read_csv("shein_unrated_fr_cleaned.csv")
print(shein_fr_unrated.head())
shein_fr_unrated["clean_text"] = shein_fr_unrated["clean_text"].astype(str).fillna("")

shein_en_unrated = pd.read_csv("shein_en_cleaned.csv")
print(shein_en_unrated.head())
shein_en_unrated["clean_text"] = shein_en_unrated["clean_text"].astype(str).fillna("")



# Vectorize clean text
X_fr_unrated = vectorizer.transform(shein_fr_unrated["clean_text"])
X_en_unrated = vectorizer.transform(shein_en_unrated["clean_text"])

# Predicting sentiment
shein_fr_unrated["predicted_sentiment"] = model.predict(X_fr_unrated)
shein_en_unrated["predicted_sentiment"] = model.predict(X_en_unrated)

df_shein_fr = shein_fr_unrated[["clean_text", "predicted_sentiment"]]
df_shein_en = shein_en_unrated[["clean_text", "predicted_sentiment"]]

# Saving the predictions to CSV
df_shein_fr.to_csv("shein_fr_unrated_predictions.csv", index=False)
df_shein_en.to_csv("shein_en_unrated_predictions.csv", index=False)

print("Predictions completed and saved.")