from flask import Flask
from flask_restx import Resource, Api

app = Flask(__name__)
api = Api(app, version='1.0', title='Hayashi\'s Kitchen',
	description='This is a kind of a reservation management system for my dinning table.',
)

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
