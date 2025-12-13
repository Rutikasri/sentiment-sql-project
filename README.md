# 💬 Sentiment Analysis on Social Media Posts (SQL + Flask)

## 🧩 Project Overview

This project focuses on **analyzing sentiments behind social media posts** — identifying whether a user’s comment or tweet expresses a **Positive**, **Negative**, or **Neutral** emotion.  
It demonstrates how **Natural Language Processing (NLP)** can be integrated with **Flask** (Python web framework) and **MySQL** (database) to create a full-stack real-time analysis system.

The purpose of this project is to build an intelligent system that can help businesses, content creators, and researchers **understand public opinion** on a topic, product, or event by analyzing the tone of user-generated content.

---

## 🎯 Objective

- To develop a **web-based sentiment analysis application** using **Flask** and **SQL**.  
- To apply **Natural Language Processing techniques** for analyzing textual data.  
- To provide a **real-time interface** where users can enter any text (e.g., a tweet, review, or post) and instantly receive the sentiment result.  
- To store all predictions in a **MySQL database** for future analytics and reporting.  
- To demonstrate a complete **end-to-end integration** of front-end, back-end, and database in one project.

---

## 🔍 Problem Statement

With millions of social media users sharing opinions daily, understanding public sentiment is essential for:

- Businesses to monitor brand reputation  
- Governments to analyze public response to policies  
- Researchers to study public emotions on social issues  

However, raw social media data is **unstructured** and **difficult to interpret** manually.  
This project automates that process using **NLP techniques** and provides a simple, interactive web interface for real-time analysis.

---

## 🧠 Project Purpose

The system is designed to help users:

- Quickly identify the tone of any text (Positive, Negative, Neutral).  
- Visualize and store sentiment data for later reference.  
- Demonstrate how NLP concepts can be applied practically using real-world tools like Flask and SQL.

---

## ⚙️ System Architecture

User Input (Frontend)
↓
Flask Backend (Python)
↓
NLP Rule-Based Sentiment Engine
↓
Result (Positive / Negative / Neutral)
↓
Stored in MySQL Database
↓
Displayed in History Page


---

## 🧰 Technologies Used

| Layer | Technologies |
|--------|---------------|
| **Frontend** | HTML5, CSS3, JavaScript |
| **Backend** | Python (Flask Framework) |
| **Database** | MySQL with SQLAlchemy ORM |
| **NLP Library** | NLTK (for text preprocessing & tokenization) |
| **Environment Management** | Python-dotenv for `.env` security |
| **Version Control** | Git and GitHub |

---

## 📦 Project Modules

### 1. **Frontend (User Interface)**
- A minimal, aesthetic web page built using HTML & CSS.
- Users can type any sentence and get a sentiment prediction.
- Includes a “View History” page to display all past predictions.

### 2. **Backend (Flask Server)**
- Receives input from the frontend.
- Passes the text through a **rule-based NLP model**.
- Returns sentiment results as JSON.
- Stores data (text, sentiment, timestamp) in the MySQL database.

### 3. **Database (MySQL)**
- Stores all user-entered text, predicted sentiment, and creation time.
- Enables data analysis and history tracking.

### 4. **Sentiment Engine**
- Uses rule-based analysis instead of machine learning for simplicity.
- Detects sentiment using keyword and phrase matching logic.
- Handles negations like “not good” → Negative, “not bad” → Positive.
- Classifies text into one of three categories:  
  ✅ Positive ❌ Negative ⚪ Neutral

---

## 🧩 Workflow of the System

1. **User enters text** in the frontend.
2. Flask **receives and processes** the text.
3. NLP function **predicts sentiment** using predefined rules.
4. Result is **displayed instantly** to the user.
5. Input and result are **saved in MySQL**.
6. History page fetches all records from the database.

---

## 🧮 Example Predictions

| Input Sentence | Predicted Output |
|----------------|------------------|
| I absolutely love this app, it’s amazing! | Positive |
| This is the worst app I’ve ever used. | Negative |
| It’s okay, not too good or bad. | Neutral |
| I’m not sure how I feel about this. | Neutral |
| Great work team, everything is perfect! | Positive |

---

## 💾 Database Schema

**Table Name:** `user_predictions`

| Column | Type | Description |
|---------|------|-------------|
| text | TEXT | The user-entered comment or post |
| sentiment | VARCHAR(20) | Sentiment label (Positive/Negative/Neutral) |
| created_at | DATETIME | Timestamp when prediction was made |

---
---

## 🔮 Future Enhancements

| Enhancement | Description |
|--------------|--------------|
| **1. Sentiment Filter** | Add filtering options on the history page to view only Positive, Negative, or Neutral entries. |
| **2. Analytics Dashboard** | Visualize the overall sentiment distribution using bar or pie charts. |
| **3. Real-time Twitter Integration** | Automatically fetch tweets on selected topics or hashtags for sentiment analysis. |
| **4. Advanced Machine Learning Models** | Replace the rule-based engine with Logistic Regression, Naive Bayes, or BERT for improved accuracy. |
| **5. Multi-user Authentication** | Allow users to sign up, log in, and maintain personal sentiment history. |
| **6. Cloud Deployment** | Deploy the complete app on platforms like Render, Railway, or Azure with an online MySQL database. |
| **7. API Development** | Expose REST APIs so other apps can use this sentiment engine programmatically. |

---

## 🧭 Conclusion

This project successfully demonstrates how **Natural Language Processing (NLP)** can be combined with **Flask** and **MySQL** to build a complete sentiment analysis web application.  
It analyzes user-generated content in real time, classifies emotions, and stores results for future reference — showcasing the true potential of data-driven decision-making.

### 🔑 Key Outcomes:
- Integrated **frontend, backend, and database** into one system.  
- Implemented a **rule-based NLP approach** for sentiment prediction.  
- Enabled **data persistence** through MySQL for history tracking.  
- Created a **user-friendly interface** for practical demonstration of AI.  

### 🧩 Learning Experience:
- Understanding of Flask–SQLAlchemy integration.  
- Implementation of real-time NLP on textual data.  
- Secure database connection handling using environment variables.  
- Designing aesthetic and functional front-end pages.

The system provides a solid foundation for future improvements like machine learning–based models, real-time Twitter monitoring, and visual analytics.  
It stands as a complete end-to-end full-stack project demonstrating skills in **Python, SQL, NLP, and Web Development**.

---
## 🏷️ Repository Info

**Repository Name:** `sentiment-sql-project`  
**Created by:** *Rutika Sri*  
**Language:** Python  
**Framework:** Flask  
**Database:** MySQL  
**Topic:** Natural Language Processing, Web Development, Data Storage


