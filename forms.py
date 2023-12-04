from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField
from wtforms.validators import  DataRequired

class miformulario(FlaskForm):
    nombre = StringField(label = 'Nombre', validators=[DataRequired()])
    correo = StringField(label = 'Correo', validators=[DataRequired()])
    mensaje = StringField(label = 'Mensaje', validators=[DataRequired()])
    enviar = StringField(label = 'Enviar', validators=[DataRequired()])