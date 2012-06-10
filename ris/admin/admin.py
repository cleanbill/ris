from flask import Flask
from flask.ext.admin import Admin, BaseView, expose

class MyView(BaseView):
	@expose('/')
	def index(self):
		return 'hello'#self.render('adminindex.html')

app = Flask(__name__)
app.config['DEBUG'] = True

admin = Admin(app)
admin.add_view(MyView(name='hello 1'))

app.run()