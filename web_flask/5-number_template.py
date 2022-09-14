#!/usr/bin/python3
"""0. Hello Flask!"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def index():
    """Index
    Returns:
        Text: Hello HBNB!
    """
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Display HBNB
    """
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def c_text(text):
    """Put a text in the route
    """
    return "C {}".format(text.replace('_', ' '))


@app.route("/python/")
@app.route("/python/<text>", strict_slashes=False)
def py_text(text="is cool"):
    """Starts web aplication
    """
    return "Python {}".format(text.replace('_', ' '))


@app.route("/number/<int:n>", strict_slashes=False)
def get_number(n):
    """Try with number
    """
    if type(n) is int:
        return "{} is a number".format(n)


@app.route("/number_template/<int:n>", strict_slashes=False)
def template(n):
    """To see html redirection
    """
    return render_template('5-number.html', n=n)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
