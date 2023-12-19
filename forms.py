from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField, IntegerField, BooleanField, SelectMultipleField, RadioField
from wtforms.validators import  DataRequired, Email, Length
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
    submit = SubmitField('Guardar Registro')

#Registro Contactos    
class Registro_contactos(FlaskForm):
    Nombre = StringField('Nombre', validators=[DataRequired(), Length(max=45)])
    Apellido1 = StringField('Primer Apellido', validators=[DataRequired(), Length(max=45)])
    Apellido2 = StringField('Segundo Apellido', validators=[DataRequired(), Length(max=45)])
    Telefono1 = IntegerField('Numero de telefono 1', validators=[DataRequired(), Length(max=45)])
    Telefono2 = IntegerField('Numero de telefono 2', validators=[DataRequired(), Length(max=45)])
    Correo1 = StringField('Correo 1º', validators=[DataRequired(), Email()])
    Correo2 = StringField('Correo 2º', validators=[DataRequired(), Email()])
    Empresa = StringField('Empresa', validators=[DataRequired(), Length(max=45)])
    submit = SubmitField('Guardar Contacto')


#Cambio contraseña
class Cambio_contraseña(FlaskForm):
    Password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Guardar')