import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib


combined = pd.read_csv("Combined_dfs.csv")

X = combined["clean_text"]
y = combined ["label"]
source = combined ["Source"]

#Vectorization

vectorizer = TfidfVectorizer(max_features =5000)
X_vectorized = vectorizer.fit_transform(X)

#Splitting the data into training and testing setts
X_train, X_test, y_train, y_test, source_train, source_test = train_test_split( X_vectorized, y, source, test_size=0.2, random_state=42)

#Training with Logistic regression and tuning hyperparameters:
params = {"C":[0.01, 0.1, 1, 10], "max_iter":[100, 200, 300]}
Grid = GridSearchCV(LogisticRegression(solver="lbfgs"), params, cv=3,verbose=1)
Grid.fit(X_train, y_train)
best_model =Grid.best_estimator_

#predicting and Evaluating the model

y_pred= best_model.predict(X_test)

print("Best params:", Grid.best_params_)
print("Accuracy:", accuracy_score(y_test, y_pred))
print("report:", classification_report(y_test, y_pred))
print ("Confusion matrix:\n", confusion_matrix(y_test, y_pred))

print(len(y_test), len(y_pred), len(source_test))


df_results = pd.DataFrame({
    "True_label": y_test.reset_index(drop=True),
    "predicted_label": pd.Series(y_pred),
    "source": source_test.reset_index(drop=True)
})
print (df_results.groupby("source")["predicted_label"].value_counts().unstack(fill_value=0))

# 9. Save prediction breakdown
df_results.to_csv("model_predictions_by_source.csv", index=False)

# Save the model and vectorizer
joblib.dump(best_model, "sentiment_model_logreg.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer_logreg.pkl")

