from __future__ import with_statement
from ris import create_app, db
#from encpaste.pastes.models import User

app = create_app()
app.test_request_context().push()
db.create_all()
# create our minimal db objects here
# admin = User('admin','password')
# db.session.add(admin)
# db.session.commit()
