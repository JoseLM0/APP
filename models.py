from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()

class Usuarios(db.Model, UserMixin):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key = True)
    Nombre = db.Column(db.String(45), nullable= False)
    Apellido1 = db.Column(db.String(45), nullable= False)
    Apellido2 = db.Column(db.String(45), nullable= False)
    Correo = db.Column(db.String(45), nullable= False)
    Password = db.Column(db.String(250), nullable= False)
    Puesto = db.Column(db.Integer, nullable = False, default = 0)

    def __repr__(self):
        return f'<Usuario {self.Correo}>'
    
    def set_Password(self, Password):
        self.Password = generate_password_hash(Password)

    def check_password(self, password):
        return check_password_hash(self.Password, password) 
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

class Contactos(db.Model):
    __tablename__="Contactos"
    id = db.Column(db.Integer, primary_key = True)
    Nombre = db.Column(db.String(45), nullable= False)
    Apellido1 = db.Column(db.String(45), nullable= False)
    Apellido2 = db.Column(db.String(45), nullable= True)
    Telefono1 = db.Column(db.Integer, nullable = True, default = 0)
    Telefono2 = db.Column(db.Integer, nullable = True, default = 0)
    Correo1 = db.Column(db.String(45), nullable= True)
    Correo2 = db.Column(db.String(45), nullable= True)
    Empresa = db.Column(db.String(45), nullable= True)
    date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    def __init__(self, Nombre, Apellido1, Apellido2, Telefono1, Telefono2, Correo1, Correo2, Empresa):
        self.Nombre = Nombre
        self.Apellido1 = Apellido1
        self.Apellido2 = Apellido2
        self.Telefono1 = Telefono1
        self.Telefono2 = Telefono2
        self.Correo1 = Correo1
        self.Correo2 = Correo2
        self.Empresa = Empresa
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()











