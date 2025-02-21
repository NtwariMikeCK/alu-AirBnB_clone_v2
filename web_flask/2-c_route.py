#!/usr/bin/python3
"""display message at route url
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def greet():
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def greet_1():
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False):
def greet_2(text):
    text = text.replace("_", " ")
    return f"C {text}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
