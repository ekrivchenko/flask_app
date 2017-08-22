import json
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from flask import Flask, render_template, Response
import queries

application = Flask(__name__)
api = Api(application)
application.debug = True


DB_STRING = 'mysql+pymysql://%s:%s@%s:%s/%s' % ('barmaley', 'barmaley', 'testdb.chvxt94wiqg2.us-east-1.rds.amazonaws.com', 3306, 'test_db')
engine = create_engine(DB_STRING, pool_recycle=3600)
conn = engine.connect()


@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')


class Users(Resource):
    def get(self):
        conn = engine.connect()
        users = dict()
        users['users'] = list()
        r = conn.execute(queries.QUERY_SELECT_ALL_USERS).cursor.fetchall()

        return users, 200


api.add_resource(Users, '/api/v1/users')

if __name__ == '__main__':
    application.run(host='0.0.0.0')