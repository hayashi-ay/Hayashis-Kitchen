from flask import Flask
from flask_restx import Resource, Api
from models import db, setup_db, db_drop_and_create_all

app = Flask(__name__)
setup_db(app)
api = Api(app, version='1.0', title='Hayashi\'s Kitchen',
	description='This is a kind of a reservation management system for my dinning table.',
)

'''
db_drop_and_create_all() will drop all existing records and create your db from scratch,
so the below code must be uncommented on the first run.
'''
# db_drop_and_create_all()

slot = api.namespace('Slot', description='Slot')
reserve = api.namespace('Reserve', description='Reserve')
user = api.namespace('User', description='User')

@slot.route('/slots')
class Slot(Resource):
	@slot.response(404, 'Resoure Not Found')
	@slot.response(500, 'Something went wrong')
	@slot.param('id', 'id of slot')
	def get(self):
		return {'get': 'slot'}

	def post(self):
		return {'method': 'post'}

	def put(self):
		return {'method': 'put'}

	def delete(self):
		return {'method': 'delete'}

@reserve.route('/reserve')
class Reserve(Resource):
	def post(self):
		return {'method': 'post'}

	def put(self):
		return {'method': 'put'}

@user.route('/users')
class User(Resource):
	def get(self):
		return {'get': 'slot'}

	def put(self):
		return {'method': 'put'}

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080,debug=True)
