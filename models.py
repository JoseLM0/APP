from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy 
db = SQLAlchemy()

class Usuarios(db.Model, UserMixin):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key = True)
    Usuario = db.Column(db.String(50), nullable= False)
    Nombre = db.Column(db.String(45), nullable= False)
    Apellido1 = db.Column(db.String(45), nullable= False)
    Apellido2 = db.Column(db.String(45), nullable= False)
    Correo = db.Column(db.String(45), nullable= False)
    password_hash = db.Column(db.String(250), nullable= False)
    Puesto = db.Column(db.Integer, nullable = False, default = 5)

    def __repr__(self):
        return (u'<{self.__class__.__name__}: {self.id}>'.format(self=self))
    @property
    def Password(self):
        raise AttributeError('password is not a readable atribute')
    
    @Password.setter
    def Password(self, Password):
        self.password_hash = generate_password_hash(Password)

    def verify_password(self, Password):
        return check_password_hash(self.password_hash, Password)
    
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
        self.date = datetime.utcnow()
    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()











