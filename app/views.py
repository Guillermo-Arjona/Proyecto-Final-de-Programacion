from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_restful import abort
import redis
import json
import requests
from app import db
from app.citas.models import Appointment

from app.citas.api_v1_0.resources import AppointmentListResource,AppointmentResource,AppointmentResourceEdit

alr = AppointmentListResource()
ar = AppointmentResource()
are = AppointmentResourceEdit()

views = Blueprint('views', __name__)

@views.route('/create-new-appointment', methods=['GET'])
def appointment():     
    
    return render_template("appointment.html")

@views.route('/', methods=['GET'] )
def home():

    list = alr.get()

    return render_template("home.html", appointments = list)


@views.route('/addAppointment', methods=['POST'])
def add_Appointment():
    
    data = {
        'name':request.form.get('name'),
        'lastname':request.form.get('lastname'),
        'email':request.form.get('email'),
        'phone_number':request.form.get('phone_number'),
        'apnt_date':request.form.get('apnt_date'),
    }
    alr.post(resp=data)
    flash('Se ha agendado la cita satisfactoriamente!!')

    return redirect('/')

@views.route('/editar', methods=['GET'])
def editar():    
    apnt_id = request.args.get('id')
    model = ar.get(appointment_id=apnt_id)
    print(model)
    return render_template("edit_apnt.html", model = model)

@views.route('/editar-appointment/<id>', methods=['GET','PUT'])
def editar_apnt(id):
    data = request.get_json()

    get_appnt = Appointment.query.get_or_404(id)
    
    print(get_appnt)

    get_appnt.name = request.form.get('name')
    get_appnt.lastname = request.form.get('lastname')
    get_appnt.lastname = request.form.get('email')
    get_appnt.lastname = request.form.get('phone_number')
    get_appnt.lastname = request.form.get('apnt_date')

    db.session.add(get_appnt)
    db.session.commit()

    return data