from flask import render_template, jsonify, redirect, url_for, flash, request, Response, render_template_string
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
import time
import requests
from datetime import datetime
import matplotlib.pyplot as plt
import io
import os 
import matplotlib
matplotlib.use('agg')
import base64
import numpy as np
from itertools import zip_longest
from flask import send_from_directory
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas 
from matplotlib.figure import Figure
import plotly.graph_objs as go 
import sqlite3
import bcrypt






@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Tillykke, du er en registreret bruger!')
        return redirect(url_for('login'))
    else:
        print(form.errors)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    logout_user()
    if current_user.is_authenticated:
        return redirect(url_for('welcome'))  # Redirect authenticated users to welcome page

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('welcome'))  # Redirect to welcome page after successful login
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')  # Provide feedback for failed login
    
    return render_template('login.html', title='Login', form=form)






@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



@app.route('/welcome')
def welcome():
    return render_template('welcome.html', title='Welcome')





@app.route('/elpriser', methods=['GET'])
def elpriser():
    # Funktion til at hente og vise elpriser for et givet prisområde
    def hent_elpriser(prisklasse='DK2', dato=None):
        if dato is None:
            # Henter den nuværende dato i det format, API'et forventer
            dato = datetime.now().strftime('%Y/%m-%d')
        
        # Bygger URL'en til API-forespørgslen med den ønskede dato og prisområde
        url = f"https://www.elprisenligenu.dk/api/v1/prices/{dato}_{prisklasse}.json"
        
        # Sender GET-forespørgslen til API'et og gemmer svaret
        response = requests.get(url)
        
        # Tjekker om forespørgslen var vellykket (HTTP statuskode 200)
        if response.status_code == 200:
            # Parser JSON-svaret til et Python-dictionary
            data = response.json()

            # Opret en tom liste til at holde HTML-strenge for priserne
            html_priser = []

            # Løber igennem hvert element i data-listen (hver time)
            for time in data:
                # Konverterer start- og sluttid til et mere læseligt format
                starttid = datetime.fromisoformat(time['time_start']).strftime('%Y-%m-%d %H:%M:%S')
                sluttid = datetime.fromisoformat(time['time_end']).strftime('%Y-%m-%d %H:%M:%S')

                # Formatterer prisen til en streng med 5 decimaler
                pris = f"{time['DKK_per_kWh']:.5f}"

                # Opret en HTML-streng for denne pris og tilføj den til listen
                html_pris = f"""
                <div>
                    <p>Starttid: {starttid}</p>
                    <p>Sluttid: {sluttid}</p>
                    <p>Pris: {pris} kr/kWh</p>
                </div>
                """
                html_priser.append(html_pris)

            # Returnerer listen med HTML-strenge for priserne
            return html_priser
        else:
            # Hvis forespørgslen ikke var vellykket, printer fejlmeddelelsen
            print("Fejl i forespørgsel:", response.status_code)
            return []

    # Hent dato og prisklasse fra URL-parametre, hvis de er angivet
    dato = request.args.get('dato')
    prisklasse = request.args.get('prisklasse', 'DK2')

    # Kald funktionen med det angivne prisområde og dato
    elpriser = hent_elpriser(prisklasse, dato)
    
    title = "Elpriser-notif"

    return render_template('elpriser.html', elpriser=elpriser, title=title)





# denne kode viser elpriser fra API i json-format
@app.route('/elpriser3', methods=['GET', 'POST'])
def elpriser3():
    if request.method == 'POST':
        request_data = request.get_json()
        dato = request_data.get('dato')
        prisklasse = request_data.get('prisklasse', 'DK2')
    else:
        dato = request.args.get('dato')
        prisklasse = request.args.get('prisklasse', 'DK2')

    def hent_elpriser(prisklasse='DK2', dato=None):
        if dato is None:
            dato = datetime.now().strftime('%Y/%m-%d')

        url = f"https://www.elprisenligenu.dk/api/v1/prices/{dato}_{prisklasse}.json"
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None

    elpriser_data = hent_elpriser(prisklasse, dato)

    # Returner JSON med elpriserne og navnet på HTML-filen
    return jsonify(elpriser=elpriser_data, template='elpriser2.html')




#denne viser realtime graf
@app.route('/elpriser9', methods=['GET'])
def elpriser9():
    # Modtag parametre fra URL'en
    mode = request.args.get('mode', 'embed')  # Tilstand (embed eller ikke embed)
    layout = request.args.get('layout', 'minimal')  # Layout (normal eller minimal)
    hide_examples = request.args.get('hide-examples', '1')  # Skjul pris-eksempler
    zoom = request.args.get('zoom', '1.2')  # Zoom-niveau
    background = request.args.get('background', 'ffffff')  # Baggrundsfarve

    # Generer iframe-kode med de angivne parametre
    iframe_code = f"""
    <script src="https://www.elprisenligenu.dk/api/v1/iframeResizer.min.js"></script>
    <iframe title="Elpriser fra elprisenligenu.dk" src="https://www.elprisenligenu.dk/i/kobenhavn?mode={mode}&layout={layout}&hide-examples={hide_examples}&zoom={zoom}&background={background}" style="width:100%;height:800px;border:0;" onload="iFrameResize({{heightCalculationMethod: 'taggedElement', checkOrigin: false}}, this);"></iframe>
    
    """

    return render_template('elpriser2.html', iframe_code=iframe_code)









@app.route('/beregn')
def beregn():
    return render_template('beregner.html')



