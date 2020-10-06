import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from login_required import login_required
from word_age_info import find_word_first_use
from word_separator import separate_words_and_punctuation, DatedWordPunctuationPair

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


# Routing functions
@app.route("/")
def index():
    """route index"""
    return render_template("index.html")


@app.route("/analyze_text_first_use", methods=["POST"])
def analyze_text_first_use():
    analysis_text = request.form["analysis_text"]

    if analysis_text:
        words_and_punctuation = separate_words_and_punctuation(analysis_text)
        dated_words = [DatedWordPunctuationPair(word=wp[0], punctuation=wp[1], first_use_info=find_word_first_use(wp[0])) for wp in words_and_punctuation]
        analyzed_text_html = render_template("analyzed_text.html", dated_words=dated_words)
        return jsonify({"analyzed_text_html" : analyzed_text_html })

    return jsonify({"error" : "Missing data!"})


@app.route("/test_login_required")
@login_required
def test_login_required():
    """Test login required page"""
    return "Test rendering index page"


@app.route("/login")
def login():
    """Test route login"""
    return "Test rendering login page"


