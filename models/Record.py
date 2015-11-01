################## IMPORTS ####################
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from sqlalchemy import String, Column, Text


################## SETUP #####################

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///twilio.db'

# set up db
db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('record', MigrateCommand)

class Record(db.Model):
    phone = db.Column(db.Text, primary_key=True)
    image_uri = db.Column(db.Text)

    def __init__(self, phone, image_uri):
        self.phone = phone
        self.image_uri = image_uri

if __name__ == "__main__":
	manager.run()
