import json
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
from flask import Flask, render_template, Response, make_response
import queries

application = Flask(__name__)
api = Api(application)
application.debug = True


DB_STRING = 'mysql+pymysql://{0}:{1}@{2}:{3}/{4}'.format('barmaley', 'barmaley', 'testdb.chvxt94wiqg2.us-east-1.rds.amazonaws.com', 3306, 'test_db')
engine = create_engine(DB_STRING, pool_recycle=3600)
conn = engine.connect()

error = dict()


@application.route('/', methods=['GET'])
def index():
    return render_template('index.html')


class Users(Resource):
    def get(self):
        users = dict()
        users['users'] = list()
        r = conn.execute(queries.QUERY_SELECT_ALL_USERS).cursor.fetchall()
        for user in r:
            users['users'].append({'uuid': user[0],
                                   'first_name': user[1],
                                   'last_name': user[2],
                                   'email': user[3]})
        return users, 200

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, location='json')
        parser.add_argument('first_name', type=str, location='json')
        parser.add_argument('last_name', type=str, location='json')
        args = parser.parse_args(strict=True)
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']

        try:
            conn.execute(queries.QUERY_INSERT_USER.format('1', first_name, last_name, email))
            return make_response('', 201)
        except Exception:
            error['error'] = 'Something went wrong.'
            return make_response(json.dumps(error), 500)

api.add_resource(Users, '/api/v1/users')

if __name__ == '__main__':
    application.run()
