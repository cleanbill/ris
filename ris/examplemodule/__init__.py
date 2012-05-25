from flask import Blueprint
import ris

bp = Blueprint('examplemodule', 'ris', template_folder='examplemodule/templates')
import views
