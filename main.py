import os
import re
import pandas as pd
from sqlalchemy import create_engine
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, accuracy_score
from dotenv import load_dotenv
from urllib.parse import quote_plus
import joblib

nltk.download("stopwords")
nltk.download("wordnet")
nltk.download("omw-1.4")

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "sentiment_db")
CSV_PATH = os.getenv("CSV_PATH", "data/twitter_training.csv")

def get_engine():
    url = f"mysql+mysqlconnector://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

def load_csv():
    df = pd.read_csv(
        CSV_PATH,
        header=None,
        names=["tweet_id", "topic", "sentiment_label", "tweet_text"],
        encoding_errors="ignore"
    )
    return df

def save_raw_to_sql(df, engine):
    df.to_sql("twitter_comments", con=engine, if_exists="replace", index=False)

def fetch_from_sql(engine):
    query = """
    SELECT tweet_id, topic, sentiment_label, tweet_text
    FROM twitter_comments
    WHERE tweet_text IS NOT NULL
    """
    return pd.read_sql(query, engine)

stop_words = set(stopwords.words("english"))
lemmatizer = WordNetLemmatizer()

def clean_text(text):
    text = str(text)
    text = re.sub(r"http\S+|www\S+", "", text)
    text = re.sub(r"@[A-Za-z0-9_]+", "", text)
    text = re.sub(r"#", "", text)
    text = text.lower()
    text = re.sub(r"[^a-z\s]", " ", text)
    tokens = text.split()
    tokens = [t for t in tokens if t not in stop_words and len(t) > 2]
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    return " ".join(tokens)

def prepare_data(df):
    df = df.copy()
    df["clean_text"] = df["tweet_text"].apply(clean_text)
    df = df.dropna(subset=["sentiment_label", "clean_text"])
    df = df[df["clean_text"].str.len() > 0]
    return df

def train_model(df):
    print("Original label distribution:")
    print(df["sentiment_label"].value_counts())

    df_bal = pd.DataFrame({
        "text": df["clean_text"],
        "label": df["sentiment_label"]
    })

    min_size = df_bal["label"].value_counts().min()
    print("\nBalancing classes to size:", min_size)

    df_bal = (
        df_bal
        .groupby("label", group_keys=False)
        .apply(lambda x: x.sample(min_size, random_state=42))
        .reset_index(drop=True)
    )

    print("\nBalanced label distribution:")
    print(df_bal["label"].value_counts())

    X_bal = df_bal["text"]
    y_bal = df_bal["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X_bal, y_bal, test_size=0.2, random_state=42, stratify=y_bal
    )

    vectorizer = TfidfVectorizer(max_features=20000, ngram_range=(1, 2))
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = LogisticRegression(max_iter=1000, class_weight="balanced")
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nClassification report:")
    print(classification_report(y_test, y_pred))

    return vectorizer, clf

def score_all(df, vectorizer, clf):
    X_all = df["clean_text"]
    X_all_vec = vectorizer.transform(X_all)
    df["predicted_sentiment"] = clf.predict(X_all_vec)
    return df

def save_scored_to_sql(df, engine):
    df_to_save = df[
        [
            "tweet_id",
            "topic",
            "sentiment_label",
            "tweet_text",
            "clean_text",
            "predicted_sentiment",
        ]
    ]
    df_to_save.to_sql("twitter_comments_scored", con=engine, if_exists="replace", index=False)

def main():
    if not DB_USER or not DB_PASSWORD:
        raise ValueError("Database credentials not set. Check your .env file.")

    print("Connecting to MySQL...")
    print(f"HOST = {DB_HOST}, PORT = {DB_PORT}, USER = {DB_USER}, DB = {DB_NAME}")

    engine = get_engine()

    df_csv = load_csv()
    print("CSV loaded:", df_csv.shape)

    save_raw_to_sql(df_csv, engine)
    print("Raw data saved to MySQL table 'twitter_comments'.")

    df_sql = fetch_from_sql(engine)
    print("Data fetched from MySQL:", df_sql.shape)

    df_clean = prepare_data(df_sql)
    print("After cleaning:", df_clean.shape)

    vectorizer, clf = train_model(df_clean)

    joblib.dump(vectorizer, "vectorizer.pkl")
    joblib.dump(clf, "sentiment_model.pkl")
    print("✅ Model and vectorizer saved successfully!")

    df_scored = score_all(df_clean, vectorizer, clf)
    print("Scoring completed. Sample:")
    print(df_scored.head())

    save_scored_to_sql(df_scored, engine)
    print("Scored data saved to MySQL table 'twitter_comments_scored'.")

if __name__ == "__main__":
    main()
