from flask import Flask
from . import db


app = Flask(__name__)
db.init_app(app)

@app.route("/")
def hello_world():
    return "<p>lilypond traveler</p>"

