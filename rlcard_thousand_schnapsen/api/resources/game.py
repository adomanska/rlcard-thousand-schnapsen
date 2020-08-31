from flask_restful import Resource


class Game(Resource):
    def get(self):
        return {'hello': 'world'}
