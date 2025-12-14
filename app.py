from flask import Flask, request, jsonify, render_template
from sentiment_model import predict_sentiment, get_engine
import pandas as pd
import datetime

app = Flask(__name__)
history_memory = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "No text provided"}), 400

        text = data["text"]
        print("Received text:", text)

        sentiment = predict_sentiment(text)
        print("Predicted sentiment:", sentiment)

        entry = {
            "text": text,
            "sentiment": sentiment,
            "created_at": datetime.datetime.now()
        }
        history_memory.append(entry)
        print("Stored in memory. Total memory records:", len(history_memory))

        try:
            engine = get_engine()
            df = pd.DataFrame([entry])
            print("About to save to DB...")
            df.to_sql("user_predictions", con=engine, if_exists="append", index=False)
            print("✅ Saved to DB")
        except Exception as db_err:
            print("❌ DB save error (using memory only):", db_err)

        return jsonify({"sentiment": sentiment})
    except Exception as e:
        print("Error in /predict:", e)
        return jsonify({"error": "Internal server error"}), 500

@app.route("/history")
def history():
    records = []
    # First try DB
    try:
        engine = get_engine()
        query = """
        SELECT text, sentiment, created_at
        FROM user_predictions
        ORDER BY created_at DESC
        """
        df = pd.read_sql(query, engine)
        records = df.to_dict(orient="records")
        print("📜 History rows loaded from DB:", len(records))
    except Exception as e:
        print("❌ Error loading history from DB, using memory instead:", e)
        records = history_memory
        print("📜 History rows loaded from memory:", len(records))

    return render_template("history.html", records=records)

if __name__ == "__main__":
    app.run(debug=True)
