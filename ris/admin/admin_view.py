from flask import Flask, session
from flask.ext.principal import identity_changed, Identity, AnonymousIdentity
from flask.ext.admin import Admin, BaseView, expose, AdminIndexView
from flask.ext.admin.contrib.sqlamodel import ModelView
from wtforms import Form, BooleanField, TextField, validators, PasswordField

from ris.permissions import admin_permission, user_permission
from ris.database import db
from ris.core.models.patient import Patient, Address

class AdminIndex(AdminIndexView):
	
	def is_accessible(self):
		try:
			with admin_permission.require():
				return True
		except:
			pass		
		return False



