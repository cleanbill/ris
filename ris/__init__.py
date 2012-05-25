from flask import Flask, jsonify, request, Blueprint
from database import db
import examplemodule

root_blueprint = Blueprint('root','ris', url_prefix='/')

@root_blueprint.route('/')
def index():
	return 'hello world!'

def create_app():
	app = Flask(__name__)
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
	app.config['DEBUG'] = True

	# register all blueprints here
	app.register_blueprint(examplemodule.bp)
	
	# start up sqlalchemny
	db.init_app(app)
	return app
