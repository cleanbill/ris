from flask import Blueprint
import ris

bp = Blueprint('core', 'ris', template_folder='core/templates')
import views.login_view
import views.patient_view
