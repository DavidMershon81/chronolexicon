from app import app
from app.word_db import find_first_word_use
from flask import request, jsonify, render_template
from app.word_utils import separate_words_and_punctuation
from app.word_utils import DatedWordPunctuationPair

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


