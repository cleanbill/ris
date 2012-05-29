from flask import request, render_template, url_for, redirect, flash
from sqlalchemy import func
from models import Patient
from ris.database import db
from ris.core import bp
from wtforms import Form, BooleanField, TextField, PasswordField, validators, DateField

@bp.after_request
def shutdown_session(response):
	db.session.remove()
	return response

@bp.route('/test')
def testpage():
	return render_template('main.html') 

@bp.route('/register', methods=['GET','POST'])
def register_patient():
	form = PatientRegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		print "%s %s %s %s %s" % (form.forenames.data, form.surname.data, form.title.data, form.dob.data, form.sex.data)
		patient = Patient(form.forenames.data, form.surname.data, form.title.data, form.dob.data, form.sex.data)
		db.session.add(patient)
		db.session.commit()
		flash('Patient Registered')
		return redirect(url_for('.show_patients'))
	return render_template('register.html', form=form)

@bp.route('/')
def mainpage():
	return 'hello'

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

class PatientRegistrationForm(Form):
	title = TextField('Title')
	forenames = TextField('Forenames')
	surname = TextField('Surname') 
	dob = DateField('Date of Birth', format='%d/%m/%Y')
	sex = TextField('sex' )


