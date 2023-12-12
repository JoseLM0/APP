from flask import Flask, render_template, request, session, redirect, url_for                
import requests, json   
from forms import miformulario, Registro, Registro_contactos
from flask_bootstrap import Bootstrap  
import config 
from models import db, Usuarios, Contactos
from sqlalchemy.orm import sessionmaker
from flask_mysqldb import MySQL

app = Flask(__name__)   
Bootstrap(app)  
app.config.from_object(config)
db.init_app(app)
app.config['SECRET_KEY'] = config.HEX_SEC_KEY
app.config['MYSQLS_HOST'] = config.MYSQL_HOST
app.config['MYSQLS_USER'] = config.MYSQL_USER
app.config['MYSQLS_PASSWORD'] = config.MYSQL_PASSWORD
app.config['MYSQL_DB'] = config.MYSQL_DB

mysql = MySQL(app)


#INICIO

@app.route('/', methods=['GET'])   #Inicio sesion 
def index():
    return render_template('/index.html') 

@app.route('/inicio', methods=['GET'])    
def inicio():
    return render_template('/inicio.html') 
    

#Login

@app.route('/login', methods=['POST'])
def login():
    correo = request.form['Correo']
    password = request.form['Password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE Correo = %s AND Password = %s",(correo, password))
    usuarios = cur.fetchone()
    cur.close()

    if  usuarios is not None:
        session['Correo'] = correo
        session['Nombre'] = usuarios[1]
        session['Apellido1'] = usuarios[2]

        return redirect('inicio')
    else:
        return render_template('index.html', message="Error datos incorrectos vuelva a intentarlo") 


#Registro usuarios
@app.route('/registro', methods = ['GET', 'POST'])
def registro():
    form = Registro()
    if form.validate_on_submit():
        Nombre = form.Nombre.data
        Apellido1 = form.Apellido1.data
        Apellido2 = form.Apellido2.data
        Correo = form.Correo.data
        Password = form.Password.data

        user = Usuarios(Nombre = Nombre, Apellido1 = Apellido1, Apellido2 = Apellido2, Correo = Correo, Password = Password)
        user.set_Password(Password) 
        user.save()


    return render_template('/registro.html', form=form)


   
#Tareas
@app.route('/tareas', methods=['GET'])
def tareas():
    return render_template('/tareas.html')  

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

        contacto_reg = Contactos(Nombre = Nombre, Apellido1 = Apellido1, Apellido2 = Apellido2, Telefono1 = Telefono1, Telefono2 = Telefono2, Correo1 = Correo1, Correo2 = Correo2, Empresa = Empresa)
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


#SALIR
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for(login))


with app.app_context():
    db.create_all()
    db.session.commit()

    users = Usuarios.query.all()
    print(users)


if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = '5001')  



