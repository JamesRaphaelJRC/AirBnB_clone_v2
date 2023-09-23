#!/usr/bin/python3
''' Starts a flask web application:
        Listens on 0.0.0.0, port 5000
    Routes:
        /           - displays "Hello HBNB!"
        /hbnb       - displays "HBNB"
        /c/<text>   - displays "C" followed by the value of the text
        /python/<text> - displays "Python" followed by the value of the text
        /number/<n> - displays '<n> is a number' only if n is an integer
'''
from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello_hbnb():
    ''' Displays Hello HBNB! '''
    return "Hello HBNB!"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    ''' Displays HBNB '''
    return "HBNB"


@app.route("/c/<text>", strict_slashes=False)
def display_c(text):
    ''' Displays "C" followed by the value of the text '''
    text = text.replace("_", " ")
    return "C {}".format(text)


@app.route("/python", strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def display_python(text=None):
    if not text:
        text = "is cool"
    else:
        text = text.replace("_", " ")
    return "Python {}".format(text)


@app.route("/number/<int:n>", strict_slashes=False)
def is_number(n):
    return "{} is a number".format(n)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
