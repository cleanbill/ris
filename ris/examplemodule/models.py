from sqlalchemy import Table, Column, Integer, String, DateTime, Binary
from ris.database import db 
from datetime import datetime as pydatetime
import hashlib

class ExampleUser(db.Model):
	__tablename__ = 'example_users'
	userid = db.Column('userid', Integer, primary_key=True)
	username = db.Column('username', String(50), unique=True)
	passwordhash = db.Column('passwordhash',String(50), nullable=False)

	def __init__(self, username, password):
		self.username=username
		self.passwordhash= hashpassword(password,username+'$4lt')
	def __repr__(self):
		return self.username

def hashpassword( password, salt):
	hasher = hashlib.new('SHA256')		
	hasher.update(password+salt)
	return hasher.hexdigest()

