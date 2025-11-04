from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    condition = db.Column(db.String(200))
    height = db.Column(db.String(50))
    bpr = db.Column(db.String(50))
    email = db.Column(db.String(120))
    location = db.Column(db.String(120))
    checkup_date = db.Column(db.String(50))

    def __repr__(self):
        return f'<Patient {self.name}>'
