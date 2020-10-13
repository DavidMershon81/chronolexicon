from app import app
from app.word_age_info import DatedWord
from app.word_age_info import search_api_for_word_first_use
from app.regex_helper import regex_find_one_match
from datetime import date
from flask_sqlalchemy import SQLAlchemy


# Initialize database
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
db = SQLAlchemy(app)


#Model class for dated word database queries
class DatedWordRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    first_use_date = db.Column(db.SmallInteger)
    first_use_known = db.Column(db.Boolean)
    lookup_date = db.Column(db.Date, default=date.today())


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