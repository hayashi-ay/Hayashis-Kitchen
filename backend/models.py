from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def setup_db(app):
	app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', 'postgres://postgres:postgres@db:5432/hayashis-kitchen')
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	db.app = app
	db.init_app(app)

def db_drop_and_create_all():
	db.drop_all()
	db.create_all()

class Slot(db.Model):
	__tablename__ = 'slots'

	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String, nullable=False)
	description = db.Column(db.String, nullable=False)
	start_time = db.Column(db.DateTime, nullable=False)
	capacity = db.Column(db.Integer, nullable=False)

	reservation = db.relationship('Reservation')

	def to_dict(self):
		return {
			'id': self.id,
			'title': self.title,
			'description': self.description,
			'start_time': self.start_time,
			'capacity': self.capacity
		}

class Reservation(db.Model):
	__tablename__ = 'reservations'

	id = db.Column(db.Integer, primary_key=True)
	slot_id = db.Column(db.Integer, db.ForeignKey('slots.id'), nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String, nullable=False)
	auth0_user_id = db.Column(db.String, unique=True, nullable=False)

	reservation = db.relationship('Reservation')

	def to_dict(self):
		return {
			'id': self.id,
			'name': self.name,
		}
