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
    NCuenta = db.Column(db.String(30), nullable = True )
    Comentarios = db.Column(db.String(250), nullable = True )

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

    #Flask Login Interaciones  
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    

class Contactos(db.Model):
    __tablename__="contactos"
    id = db.Column(db.Integer, primary_key = True)
    Nombre = db.Column(db.String(45), nullable= False)
    Apellido1 = db.Column(db.String(45), nullable= False)
    Apellido2 = db.Column(db.String(45), nullable= True)
    Telefono1 = db.Column(db.Integer, nullable = True, default = 0)
    Telefono2 = db.Column(db.Integer, nullable = True, default = 0)
    Correo1 = db.Column(db.String(45), nullable= True)
    Correo2 = db.Column(db.String(45), nullable= True)
    Calle = db.Column(db.String(450), nullable= True)
    Poblacion = db.Column(db.String(450), nullable= True)
    Provincia = db.Column(db.String(450), nullable= True)
    Pais = db.Column(db.String(450), nullable= True)
    Empresa = db.Column(db.String(45), nullable= True)
    fechasubida = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    usuariosubida = db.Column(db.String(45), nullable= True)

class Tareas(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    Usuario = db.Column(db.String(45), nullable= False)
    id_puesto = db.Column(db.Integer, nullable= False)
    Titulo = db.Column(db.String(120), nullable= False)
    Descripcion = db.Column(db.String(500), nullable= False)
    FECHA = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Estado = db.Column(db.String(35), nullable= False)
   
class Ordenadores(db.Model):
    __tablename__="Ordenadores"
    id = db.Column(db.Integer, primary_key = True)
    Codigo = db.Column(db.String(10), nullable= False)
    Tipo = db.Column(db.String(45), nullable= False)
    Estado = db.Column(db.String(10), nullable= True)
    Activo = db.Column(db.String(2), nullable= True)
    Fecompra = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Proveedor = db.Column(db.String(90), nullable= True)
    Factura = db.Column(db.String(90), nullable= True)
    Marca = db.Column(db.String(45), nullable= True)
    Modelo = db.Column(db.String(90), nullable= True)
    CPU = db.Column(db.String(45), nullable= True)
    MemoriaRam = db.Column(db.String(35), nullable= True)
    SO = db.Column(db.String(45), nullable= True)
    Lugar = db.Column(db.String(45), nullable= True)
    Usubido = db.Column(db.String(45), nullable= True)
    fsubida = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Encargado = db.Column(db.String(45), nullable= True)
    Observaciones = db.Column(db.String(450), nullable= True)

class Maquinaria(db.Model):
    __tablename__="Maquinaria"
    id = db.Column(db.Integer, primary_key = True)
    Codigo = db.Column(db.String(10), nullable= False)
    Tipo = db.Column(db.String(45), nullable= False)
    Estado = db.Column(db.String(10), nullable= True)
    Activo = db.Column(db.String(2), nullable= True)
    Fecompra = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Proveedor = db.Column(db.String(90), nullable= True)
    Factura = db.Column(db.String(90), nullable= True)
    Marca = db.Column(db.String(45), nullable= True)
    Modelo = db.Column(db.String(90), nullable= True)
    NSerie = db.Column(db.String(45), nullable= True)
    Lugar = db.Column(db.String(45), nullable= True)
    Usubido = db.Column(db.String(45), nullable= True)
    fsubida = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Encargado = db.Column(db.String(45), nullable= True)
    Observaciones = db.Column(db.String(450), nullable= True)    

class Vehiculos(db.Model):
    __tablename__="Vehiculos"
    id = db.Column(db.Integer, primary_key = True)
    Codigo = db.Column(db.String(10), nullable= False)
    Tipo = db.Column(db.String(45), nullable= False)
    Estado = db.Column(db.String(10), nullable= True)
    Activo = db.Column(db.String(2), nullable= True)
    Fecompra = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Fematri = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Proveedor = db.Column(db.String(90), nullable= True)
    Factura = db.Column(db.String(90), nullable= True)
    Marca = db.Column(db.String(45), nullable= True)
    Modelo = db.Column(db.String(90), nullable= True)
    Matricula = db.Column(db.String(10), nullable= True)
    NSerie = db.Column(db.String(35), nullable= True)
    ITV = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Lugar = db.Column(db.String(45), nullable= True)
    Usubido = db.Column(db.String(45), nullable= True)
    fsubida = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    Encargado = db.Column(db.String(45), nullable= True)
    Observaciones = db.Column(db.String(450), nullable= True)

class Puesto(db.Model):
    __tablename__="Puestos"
    id_rol = db.Column(db.Integer, primary_key = True)
    Descripcion = db.Column(db.String(50), nullable= False)

