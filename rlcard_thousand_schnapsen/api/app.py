from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_socketio import SocketIO
import click

from rlcard_thousand_schnapsen.api.resources import Game

app = Flask(__name__)
api = Api(app)
CORS(app)
socket_io = SocketIO(app, async_mode='threading')


@click.command()
@click.option('--port', default=5000, help='Port number')
@click.option('--model',
              type=click.Path(exists=True),
              required=True,
              help='Path to pre-trained Deep CFR model')
def run_api(port: int, model: str):
    api.add_resource(Game,
                     '/game',
                     resource_class_args=[model, socket_io.emit])
    socket_io.run(app, port=port)


if __name__ == '__main__':
    run_api()
