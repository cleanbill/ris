from wtforms import Form, BooleanField, TextField, PasswordField, validators, DateField
from flask import current_app, request, render_template, url_for, redirect, flash, session, jsonify, abort
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from ris.permissions import admin_permission, user_permission
from ris.database import db
from ris.core import bp
from ris.core.models.user import User 
from uuid import uuid4

# proof of concept token login. this should probably be persisted centrally
# maybe look at using redis as it handles expiration etc for free
login_tokens = dict()

class LoginForm(Form):
	username = TextField('username',[validators.required()])
	password = PasswordField('password',[validators.required()])

@bp.after_request
def shutdown_session(response):
	db.session.remove()
	return response


@bp.route('/_request_token', methods=("GET", "POST"))
def generatetoken():
	'''
	this is mostly just as a proof of concept.
	should really break this down a bit more. for the java app integration
	my thinking was to 1. java app makes POST _request_token call, 2. gets token
	3. launches browser with token in url (GET) which should log them in
	'''
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		password = form.password.data

		try:
			user = db.session.query(User).filter(User.username == username).first()
		except:
			return 'No users found (you need at least one). Have you run initdb.py?'

		if user and user.checkpassword(password):
			# for testing purposes im just using a uuid here
			# could do with reading up on how to generate good tokens
			token = str(uuid4())
			login_tokens[token] = username
			rv = {'token':token, 'ok':True}
			return jsonify(rv)
		else:
			rv = {'token':None, 'ok':False}
			return jsonify(rv) 
	else:
		return render_template('testtoken.html', form=form)


@bp.route('/login_token/<token>')
def token_login(token):
	if login_tokens.has_key(token):
		try:
			user = db.session.query(User).filter(User.username == login_tokens[token]).first()
		except:
			return 'No users found (you need at least one). Have you run initdb.py?'
		if user:
			session['user'] = user
			identity_changed.send(current_app._get_current_object(), identity=Identity(user.username))
			return redirect(url_for('.test'))
	abort(403)


@bp.route('/login', methods=("GET","POST"))
def test_login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		password = form.password.data

		try:
			user = db.session.query(User).filter(User.username == username).first()
		except:
			return 'No users found (you need at least one). Have you run initdb.py?'

		if user and user.checkpassword(password):
			session['user']=user
			identity_changed.send(current_app._get_current_object(), identity=Identity(username))
			return redirect(url_for('.test'))
		else:
			flash('Sorry %s there is something wrong about your log on' % (username) ,u'Login Failed')
			return redirect(url_for('.test_login')) 
	else:
		return render_template('testlogin.html', form=form)

@bp.route('/logout')
def test_logout():
	if session.has_key('user'):
		del session['user']
	identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
	return redirect(url_for('.test_login'))

@bp.route('/test')
@admin_permission.require(401)
def test():
	return render_template('formtest.html')

@bp.route('/test/user')
@user_permission.require(401)
def test_userpermission():
	return 'you are a valid user. well done.'

@bp.route('/test/admin')
@admin_permission.require(401)
def test():
	return 'you are an admin! well done' 
