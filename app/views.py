from app import app
from flask import request, jsonify, render_template
from app.word_utils import get_dated_words_from_text

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
        dated_words = get_dated_words_from_text(analysis_text)
        analyzed_text_html = render_template("analyzed_text.html", dated_words=dated_words)
        return jsonify({"analyzed_text_html" : analyzed_text_html })

    return jsonify({"error" : "Missing data!"})


