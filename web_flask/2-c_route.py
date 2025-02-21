#!/usr/bin/python3
"""
A Flask web application with multiple routes.

Routes:
    - `/`: Displays "Hello HBNB!".
    - `/hbnb`: Displays "HBNB".
    - `/c/<text>`: Displays "C " followed by the value of the `text` variable, where underscores (_) are replaced by spaces.
"""

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    """
    Route handler for `/`.
    Displays:
        "Hello HBNB!"
    Returns:
        str: A simple greeting message.
    """
    return 'Hello HBNB!'


@app.route('/hbnb')
def hbnb():
    """
    Route handler for `/hbnb`.
    Displays:
        "HBNB"
    Returns:
        str: The string "HBNB".
    """
    return 'HBNB'


@app.route('/c/<text>')
def c_is_fun(text):
    """
    Route handler for `/c/<text>`.
    Displays:
        "C " followed by the value of the `text` variable, with underscores replaced by spaces.
    Args:
        text (str): Text passed in the URL.
    Returns:
        str: "C <processed_text>", where underscores are replaced by spaces.
    """
    text = text.replace('_', ' ')
    return f"C {text}"


if __name__ == '__main__':
    # Disable strict slashes to allow routes to work with or without trailing slashes.
    app.url_map.strict_slashes = False

    # Run the app on 0.0.0.0 (accept connections from any host) and port 5000.
    app.run(host='0.0.0.0', port=5000)
