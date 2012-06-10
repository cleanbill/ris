from wtforms import Form, BooleanField, TextField, PasswordField, validators, DateField
from flask import current_app, request, render_template, url_for, redirect, flash
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from ris.permissions import admin_permission, user_permission
from ris.database import db
from ris.core import bp
from ris.core.models.user import User 


class LoginForm(Form):
	username = TextField('username',[validators.required()])
	password = PasswordField('password',[validators.required()])

@bp.after_request
def shutdown_session(response):
	db.session.remove()
	return response

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
			identity_changed.send(current_app._get_current_object(), identity=Identity(username))
			return redirect(url_for('.test'))
		else:
			flash('Sorry <b>%s</b> there is something wrong about your log on' % (username) ,u'Login Failed')
			return redirect(url_for('.test_login')) 
	else:
		return render_template('testlogin.html', form=form)

@bp.route('/logout')
def test_logout():
	identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
	return redirect(url_for('.test'))

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
