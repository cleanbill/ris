from flask import Flask, jsonify, request, Blueprint, g, session
from flask.ext.principal import Principal, RoleNeed, UserNeed, identity_loaded, AnonymousIdentity

from database import db
from permissions import admin_permission, user_permission
import core
from core.models.user import User


root_blueprint = Blueprint('root','ris', url_prefix='/')

@root_blueprint.route('/')
def index():
	return 'hello world!'

def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
	app.config['SQLALCHEMY_ECHO'] = False
	app.config['DEBUG'] = True
	app.secret_key = 'DEVELOPMENT KEY CHANGE ME'

	# register all blueprints here
	#app.register_blueprint(examplemodule.bp)
	app.register_blueprint(core.bp)

	# start up sqlalchemny
	db.init_app(app)

	configure_login(app)
	
	return app

def configure_login(app):

    principal = Principal(app)

    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
    	# revoke any roles for anon users
		if identity.name == AnonymousIdentity().name:
			identity.provides.clear()
			return

		# get user from session
		if session.has_key('user'):
			user = session['user']

			if user.username != identity.name:
				user = None

		# its possible this might not be needed
		if user == None:
			user = db.session.query(User).filter(User.username == identity.name).first()
			session['user'] = user

		#TODO: add proper role lookups. for now we just have admin or normal user
		identity.provides.add(RoleNeed('user'))
		if user.admin:
			identity.provides.add(RoleNeed('admin'))
