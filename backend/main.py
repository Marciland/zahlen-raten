from flask import Flask

app = Flask(__name__)


@app.route("/save")
def hello_world():
    # saves a played game in the database
    # name + counter
    pass


@app.route("/highscore")
def show_test():
    # returns the scores + names
    pass
