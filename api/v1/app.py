#!/usr/bin/python3
'''
Creates app.py to register blueprint to Flask instance app
'''
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
'''Enable CORS: key is all routes, origin is specific IP'''
CORS(app, resources={'/*': {'origins': '0.0.0.0'}})


@app.teardown_appcontext
def teardown_db(self):
    '''Closes storage on teardown'''
    storage.close()


@app.errorhandler(404)
def page_not_found(e):
    ''' Custom error handler for 404 page not found '''
    return jsonify(dict(error="Not found")), 404


if __name__ == '__main__':
    app.run(host=getenv('HBNB_API_HOST'), port=int(getenv('HBNB_API_PORT')),
            threaded=True)
'''
To test CORS, run:
$ curl -X GET http://0.0.0.0:5000/api/v1/cities/
1da255c0-f023-4779-8134-2b1b40f87683 -vvv

You will see this HTTP Response Header: < Access-Control-Allow-Origin: 0.0.0.0

To test page_not_found run:
$ curl -X GET http://0.0.0.0:5000/api/v1/nop
{
  "error": "Not found"
}
'''
