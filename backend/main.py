from flask import Flask
from sqlalchemy.orm import Session
from database import create_connection_pool, Player
app = Flask(__name__)

test_database = "test.db"
player_database = "player.db"
connection_pool = create_connection_pool(player_database)


@app.route("/register")
def register():
    # request sends username and password
    return ""


@app.route("/login")
def login():
    # request sends username and password
    # response should contain json with token: token
    return ""


@app.route("/save")
def save_game():
    # saves a played game in the database
    # name + counter
    return ""


@app.route("/highscore")
def get_highscore():
    # returns the scores + names
    return ""
