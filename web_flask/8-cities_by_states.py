#!/usr/bin/python3
''' Starts a Flask web applicaton listening on 0.0.0.0 port 5000'''
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/cities_by_states', strict_slashes=False)
def cities_by_states():
    ''' Displays a HTML webpage with a list of all States object in the
        database
    '''
    states = storage.all("State")
    return render_template("8-cities_by_states.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    ''' Remove the current SQLALchemy session'''
    storage.close()


if __name__ == '__main__':
    app.run(host="0.0.0.0")
