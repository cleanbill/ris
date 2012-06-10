from flask import current_app, request, render_template, url_for, redirect, flash
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from sqlalchemy import func
from ris.permissions import admin_permission, user_permission
from ris.database import db
from ris.core import bp
from ris.core.models.patient import Patient, Address
from wtforms import Form, BooleanField, TextField, validators, DateField

@bp.after_request
def shutdown_session(response):
	db.session.remove()
	return response


@bp.route('/register', methods=['GET','POST'])
@user_permission.require(401)
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
@user_permission.require(401)
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
@user_permission.require(401)
def show_patients():
	patient_list = db.session.query(Patient).all()

	return render_template('patient_list.html', patient_list=patient_list)

@bp.route('/patient/<int:patient_id>')
@user_permission.require(401)
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
@user_permission.require(401)
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

