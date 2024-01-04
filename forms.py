from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, IntegerField, BooleanField, SelectMultipleField, RadioField, DateField
from wtforms.validators import  DataRequired, Email, Length, NumberRange
import email_validator

#AGENDA
class miformulario(FlaskForm):
    nombre = StringField(label = 'Nombre', validators=[DataRequired()])
    correo = StringField(label = 'Correo', validators=[DataRequired(), Email(granular_message=True)])
    mensaje = StringField(label = 'Mensaje', validators=[DataRequired()])
    submit = StringField(label = 'Enviar', validators=[DataRequired()])

#Registro USUARIOS
class Registro (FlaskForm):
    Usuario = StringField('Usuario', validators=[DataRequired(), Length(max=45)])
    Nombre = StringField('Nombre', validators=[DataRequired(), Length(max=45)])
    Apellido1 = StringField('Primer Apellido', validators=[DataRequired(), Length(max=45)])
    Apellido2 = StringField('Segundo Apellido', validators=[DataRequired(), Length(max=45)])
    Correo = StringField('Correo', validators=[DataRequired(), Email()])
    Password = PasswordField('Contraseña', validators=[DataRequired()])
    Puesto = RadioField('Nª Puesto', choices=[('1','ADMIN'), ('2','ALCALDE'), ('3','CONCEJALES'), ('4','ADMINISTRATIVOS'), ('5','USUARIO')], validators=[DataRequired()])
    NCuenta = StringField('Numero de Cuenta', validators=[DataRequired(), Length(max=30)])
    Comentarios = StringField('Comentarios', validators=[DataRequired(), Length(max=250)])
    submit = SubmitField('Guardar Registro')

#Registro Contactos    
class Registro_contactos(FlaskForm):
    Nombre = StringField('Nombre', validators=[DataRequired(), Length(max=45)])
    Apellido1 = StringField('Primer Apellido', validators=[DataRequired(), Length(max=45)])
    Apellido2 = StringField('Segundo Apellido', validators=[DataRequired(), Length(max=45)])
    Telefono1 = IntegerField('Numero de telefono 1', validators=[DataRequired(), NumberRange(max=99999999999)])
    Telefono2 = IntegerField('Numero de telefono 2', validators=[DataRequired(), NumberRange(max=99999999999)])
    Correo1 = StringField('Correo 1º', validators=[DataRequired(), Email()])
    Correo2 = StringField('Correo 2º', validators=[DataRequired(), Email()])
    Calle = StringField('Calle', validators=[DataRequired(), Length(max=90)])
    Poblacion = StringField('Poblacion', validators=[DataRequired(), Length(max=90)])
    Provincia = StringField('Provincia', validators=[DataRequired(), Length(max=90)])
    Pais = StringField('Pais', validators=[DataRequired(), Length(max=90)])
    Empresa = StringField('Empresa', validators=[DataRequired(), Length(max=45)])
    submit = SubmitField('Guardar Contacto')

#Form Login
class Login_form(FlaskForm):
    Usuario = StringField(label = 'Usuario', validators=[DataRequired()])   
    Password = PasswordField(label = 'Contraseña', validators=[DataRequired()])
    submit = SubmitField('Entrar')
#Cambio contraseña
class Cambio_contraseña(FlaskForm):
    Password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Guardar')

# Buscador    
class Buscador(FlaskForm):
    busqueda = StringField("Descripcion", validators=[DataRequired()])  
    submit = SubmitField('Entrar')

class Ordenadoresform(FlaskForm):
    Codigo = StringField('Codigo', validators=[DataRequired(), Length(max=10)])
    Tipo = StringField('Tipo', validators=[DataRequired(), Length(max=45)])
    Estado = StringField('Estado', validators=[DataRequired(), Length(max=10)])
    Activo = StringField('Activo', validators=[DataRequired(), Length(max=2)])
    Fecompra = DateField('Dia de compra del bien', format='%Y-%m-%d', validators=[DataRequired()])
    Activo = RadioField('Activo', choices=[('SI','Activo'), ('NO','Inactivo')], validators=[DataRequired()])
    Proveedor = StringField('Proveedor', validators=[DataRequired(), Length(max=90)]) 
    Factura = StringField('Factura', validators=[DataRequired(), Length(max=90)]) 
    Marca = StringField('Marca', validators=[DataRequired(), Length(max=90)]) 
    Modelo = StringField('Modelo', validators=[DataRequired(), Length(max=90)])
    CPU = StringField('CPU', validators=[DataRequired(), Length(max=90)]) 
    MemoriaRam = StringField('Memoria RAM', validators=[DataRequired(), Length(max=35)]) 
    SO = StringField('SO', validators=[DataRequired(), Length(max=45)]) 
    Lugar = StringField('Lugar', validators=[DataRequired(), Length(max=45)])  
    Encargado = StringField('Encargado', validators=[DataRequired(), Length(max=45)])     
    Observaciones = StringField('Observaciones', validators=[DataRequired(), Length(max=450)])  
    submit = SubmitField('Guardar')
