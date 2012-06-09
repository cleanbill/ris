from sqlalchemy import Table, Column, Integer, String, Boolean
from ris.database import db 
from datetime import datetime as pydatetime
import hashlib

class User(db.Model):
	__tablename__ = 'users'
	userid = db.Column('userid', Integer, primary_key=True)
	username = db.Column('username', String(50), unique=True)
	passwordhash = db.Column('passwordhash',String(50), nullable=False)
	admin = db.Column('admin', Boolean)

	def __init__(self, username, password, admin=False):
		self.username=username
		salt = self.username+'$4lt'
		self.passwordhash= self.hashpassword(password,salt)
		self.admin=admin

	def __repr__(self):
		return self.username

	def hashpassword(self, password, salt):
		hash = hashlib.new('SHA256')		
		hash.update(password+salt)
		return hash.hexdigest()

	def checkpassword(self, password):
		salt = self.username+'$4lt'
		return self.hashpassword(password, salt) == self.passwordhash
