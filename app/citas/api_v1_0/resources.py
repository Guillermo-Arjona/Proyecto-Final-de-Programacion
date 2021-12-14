import arrow 
from flask import request, Blueprint
from flask_restful import Api, Resource
from flask import render_template, request, redirect, url_for
from app.common.error_handling import ObjectNotFound

from .schemas import AppointmentSchema
from ..models import Appointment

appointment_v1_0_bp = Blueprint('appointments_v1_0_bp', __name__)

appointment_schema = AppointmentSchema()

api = Api(appointment_v1_0_bp)

class AppointmentListResource(Resource):
    def get(self):
        films = Appointment.get_all()
        result = appointment_schema.dump(films, many=True)
        return result

    def post(self,resp):
        
        if resp:
            data=resp
            appointment_dict = resp
            print(appointment_dict)
        else:
            print(self)
            data = request.get_json(self)
            appointment_dict = appointment_schema.load(data)
            
        apnt = Appointment(name=appointment_dict['name'],
                           lastname=appointment_dict['lastname'],
                           email=appointment_dict['email'],
                           phone_number=appointment_dict['phone_number'],
                           apnt_date=appointment_dict['apnt_date']
        )
        apnt.apnt_date = arrow.get(apnt.apnt_date).to('utc').naive
        apnt.save()
        resp = appointment_schema.dump(apnt)
        return resp, 201

class AppointmentResource(Resource):
    def get(self,appointment_id):
        apnt = Appointment.get_by_id(appointment_id)
        
        resp = appointment_schema.dump(apnt)
        return resp

class AppointmentResourceEdit(Resource):
    def post(self,id,data):
        apnt = Appointment.save_changes(id,data)
        

class AppointmentResourceDelete(Resource):
    def post(self, id):
        apnt = Appointment.delete(id)

        return 201


api.add_resource(AppointmentListResource, '/api/v1.0/appointments/', endpoint='appointment_list_resource')
api.add_resource(AppointmentResource, '/api/v1.0/appointments/<int:appointment_id>', endpoint='appointment_resource')
api.add_resource(AppointmentResourceDelete, '/api/v1.0/appointments/delete/<int:id>', endpoint='appointment_resource_delete')