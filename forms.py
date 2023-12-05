from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from wtforms.validators import  DataRequired, Email
import email_validator

class miformulario(FlaskForm):
    nombre = StringField(label = 'Nombre', validators=[DataRequired()])
    correo = StringField(label = 'Correo', validators=[DataRequired(), Email(granular_message=True)])
    mensaje = StringField(label = 'Mensaje', validators=[DataRequired()])
    submit = StringField(label = 'Enviar', validators=[DataRequired()])