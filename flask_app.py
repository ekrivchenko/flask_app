from flask import Flask
from flask.ext.mysql import MySQL
from flask_restful import Resource, Api
import json
import uuid
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from flask import Flask, render_template, Response

app = Flask(__name__)
api = Api(app)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'barmaley'
app.config['MYSQL_DATABASE_PASSWORD'] = 'barmaley'
app.config['MYSQL_DATABASE_DB'] = 'test_db'
app.config['MYSQL_DATABASE_HOST'] = 'testdb.chvxt94wiqg2.us-east-1.rds.amazonaws.com'
mysql.init_app(app)

conn = mysql.connect()
cursor = conn.cursor()


class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

api.add_resource(HelloWorld, '/')

if __name__ == '__main__':
    app.run(debug=True)
