#!/usr/bin/python3
"""display message at route url
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def greet():
    """display hello HBNB! for root
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def greet_1():
    """display HBNB for route /hbnb
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False):
def greet_2(text):
    """display message for route /c/<text>
    """
    text = text.replace("_", " ")
    return f"C {text}"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
