from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

db = SQLAlchemy()

class Registro(db.Model):
    __tablename__ = 'registros'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    cedula = db.Column(db.String(20), nullable=False, unique=True)
    telefono = db.Column(db.String(20))
    barrio = db.Column(db.String(100))
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)