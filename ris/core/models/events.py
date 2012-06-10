from sqlalchemy import Table, Column, Integer, String, Date, Binary, ForeignKey
from sqlalchemy.orm import relationship
from ris.database import db 

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
