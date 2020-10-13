from app import app
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


def find_word_in_db(word):
    return DatedWordRecord.query.filter_by(word=word).first()


def find_api_queries_today():
    return len(DatedWordRecord.query.filter_by(lookup_date=date.today()).all())


def add_word_to_db(word, first_use_date, first_use_known):
    dwr = DatedWordRecord(word=word, first_use_date=first_use_date, first_use_known=first_use_known)
    db.session.add(dwr)
    db.session.commit()