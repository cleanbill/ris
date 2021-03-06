from __future__ import with_statement
from ris import create_app, db
from ris.core.models.user import User

app = create_app()
app.test_request_context().push()
db.drop_all()
db.create_all()
# create our minimal db objects here
admin = User('admin','password', admin=True)
db.session.add(admin)
db.session.commit()
db.session.remove()

