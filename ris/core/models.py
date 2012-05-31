from sqlalchemy import Table, Column, Integer, String, Date, Binary, ForeignKey
from ris.database import db 

class Patient(db.Model):
	__tablename__ = 'patients'
	id = db.Column(Integer, primary_key=True)
	surname = db.Column( String(50), nullable=False)
	forenames = db.Column(String(50), nullable=False)
	title = db.Column(String(20))
	dob = db.Column(Date)
	soundexkey = db.Column(String(100))
	sex = db.Column(String(1))

	def __init__(self, forenames, surname, title, dob, sex):
		self.surname=surname
		self.forenames=forenames
		self.title=title
		self.dob=dob
		self.sex=sex

	def fullname(self):
		return "%s %s %s %s" % (self.title, self.forenames, self.surname, self.dob)

class Identity(db.Model):
	'''
	as a way of handling merges, duplicates etc we could seperate out the concept
	of patient and their identity(s). it would give us an easy way of handling merges
	and duplicates, etc, we could keep track of HIS/external systems
	also allows us to keep history of demographic changes
	patient stores info about their relationship and actions in the hospital

	'''
	__tablename__ = 'identities'
	id = db.Column(Integer, primary_key=True)

class Address(db.Model):
	__tablename__ = 'address'

	id = db.Column(Integer, primary_key=True)
	patient_id = db.Column(Integer, ForeignKey('patients.id'))
	address_type = db.Column('address_type', String(50))
	address_line1 = db.Column('address_line1', String(200))
	address_line2 = db.Column('address_line2', String(200))
	address_line3 = db.Column('address_line3', String(200))
	address_line4 = db.Column('address_line4', String(200))
	post_code = db.Column('post_code', String(200))


class Appointment(db.Model):
	'''
	has an exam, for a patient on a date at a place
	'''

	__tablename__ = 'appointments'
	id = db.Column('eventid', Integer, primary_key=True)
	patient_id = db.Column(Integer, ForeignKey('patients.id'))


class Exam(db.Model):
	__tablename__ ='exams'
	id = db.Column('examid', Integer, primary_key=True)
	code = db.Column(String(20), ForeignKey('examcodes.code'))

class ExamCode(db.Model):
	__tablename__ = 'examcodes'
	code = db.Column('code', String(20), primary_key=True)
	description = db.Column('description',String(200))
	modality = db.Column('modality', String(2), nullable=False)

