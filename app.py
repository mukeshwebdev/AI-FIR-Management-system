from flask import Flask, render_template, request, redirect, session, flash
import sqlite3
import pickle
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from flask import Flask, render_template, request, redirect, session, url_for


app = Flask(__name__)
app.secret_key = "your_secret_key"

# Load NLP Model
with open("legal_nlp_model.pkl", "rb") as f:
    model = pickle.load(f)

# Database Connection
def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/user_dashboard", methods=["GET", "POST"])
def user_dashboard():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        fir_text = request.form["fir_text"]
        processed_text = fir_text.lower()  # Example processing
        predicted_section = model.predict([processed_text])[0]

        conn = get_db_connection()
        conn.execute("INSERT INTO firs (username, fir_text, section) VALUES (?, ?, ?)",
                     (session.get("user"), fir_text, predicted_section))
        conn.commit()
        conn.close()

        flash("Your response has been submitted successfully!", "success")
        return redirect("/user_dashboard")  # Redirect to the same page

    return render_template("user_dashboard.html")

# Text Preprocessing
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

def preprocess_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z\s]", "", text)
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    filtered_tokens = [word for word in tokens if word not in stop_words]
    lemmatizer = WordNetLemmatizer()
    return " ".join(lemmatizer.lemmatize(word) for word in filtered_tokens)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user_type = request.form.get("user_type")

        if not username or not password or not user_type:
            return "All fields are required!", 400

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if username exists
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            conn.close()
            return "Username already exists!", 400

        # Insert new user
        cursor.execute("INSERT INTO users (username, password, user_type) VALUES (?, ?, ?)", 
                       (username, password_hash, user_type))
        conn.commit()
        conn.close()
        return redirect("/login")

    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user"] = username
            session["user_type"] = user["user_type"]
            return redirect(url_for("user_dashboard") if user["user_type"] == "user" else url_for("admin_dashboard"))
        return "Invalid credentials"

    return render_template("login.html")

@app.route("/admin_dashboard")
def admin_dashboard():
    if "user" not in session or session["user_type"] != "admin":
        return redirect("/login")

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM firs")
    firs = cursor.fetchall()
    conn.close()

    return render_template("admin_dashboard.html", firs=firs)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
