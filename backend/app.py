from flask import Flask, request, jsonify, abort, render_template
from flask_restx import Resource, Api, fields
from flask_cors import CORS
from models import db, setup_db, db_drop_and_create_all, Slot, Reservation, User
from auth import requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

authorizations = {
	'oauth2': {
		'type': 'oauth2',
		'flow': 'implicit',
		'authorizationUrl': 'https://hayashi-ay.auth0.com/authorize?audience=hayashis_kitchen',
		'scopes': {},
	}
}

api = Api(app, version='1.0', title='Hayashi\'s Kitchen',
	description='This is a kind of a reservation management system for my dinning table.',
	authorizations=authorizations,
)

'''
db_drop_and_create_all() will drop all existing records and create your db from scratch,
so the below code must be uncommented on the first run.
'''
# db_drop_and_create_all()

slot = api.namespace('Slot', description='Slot')
reserve = api.namespace('Reserve', description='Reserve')
user = api.namespace('User', description='User')

slot_resource_fields = api.model('Slot', {
		'id': fields.Integer,
		'title': fields.String,
		'description': fields.String,
		'start_time': fields.DateTime,
		'capacity': fields.Integer,
	})

reserve_resource_fields = api.model('Reserve', {
		'id': fields.Integer,
		'slot_id': fields.Integer,
		'user_id': fields.Integer,
	})

user_resource_fields = api.model('User', {
		'id': fields.Integer,
		'name': fields.String,
		'auth0_user_id': fields.String,
	})

@app.route('/oauth2-redirect.html')
def render_html():
	return render_template('oauth2-redirect.html')

@slot.route('/slots')
class SlotResource(Resource):
	@slot.response(404, 'Resoure Not Found')
	@slot.response(500, 'Something went wrong')
	@slot.param('id', 'id of slot')
	@slot.param('user_id', 'retrieve slots with reverved by the user')
	@slot.param('search_start_date', 'start date of searching')
	@slot.param('search_end_date', 'end date of searching')
	def get(self):
		sql = Slot.query

		user_id = request.args.get('user_id', None, type=int)
		if user_id:
			sql = sql.join(Reservation, Slot.id==Reservation.slot_id).filter( Reservation.user_id == user_id )

		id = request.args.get('id', None, type=int)
		if id:
			sql = sql.filter_by(id=id)

		search_start_date = request.args.get('search_start_date', None, type=str)
		search_end_date = request.args.get('search_end_date', None, type=str)
		if search_start_date:
			sql = sql.filter(Slot.start_time >= search_start_date)
		if search_end_date:
			sql = sql.filter(Slot.start_time <= search_end_date)

		slots = list(map(lambda x: x.to_dict(), sql.all() ) )
		'''
		TODO: 'TypeError: Object of type Response is not JSON serializable' is raised,
		when response status code is explicitly passed to the return object:
		return jsonify( {"success": True, "slots": slots} ), 200
		'''
		return jsonify( {"success": True, "slots": slots} )

	@user.doc(body=slot_resource_fields)
	@api.doc(security=[{'oauth2': ['patch:slots']}])
	@requires_auth('patch:slots')
	def patch(self, jwt):
		body = request.get_json()

		slot_id = body['id']
		if slot_id is None:
			abort(404, "resource not found")

		slot = Slot.query.filter_by(id=slot_id).one_or_none()
		if slot is None:
			abort(404, "resource not found")

		if 'title' in body:
			slot.title = body['title']

		if 'description' in body:
			slot.description = body['description']

		if 'start_time' in body:
			slot.start_time = body['start_time']

		if 'capacity' in body:
			slot.capacity = body['capacity']

		try:
			db.session.add(slot)
			db.session.commit()
		except:
			abort(422, "unprocessable")
		return jsonify( { "success": True, "slots": [ slot.to_dict() ] } )

	@user.doc(body=slot_resource_fields)
	@api.doc(security=[{'oauth2': ['put:slots']}])
	@requires_auth('put:slots')
	def put(self, jwt):
		body = request.get_json()

		title = body['title']
		description = body['description']
		start_time = body['start_time']
		capacity = body['capacity']

		try:
			slot = Slot()

			slot.title = title
			slot.description = description
			slot.start_time = start_time
			slot.capacity = capacity

			db.session.add(slot)
			db.session.commit()
		except:
			db.session.rollback()
			abort(422, "unprocessable")

		return jsonify( { "success": True, "id": slot.id } )

	@slot.doc(params={'id': 'An ID of slot'})
	@api.doc(security=[{'oauth2': ['delete:slots']}])
	@requires_auth('delete:slots')
	def delete(self, jwt):
		slot_id = request.args.get('id', None, type=int)
		if id is None:
			abort(404, "resource not found")

		slot = Slot.query.filter_by(id=slot_id).one_or_none()
		if slot is None:
			abort(404, "resource not found")

		try:
			db.session.delete(slot)
			db.session.commit()
		except:
			db.session.rollback()
			abort(422, "unprocessable")
		return jsonify( { "success": True, "delete": slot_id } )

@reserve.route('/reserve')
class ReserveResource(Resource):
	@user.doc(body=reserve_resource_fields)
	def put(self):
		body = request.get_json()

		slot_id = body['slot_id']
		user_id = body['user_id']

		try:
			reservation = Reservation()
			reservation.slot_id = slot_id
			reservation.user_id = user_id

			db.session.add(reservation)
			db.session.commit()
		except:
			db.session.rollback()
			abort(422, "unprocessable")

		return jsonify( { "success": True, "id": reservation.id } )

@user.route('/users')
class UserResource(Resource):
	@slot.param('id', 'id of user')
	def get(self):
		sql = User.query

		id = request.args.get('id', None, type=int)
		if id:
			sql = sql.filter_by(id=id)

		users = list(map(lambda x: x.to_dict(), sql.all() ) )

		return jsonify( { "success": True, "users": users } )

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
