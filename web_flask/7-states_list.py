#!/usr/bin/python3
"""
Starts a Flask web application that serves a list of states.
"""

from flask import Flask, render_template

from models import storage

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states():
    """
    Retrieves a list of states from storage and renders them in a template.

    Returns:
        HTML page displaying the list of states.
    """
    return render_template("7-states_list.html", states=storage.all("State").values())


@app.teardown_appcontext
def teardown():
    """
    Removes the current SQLAlchemy session to free up resources.

    Args:
        exception (Exception, optional): The exception that caused the teardown, if any.
    """
    storage.close()


if __name__ == "__main__":
    # Run the Flask application, making it accessible from any IP.
    app.run(host="0.0.0.0")
