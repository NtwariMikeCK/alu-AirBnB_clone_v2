#!/usr/bin/python3

""" display message at route url"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def greet():
    """Comment"""
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def greet_1():
    """Comment"""
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False):
def c_text(text):
    """Comment"""
    text = text.replace("_", " ")
    return f"C {text}"


@app.route("/python/<text>", strict_slashes=False)
def python_tect(text):
    """Comment"""
    if text:
      text = text.replace("_", " ")
    else:
      text = "is cool"
    return f"Pyhton {text}"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
