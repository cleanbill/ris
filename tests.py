import unittest
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flaskext.testing import TestCase

from ris import create_app as ris_create_app, db
from ris.permissions import admin_permission, user_permission

from ris.core.models.user import User

class UserModelTest(TestCase):

	def create_app(self):
		print 'creating test app'
		app = ris_create_app()
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		app.config['TESTING'] = True 
		app.config['SQLALCHEMY_ECHO'] =False  
		db.init_app(app)
		db.echo = False

		@app.route('/unit_test/adminonly')
		@admin_permission.require(401)
		def admin_only_page():
			return 'hello admin'

		@app.route('/unit_test/useronly')
		@user_permission.require(401)
		def user_only_page():
			return 'hello user'

		return app

	def setUp(self):
		db.create_all()

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_passwordhash(self):
		user1 = User('admin','password')

		# check we're actually hashing it
		self.assertNotEquals(user1.passwordhash, 'password')

		# check hashing is consistant 
		self.assertEquals(user1.hashpassword('password','salt'), user1.hashpassword('password','salt'))

		# check two users with the same pass dont generate same hash
		user2 = User('admin2','password')
		self.assertNotEquals(user1.passwordhash, user2.passwordhash)

	def test_login_form(self):
		self.assertEquals(0, db.session.query(User).count())

		response = self.app.test_client().get('/login')
		self.assert200(response)

		# check we're not allowed in
		response = self.app.test_client().get('/unit_test/adminonly')
		self.assert401(response)

		# check we're not allowed in
		response = self.app.test_client().get('/unit_test/useronly')
		self.assert401(response)

		# add a user (non admin)
		user_bob = User('bob', 'password')
		db.session.add(user_bob)
		db.session.commit()

		# do the login again (with wrong username right password)
		response =  self.app.test_client().post('/login', data=dict(username='notbob', password='password'))
		assert 'wrong password' in response.data

		# do the login again (with right username wrong password)
		response =  self.app.test_client().post('/login', data=dict(username='bob', password='notpassword'))
		assert 'wrong password' in response.data

		# do the login again (with right username right password)
		response =  self.app.test_client().post('/login', data=dict(username='bob', password='password'))
		print response
		assert 'wrong password' not in response.data

'''
class DatabaseTest(TestCase)():

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
		assert 'Welcome' in rv.data

	def test_userPersistance(self):
		user1 = User('bob, 'password')
		user2 = User('bob', 'password')
		user3 = User('jim', '123456')
		db.session.add_all([user1, user2, user3])
		db.session.commit()

		self.assertEquals(len(User.query.all()), 3)
		testuser = db.session.query(User).filter(User.username=='bob).first()
		# check we get back the record we just created
		self.assertEquals(testuser.username,'bob)

		# check we can validate the password
		self.assertEquals(testuser.passwordhash, hashpassword('password',testuser.username+'$4lt'))
		self.assertNotEquals(testuser.passwordhash, hashpassword('wrongpassword',testuser.username+'$4lt'))

		# check db doesnt just give us any old record
		missinguser = db.session.query(User.username, User.passwordhash).filter(User.username=='invalid').first()
		self.assertEquals(missinguser, None)

		db.session.delete(testuser)
		db.session.commit()
		self.assertEquals(len(User.query.all()), 2)
'''

if __name__ == '__main__':
	unittest.main()
