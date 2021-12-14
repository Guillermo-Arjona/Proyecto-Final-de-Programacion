from marshmallow import fields

from app.ext import ma


class AppointmentSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    lastname = fields.String()
    email = fields.String()
    phone_number = fields.String()
    apnt_date = fields.DateTime()
