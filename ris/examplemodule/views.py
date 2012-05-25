from flask import request, render_template, url_for, redirect
from sqlalchemy import func
from models import User
from ris.database import db
from ris.examplemodule import bp

@bp.after_request
def shutdown_session(response):
	db.session.remove()
	return response

@bp.route('/test')
def testpage():
	return render_template('main.html') 

@bp.route('/')
def mainpage():
	user = db.session.query(func.count(User.userid)).all()
	return 	"hello. example module here. %s %d"% (url_for('.mainpage'), len(user))

@bp.route('/newuser', methods=['GET','POST'])
def newpaste():
	if request.method == 'POST':
		user = User(request.form['username'], request.form['password'])
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('examplemodule.mainpage'))
	else:
		pass
		# show new paste form
	return 'New Paste'

@bp.route('/admin')
def adminpage():
	return 'Admin Page'

@bp.route('/admin/user/<int:userid>')
def admininfo(userid):
	user = db.session.query(User).filter(User.userid == userid).first()
	if user == None:
		return 'User not found'
	else:
		return 'user: %s password %s' % (user.username, user.passwordhash)
