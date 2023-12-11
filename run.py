from flask import Flask, render_template, request              
import requests, json   
from forms import miformulario, Registro, Registro_contactos
from flask_bootstrap import Bootstrap  
import config 
from models import db, Usuarios, Contactos, Usuarios


app = Flask(__name__)   
Bootstrap(app)  
app.config.from_object(config)
db.init_app(app)


#INICIO

@app.route('/', methods=['GET'])    
def index():
    return render_template('/index.html') 

#Agenda
@app.route('/agenda', methods=['GET', 'POST'])    
def agenda():
    
    return render_template('/agenda.html')


#Contacto
@app.route('/contacto', methods=['GET', 'POST'])    
def contacto():
    form = Registro_contactos()
    if form.validate_on_submit():
        Nombre = form.Nombre.data
        Apellido1 = form.Apellido1.data
        Apellido2 = form.Apellido2.data
        Telefono1 = form.Telefono1.data
        Telefono2 = form.Telefono2.data
        Correo1 = form.Correo1.data
        Correo2 = form.Correo2.data
        Empresa = form.Empresa.data

        contacto_reg = Contactos(Nombre=Nombre, Apellido1=Apellido1, Apellido2=Apellido2, Telefono1=Telefono1, Telefono2=Telefono2, Correo1=Correo1, Correo2=Correo2, Empresa=Empresa)
        contacto_reg.save()
    
    
    return render_template('contacto.html', form=form)

#EQUIPOS INFORMATICOS
@app.route('/equipos_informaticos', methods=['GET'])
def equipos_informaticos():
    return render_template('/e-informaticos.html')

#Maquinaria
@app.route('/maquinaria', methods=['GET'])
def maquinaria():
    return render_template('/maquinaria.html')

#Vehiculos
@app.route('/vehiculos', methods=['GET'])
def vehiculos():
    return render_template('/vehiculos.html')

with app.app_context():
    db.create_all()
    db.session.commit()
    contacto_reg = Contactos.query.all()
    print(contacto_reg)


if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = '5001')  



