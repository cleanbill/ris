import unittest
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.testing import TestCase

from ris import create_app, db
from ris.examplemodule.models import User, hashpassword

class UserModelTest(TestCase):

	def create_app(self):
		#self.app = Flask(__name__)
		app = create_app()
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		app.config['TESTING'] = True
		db.init_app(app)
		return create_app()

	def setUp(self):
		pass

	def test_passwordhash(self):
		user1 = User('admin','password')

		# check we're actually hashing it
		self.assertNotEquals(user1.passwordhash, 'password')

		# check hashing is consistant 
		self.assertEquals(hashpassword('password','salt'), hashpassword('password','salt'))

		# check two users with the same pass dont generate same hash
		user2 = User('admin2','password')
		self.assertNotEquals(user1.passwordhash, user2.passwordhash)

	def test_pasteEncryption(self):
		pass

class DatabaseTest(TestCase):

	def create_app(self):
		app = create_app()
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		app.config['TESTING'] = True
		db.init_app(app)
		return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_main_page(self):
		rv = self.app.test_client().get('/')
		print rv.data
		assert 'hello' in rv.data

	def test_userPersistance(self):
		user1 = User('admin', 'password')
		user2 = User('bob', 'password')
		user3 = User('jim', '123456')
		db.session.add_all([user1, user2, user3])
		db.session.commit()

		self.assertEquals(len(User.query.all()), 3)
		testuser = db.session.query(User).filter(User.username=='admin').first()
		# check we get back the record we just created
		self.assertEquals(testuser.username,'admin')

		# check we can validate the password
		self.assertEquals(testuser.passwordhash, hashpassword('password',testuser.username+'$4lt'))
		self.assertNotEquals(testuser.passwordhash, hashpassword('wrongpassword',testuser.username+'$4lt'))

		# check db doesnt just give us any old record
		missinguser = db.session.query(User.username, User.passwordhash).filter(User.username=='invalid').first()
		self.assertEquals(missinguser, None)

		db.session.delete(testuser)
		db.session.commit()
		self.assertEquals(len(User.query.all()), 2)


if __name__ == '__main__':
	unittest.main()