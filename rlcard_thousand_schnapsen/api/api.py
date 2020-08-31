from flask import Flask
from flask_restful import Api

from rlcard_thousand_schnapsen.api.resources import Game

app = Flask(__name__)
api = Api(app)

api.add_resource(Game, '/game')

if __name__ == '__main__':
    app.run()
