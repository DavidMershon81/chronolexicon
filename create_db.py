#run this script to create the SQLite databse for the first time
#this must be done before the first time you launch Chronolexicon

from app import word_db
word_db.db.create_all()