from flask import Flask, request
from flask_restplus import Api, Resource
from flask_json import FlaskJSON
from core.base_api import base_blueprint
import json as j
import os
import traceback

app: Flask = Flask(__name__)
app.register_blueprint(base_blueprint)
json: FlaskJSON = FlaskJSON(app)

api = Api(app=app, version="1.0", title="Annotation Interface API",
          description="API for the Annotation Interface of the Dejavu Project")

col_namespace = api.namespace('annoapi/images',
                              description='Collections')

list_of_names = {}


@col_namespace.route("/list_images")
class list_images(Resource):
    @api.doc(responses={200: 'OK', 404: 'Error'},
         params={"title": "collection's title"})

    @api.doc(responses={200: 'OK', 404: 'None Collections'})
    def get(self):
        collections = col.list_collections()

        try:
            if collections is None:
                return app.response_class(status=404,
                                          mimetype='application/json')

            return app.response_class(
                response=j.dumps([col for col in collections]),
                status=200,
                mimetype='application/json'
            )
        except Exception as e:
            print(traceback.format_exc())
            return app.response_class(status=404, mimetype='application/json')