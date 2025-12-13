import os
import re
from sqlalchemy import create_engine
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "sentiment_db")

def get_engine():
    url = f"mysql+mysqlconnector://{DB_USER}:{quote_plus(DB_PASSWORD)}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    return create_engine(url)

def predict_sentiment(text: str) -> str:
    t = str(text).lower()

    strong_pos_phrases = [
        "absolutely love",
        "really love",
        "love this",
        "love it",
        "so good",
        "very good",
        "really good",
        "amazing",
        "fantastic",
        "wonderful",
        "great experience",
        "very happy",
        "super happy",
        "excellent",
        "perfect",
        "thank you so much",
    ]

    strong_neg_phrases = [
        "hate this",
        "hate it",
        "worst ever",
        "very bad",
        "really bad",
        "so bad",
        "terrible",
        "horrible",
        "awful",
        "disappointed",
        "very disappointed",
        "waste of time",
        "waste of money",
        "doesn't work",
        "doesnt work",
        "not working at all",
        "keeps crashing",
        "regret using",
        "regret downloading",
    ]

    neutral_phrases = [
        "it's okay",
        "its okay",
        "its ok",
        "it's ok",
        "just okay",
        "just ok",
        "not too good or bad",
        "not very good or bad",
        "nothing special",
        "just average",
        "is average",
        "kind of average",
        "so so",
        "meh",
        "i don't really care",
        "i dont really care",
        "i don't care",
        "i dont care",
        "i'm not sure how i feel",
        "im not sure how i feel",
        "i'm not sure about this",
        "im not sure about this",
        "neither good nor bad",
        "it works, nothing more",
        "works fine",
        "works as expected",
        "okay i guess",
        "ok i guess",
    ]

    for p in neutral_phrases:
        if p in t:
            return "Neutral"

    for p in strong_pos_phrases:
        if p in t:
            return "Positive"

    for p in strong_neg_phrases:
        if p in t:
            return "Negative"

    t = t.replace("not good", "NEGNOTGOOD")
    t = t.replace("not great", "NEGNOTGOOD")
    t = t.replace("not bad", "POSNOTBAD")
    t = t.replace("no good", "NEGNOTGOOD")

    words = re.findall(r"[a-z']+", t)

    pos_words = [
        "good", "great", "nice", "amazing", "love", "loved", "like",
        "happy", "satisfied", "awesome", "cool", "excellent", "enjoyed",
        "better", "best", "fine"
    ]

    neg_words = [
        "bad", "worse", "worst", "hate", "hated", "terrible", "awful",
        "horrible", "annoying", "disappointed", "sad", "problem",
        "issues", "buggy", "slow", "laggy", "useless"
    ]

    pos_count = 0
    neg_count = 0

    for w in words:
        if w == "POSNOTBAD":
            pos_count += 1
        elif w == "NEGNOTGOOD":
            neg_count += 1
        elif w in pos_words:
            pos_count += 1
        elif w in neg_words:
            neg_count += 1

    if pos_count == 0 and neg_count == 0:
        return "Neutral"

    if pos_count > neg_count:
        return "Positive"
    if neg_count > pos_count:
        return "Negative"

    return "Neutral"
