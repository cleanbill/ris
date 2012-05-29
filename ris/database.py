from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.echo=True

