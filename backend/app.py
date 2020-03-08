from flask import Flask, request, jsonify, abort
from flask_restx import Resource, Api, fields
from models import db, setup_db, db_drop_and_create_all, Slot, Reservation, User

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

user_resource_fields = api.model('User', {
		'id': fields.Integer,
		'name': fields.String,
		'auth0_user_id': fields.String,
	})

@slot.route('/slots')
class SlotResource(Resource):
	@slot.response(404, 'Resoure Not Found')
	@slot.response(500, 'Something went wrong')
	@slot.param('id', 'id of slot')
	def get(self):
		return {'get': 'slot'}

	def patch(self):
		return {'method': 'post'}

	def put(self):
		return {'method': 'put'}

	def delete(self):
		return {'method': 'delete'}

@reserve.route('/reserve')
class ReserveResource(Resource):
	def patch(self):
		return {'method': 'post'}

	def put(self):
		return {'method': 'put'}

@user.route('/users')
class UserResource(Resource):
	def get(self):
		return {'get': 'slot'}

	@user.doc(body=user_resource_fields)
	def put(self):
		body = request.get_json()

		auth0_user_id = body['auth0_user_id']
		name = body['name']

		user = User.query.filter_by(auth0_user_id=auth0_user_id).one_or_none()

		if user is None:
			try:
				user = User()

				user.auth0_user_id = auth0_user_id
				user.name = name

				db.session.add(user)
				db.session.commit()
			except:
				db.session.rollback()
				abort(422, "unprocessable")

		return jsonify( { "success": True, "id": user.id } )

if __name__ == '__main__':
	app.run(host='0.0.0.0',port=8080,debug=True)
