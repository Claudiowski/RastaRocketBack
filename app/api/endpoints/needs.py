from flask_restplus import Resource
from app.api import api
from ..serializers.needs import need_data_container

ns = api.namespace('needs', description='Operations related to needs')


@ns.route('/')
class NeedCollection(Resource):

    @api.marshal_with(need_data_container)
    def get(self):
        """
        Return needs list
        """

        return {'needs': []}