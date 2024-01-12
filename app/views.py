from datetime import datetime
from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.models import RezervBasvurulari

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/tickets.html')
def tickets():
    return render_template('tickets.html')

@app.route('/ticket-details.html')
def ticket_details():
    return render_template('ticket-details.html')

@app.route('/shows-events.html')
def shows_events():
    return render_template('shows-events.html')

@app.route('/event-details.html')
def event_details():
    return render_template('event-details.html')

@app.route('/rent-venue.html')
def rent_venue():
    return render_template('rent-venue.html')

@app.route('/submit-form',methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        # Formdan gelen verileri al
        email = request.form['email']
        name = request.form['name']
        phone_number = request.form['phone_number']
        company = request.form['company']
        venue_requested = request.form['venue_requested']
        type_of_event = request.form['type_of_event']
        date_requested_primary = datetime.strptime(request.form['date_requested_primary'], '%Y-%m-%d').date()
        date_requested_secondary = datetime.strptime(request.form['date_requested_secondary'], '%Y-%m-%d').date()
        about_event = request.form['about_event']
        return f"Form submitted successfully."
    
    new_application = RezervBasvurulari(email=email, name=name, phone_number=phone_number, company=company,
                                            venue_requested=venue_requested, type_of_event=type_of_event,
                                            date_requested_primary=date_requested_primary,
                                            date_requested_secondary=date_requested_secondary, about_event=about_event)

        # Veritabanına kaydet
    db.session.add(new_application)
    db.session.commit()
