from flask_restful import Resource


class Game(Resource):
    def __init__(self, model: str):
        self._model = model

    def get(self):
        return {'hello': self._model}
