import os
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from login_required import login_required
from word_age_info import find_word_age

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

    test_word = "engineer"
    processed_json = find_word_age(test_word)        
    return render_template("index.html", test_word=test_word, processed_json=processed_json)


@app.route("/test_login_required")
@login_required
def test_login_required():
    """Test login required page"""
    return "Test rendering index page"


@app.route("/login")
def login():
    """Test route login"""
    return "Test rendering login page"


