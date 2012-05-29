from flask import Flask, jsonify, request, Blueprint
from database import db
import examplemodule, core

root_blueprint = Blueprint('root','ris', url_prefix='/')

@root_blueprint.route('/')
def index():
	return 'hello world!'

def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
	app.config['DEBUG'] = True
	app.secret_key = 'DEVELOPMENT KEY CHANGE ME'

	# register all blueprints here
	app.register_blueprint(examplemodule.bp)
	app.register_blueprint(core.bp)
	
	# start up sqlalchemny
	db.init_app(app)
	db.echo = True
	return app
