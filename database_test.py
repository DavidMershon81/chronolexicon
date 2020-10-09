from datetime import date
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

db = SQLAlchemy(app)


class DatedWordRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(50))
    first_use_date = db.Column(db.SmallInteger)
    first_use_known = db.Column(db.Boolean)
    lookup_date = db.Column(db.Date, default=date.today())
    blup = db.Date


@app.route("/add_word/<word>/<first_use_date>/<first_use_known_raw>")
def add_word(word, first_use_date, first_use_known_raw):
    first_use_known = first_use_known_raw.lower() == "true"
    dwr = DatedWordRecord(word=word, first_use_date=first_use_date, first_use_known=first_use_known)
    db.session.add(dwr)
    db.session.commit()
    return "<h1>Added New Word to DB!</h1>"


@app.route("/get_word/<word>")
def get_word(word):
    dwr = DatedWordRecord.query.filter_by(word=word).first()
    queries_today = len(DatedWordRecord.query.filter_by(lookup_date=date.today()).all())

    if dwr:
        return f"<p>word: { dwr.word }<br>first_use_date: { dwr.first_use_date }<br>first_use_known: { dwr.first_use_known }<br>lookup_date: { dwr.lookup_date }"\
            f"<br>queries_today: { queries_today }</p>"
    else:
        return f"<p>{ word } isn't in the database</p>"\
            f"<br>queries_today: { queries_today }</p>"