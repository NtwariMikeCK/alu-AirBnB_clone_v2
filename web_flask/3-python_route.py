#!/usr/bin/python3

"""Script that starts a Flask web application"""
from flask import Flask

app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Comment"""
    return "Hello HBNB!"


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """Comment"""
    return "HBNB"


@app.route('/c/<text>', strict_slashes=False)
def text_var(text):
    """Comment"""
    return "C {}".format(text.replace("_", " "))


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
