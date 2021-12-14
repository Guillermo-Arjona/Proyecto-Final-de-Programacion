import os
from app.db import db
from app.citas.models import Appointment 


if os.path.exists('appointments2.db'):
    os.remove('appointments2.db')

db.create_all()

db.session.commit()