import os
from datetime import date
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from word_age_info import search_api_for_word_first_use, DatedWord
from word_separator import separate_words_and_punctuation, DatedWordPunctuationPair
from regex_helper import regex_find_one_match

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

# Initialize database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)

#start session
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
    """analyze text and return a formatted html file where words are tagged by their first known use"""
    analysis_text = request.form["analysis_text"]

    if analysis_text:
        words_and_punctuation = separate_words_and_punctuation(analysis_text)
        dated_words = [DatedWordPunctuationPair(word=wp[0], punctuation=wp[1], first_use_info=find_first_word_use(wp[0])) for wp in words_and_punctuation]
        analyzed_text_html = render_template("analyzed_text.html", dated_words=dated_words)
        return jsonify({"analyzed_text_html" : analyzed_text_html })

    return jsonify({"error" : "Missing data!"})


#Word parsing and database management functions
def find_first_word_use(word_raw):
    word = word_raw.lower()

    number_match = regex_find_one_match(word, r"\d+")

    if number_match:
        return DatedWord(word_lower=word, first_use=None, was_parsed=False)
    else:
        db_match = find_word_in_db(word)

        if db_match:
            return DatedWord(word_lower=db_match.word, first_use=db_match.first_use_date, was_parsed=db_match.first_use_known)
        else:
            queries_today = find_api_queries_today()
            max_queries_per_day = 1000

            if queries_today >= max_queries_per_day:
                return DatedWord(word_lower=word, first_use=None, was_parsed=False)

            search_result = search_api_for_word_first_use(word)
            add_word_to_db(search_result.word_lower, search_result.first_use, search_result.was_parsed)
            return search_result


def find_word_in_db(word):
    return DatedWordRecord.query.filter_by(word=word).first()


def find_api_queries_today():
    return len(DatedWordRecord.query.filter_by(lookup_date=date.today()).all())


def add_word_to_db(word, first_use_date, first_use_known):
    dwr = DatedWordRecord(word=word, first_use_date=first_use_date, first_use_known=first_use_known)
    db.session.add(dwr)
    db.session.commit()


#Model class for dated word database queries
class DatedWordRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    first_use_date = db.Column(db.SmallInteger)
    first_use_known = db.Column(db.Boolean)
    lookup_date = db.Column(db.Date, default=date.today())