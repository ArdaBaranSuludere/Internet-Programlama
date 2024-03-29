
#views.py

from datetime import datetime
from flask import render_template, redirect, url_for, request, flash,Flask
from app import app, db
from flask_login import current_user, login_required
from app.models import RezervBasvurulari,Newsletter,Etkinlikler

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

@app.route('/shows-events.html')
def shows_events():
    events = Etkinlikler.query.all()
    return render_template('shows-events.html', events=events)

@app.route('/event-details.html')
def event_details():
    return render_template('event-details.html')

@app.route('/rent-venue.html')
def rent_venue():
    return render_template('rent-venue.html')

@app.route('/submit-form',methods=['POST'])
def submit_form():
        email = request.form['email']
        name = request.form['name']
        phone_number = request.form['phone_number']
        company = request.form['company']
        venue_requested = request.form['venue_requested']
        type_of_event = request.form['type_of_event']
        date_requested_primary = datetime.strptime(request.form['date_requested_primary'], '%Y-%m-%d').date()
        date_requested_secondary = datetime.strptime(request.form['date_requested_secondary'], '%Y-%m-%d').date()
        about_event = request.form['about_event']
        
        new_application = RezervBasvurulari(email=email, name=name, phone_number=phone_number, company=company,
                                            venue_requested=venue_requested, type_of_event=type_of_event,
                                            date_requested_primary=date_requested_primary,
                                            date_requested_secondary=date_requested_secondary, about_event=about_event)

        db.session.add(new_application)
        db.session.commit()

        return render_template('rent-venue.html')


@app.route('/abone-form', methods=['GET', 'POST'])
def abone_form():
    if request.method == 'POST':
        email = request.form['mail']

        existing_entry = Newsletter.query.filter_by(email=email).first()

        if existing_entry:
            flash('Zaten kayıtlısınız!', 'info')
        else:
            new_entry = Newsletter(email=email)

            db.session.add(new_entry)
            db.session.commit()

            flash('yeni kayıt başarılı!', 'success')

    return '', 204


@app.route('/tickets')
def tickets():
    events = Etkinlikler.query.all()
    return render_template('tickets.html', events=events)


@app.route('/my-tickets')
@login_required
def my_tickets():
    return render_template('my-tickets.html',etkinliks=current_user.etkinliks)


@app.route('/buy_tickets/<int:etkinlik_id>', methods=['GET', 'POST'])
@login_required
def buy_purchase(etkinlik_id):
    etkinlik = Etkinlikler.query.get(etkinlik_id)
    if etkinlik and etkinlik_id != current_user.id:
        current_user.etkinliks.append(etkinlik)
        db.session.commit()
        return redirect(url_for('tickets'))
    
    return render_template('index.html')


@app.route('/ticket-details', methods=['GET', 'POST'])
def ticket_details():
    
    if request.method == 'POST':
        etkinlik_adi = request.form.get('etkinlik_adi')

        events = Etkinlikler.query.all()

        if etkinlik_adi:
            events = [event for event in events if event.etkinlik_ad.strip() == etkinlik_adi]

    return render_template('ticket-details.html', events=events)


@app.route('/tickets_filtered', methods=['GET', 'POST'])
def tickets_filtered():
    if request.method == 'POST':

        selected_month = request.form.get('month')
        selected_location = request.form.get('location')

        events = Etkinlikler.query.all()

        if selected_month=='Month' or selected_month=='None':
            events = [event for event in events if event.etkinlik_yeri.strip() == selected_location.strip()]
            
        elif selected_location=='Location':
            events = [event for event in events if event.etkinlik_tarih.strftime('%B') == selected_month]
            
        else:
            if selected_month and selected_month.strip() != "" and selected_location and selected_location.strip() != "":
                events = [event for event in events if event.etkinlik_yeri.strip() ==
                           selected_location.strip() and event.etkinlik_tarih.strftime('%B') == selected_month.strip()]
        
        return render_template('tickets.html', events=events)
    else:
        events = Etkinlikler.query.all()
        events = [event for event in events if event.etkinlik_yeri.strip() == 'Radio City Musical Hall']
        return render_template('tickets.html', events=events)
