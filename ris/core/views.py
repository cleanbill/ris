from wtforms import Form, BooleanField, TextField, PasswordField, validators, DateField
from flask import current_app, request, render_template, url_for, redirect, flash
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from sqlalchemy import func
from ris.permissions import admin_permission, user_permission
from ris.database import db
from ris.core import bp
from models import Patient, Address

@bp.after_request
def shutdown_session(response):
	db.session.remove()
	return response

@bp.route('/test/login', methods=("GET","POST"))
def test_login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		username = form.username.data
		password = form.password.data

		# todo: do real authentication here
		if password == 'password':
			identity_changed.send(current_app._get_current_object(), identity=Identity(username))
			return redirect(url_for('.test'))
		else:
			return 'wrong password. get out %s' % (password)
	else:
		return render_template('testlogin.html', form=form)

@bp.route('/test/logout')
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

@bp.route('/register', methods=['GET','POST'])
def register_patient():
	form = PatientDemographicsForm(request.form)
	if request.method == 'POST' and form.validate():
		patient = Patient(form.forenames.data, form.surname.data, form.title.data, form.dob.data, form.sex.data)
		address = Address('main', form.address_line1.data, form.address_line2.data, form.address_line3.data, form.address_line4.data, form.post_code.data)
		patient.addresses.append(address)
		db.session.add(patient)
		db.session.commit()
		flash('Patient Registered')
		return redirect(url_for('.show_patients'))
	return render_template('register.html', form=form)

@bp.route('/')
def mainpage():
	return render_template('index.html')

@bp.route('/search', methods=['GET', 'POST'])
def search_patient():
	form = PatientDemographicsForm(request.form)
	if request.method == 'POST' and form.validate():
		search_url = '/patient'
		if form.surname.data:
			search_url += '/'+form.surname.data
		if form.forenames.data:
			search_url += '/'+form.forenames.data
		if form.dob.data:
			search_url += '/'+str(form.dob.data)
		if form.sex.data:
			search_url += '/'+form.sex.data
		return search_by_name(form.surname.data, form.forenames.data, form.dob.data, form.sex.data)
		#redirect(search_url)
	return render_template('search.html', form=form)

@bp.route('/patients')
def show_patients():
	patient_list = db.session.query(Patient).all()

	return render_template('patient_list.html', patient_list=patient_list)

@bp.route('/patient/<int:patient_id>')
def search_by_id(patient_id):
	patient = db.session.query(Patient).filter(Patient.id == patient_id).first()
	if patient:
		return patient.fullname()
	else:
		return 'patient not found'

@bp.route('/patient/<surname>')
@bp.route('/patient/<surname>/<forenames>')
@bp.route('/patient/<surname>/<forenames>/<dob>')
@bp.route('/patient/<surname>/<forenames>/<dob>/<sex>')
def search_by_name(surname, forenames=None, dob=None, sex=None):
	search = db.session.query(Patient).filter(Patient.surname==surname)
	if forenames:
		search = search.filter(Patient.forenames == forenames)
		if dob:
			search = search.filter(Patient.dob == dob)
			if sex:
				search = search.filter(Patient.sex == sex)

	return render_template('patient_list.html', patient_list=search.all())

class PatientDemographicsForm(Form):
	title = TextField('Title')
	forenames = TextField('Forenames', [validators.required()])
	surname = TextField('Surname', [validators.required()]) 
	dob = DateField('Date of Birth', [validators.optional()],format='%d/%m/%Y')
	sex = TextField('Sex', [validators.AnyOf(('M','F','U','I'))])
	address_line1 = TextField('Address Line 1')
	address_line2 = TextField('Address Line 2' )
	address_line3 = TextField('Address Line 3' )
	address_line4 = TextField('Address Line 4' )
	post_code = TextField('Post Code')


class LoginForm(Form):
	username = TextField('Username')
	password = PasswordField('Password')
