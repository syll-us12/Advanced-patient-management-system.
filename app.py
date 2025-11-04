from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Patient
from ai_utils import generate_health_summary
import os

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    patients = Patient.query.all()
    return render_template('index.html', patients=patients)

@app.route('/add', methods=['POST'])
def add_patient():
    name = request.form['name']
    age = request.form['age']
    condition = request.form['condition']
    height = request.form['height']
    bpr = request.form['bpr']
    email = request.form['email']
    location = request.form['location']
    checkup_date = request.form['checkup_date']

    new_patient = Patient(
        name=name,
        age=age,
        condition=condition,
        height=height,
        bpr=bpr,
        email=email,
        location=location,
        checkup_date=checkup_date
    )
    db.session.add(new_patient)
    db.session.commit()
    flash('Patient added successfully!')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_patient(id):
    patient = Patient.query.get(id)
    if request.method == 'POST':
        patient.name = request.form['name']
        patient.age = request.form['age']
        patient.condition = request.form['condition']
        patient.height = request.form['height']
        patient.bpr = request.form['bpr']
        patient.email = request.form['email']
        patient.location = request.form['location']
        patient.checkup_date = request.form['checkup_date']
        db.session.commit()
        flash('Patient updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', patient=patient)

@app.route('/delete/<int:id>')
def delete_patient(id):
    patient = Patient.query.get(id)
    db.session.delete(patient)
    db.session.commit()
    flash('Patient deleted successfully!')
    return redirect(url_for('index'))

@app.route('/ai-summary/<int:id>')
def ai_summary(id):
    patient = Patient.query.get(id)
    summary = generate_health_summary(patient)
    return render_template('patient_detail.html', patient=patient, summary=summary)

if __name__ == '__main__':
    app.run(debug=True)
