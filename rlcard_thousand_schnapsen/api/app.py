from flask import Flask
from flask_cors import CORS
from flask_restful import Api
import click

from rlcard_thousand_schnapsen.api.resources import Game

app = Flask(__name__)
api = Api(app)
CORS(app)


@click.command()
@click.option('--port', default=5000, help='Port number')
@click.option('--model',
              type=click.Path(exists=True),
              required=True,
              help='Path to pre-trained Deep CFR model')
def run_api(port: int, model: str):
    api.add_resource(Game, '/game', resource_class_args=[model])
    app.run(port=port)


if __name__ == '__main__':
    run_api()
