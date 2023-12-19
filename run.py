from flask import Flask, render_template, request, session, redirect, url_for, abort              
from forms import Cambio_contraseña, Registro, Registro_contactos
from flask_bootstrap import Bootstrap  
import config 
from models import db, Usuarios, Contactos
from sqlalchemy.orm import sessionmaker
from flask_mysqldb import MySQL
from datetime import datetime
from login import abrir_sesion


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
    

#Login y Logout. OPCIONES DE LOGIN

@app.route('/login', methods=['POST'])
def login():

    user = request.form['Usuario']
    password = request.form['Password']

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE Usuario = %s AND Password = %s",(user, password))
    usuarios = cur.fetchone()
    cur.close()

    if  usuarios is not None:
        session['Usuario'] = user
        session['Nombre'] = usuarios[2]
        session['Apellido1'] = usuarios[3]
        session['Puesto'] = usuarios[7]
        
        if session['Puesto']==1:
            return render_template('/tareas.html')
        
        elif session['Puesto']<1:
            return render_template('/inicio.html')

        return redirect('inicio')
    else:
        return render_template('index.html', message="Error datos incorrectos vuelva a intentarlo") 
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))







#Pestaña de Usuarios
@app.route('/registro', methods = ['GET', 'POST'])
def registro():
    form = Registro()
    if form.validate_on_submit():
        Nombre = form.Nombre.data
        Usuario = form.Usuario.data
        Apellido1 = form.Apellido1.data
        Apellido2 = form.Apellido2.data
        Correo = form.Correo.data
        Password = form.Password.data

        user = Usuarios(Nombre = Nombre, Usuario = Usuario, Apellido1 = Apellido1, Apellido2 = Apellido2, Correo = Correo, Password = Password)
        user.set_Password(Password) 
        user.save()

    return render_template('/registro.html', form=form)

@app.route('/perfil/<Usuario>', methods = ['GET', 'POST'])
def perfil(Usuario):
    user = Usuarios.query.filter_by(Usuario=Usuario).first()
    if user is None:
        abort(404)
    form = Registro(request.form, obj=user) 
    del form.Password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))   
    return render_template('/registro.html', form=form, perfil=True)

@app.route('/cambiarcontraseña/<Usuario>', methods =['GET', 'POST'])
def cambiarcontraseña(Usuario):
    user = Usuarios.query.filter_by(Usuario=Usuario).first()
    if user is None:
        abort(404)
    form = Cambio_contraseña()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("/cambiarcontraseña.html", form = form)

   
#Tareas
@app.route('/tareas', methods=['GET'])
def tareas():
    user = session['Usuario']
    cur = mysql.connection.cursor()
    cur.execute("SElECT * FROM tareas WHERE Usuario = %s", [user])
    tareas = cur.fetchall()

    insertObject = []
    columnNames = [column[0] for column in cur.description]
    for record in tareas:
        insertObject.append(dict(zip(columnNames, record)))
    cur.close()    
    return render_template('/tareas.html', tareas = insertObject)  

@app.route('/nuevatarea', methods=['POST'])
def nueva_tarea():
    titulo = request.form['Titulo']
    descripcion = request.form['Descripcion']
    estado = request.form['Estado']
    user = session['Usuario']
    d = datetime.now()
    diaTarea = d.strftime("%Y-%m-%d $H:%M:%S")

    if titulo and descripcion and user and estado: 
        cur = mysql.connection.cursor()
        sql = "INSERT INTO  tareas (Usuario, Titulo, Descripcion, FECHA, Estado) VALUES (%s, %s, %s, %s, %s)"
        data = (user, titulo, descripcion, diaTarea, estado)
        cur.execute(sql, data)
        mysql.connection.commit()
    return redirect(url_for('tareas'))
    
@app.route('/borrartarea', methods=['POST'])
def borrartarea():
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM tareas WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('tareas'))

@app.route('/editartareas/<string:id>', methods=['POST'])
def editartareas(id):
    
    titulo = request.form['Titulo']
    descripcion = request.form['Descripcion']
    estado = request.form['Estado']
    user = session['Usuario']
    d = datetime.now()
    diaTarea = d.strftime("%Y-%m-%d $H:%M:%S")

    if titulo and descripcion and estado: 
        cursor = mysql.connection.cursor()
        sql = "UPDATE tareas SET Usuario = %s, Titulo = %s, Descripcion = %s, FECHA = %s, Estado = %s WHERE id = %s"
        data = ( user, titulo, descripcion, diaTarea, estado, id)
        cursor.execute(sql, data)
        mysql.connection.commit()
    return redirect(url_for('tareas'))


@app.route('/vuelta', methods=['GET'])
def vuelta():
    return render_template('/e-informaticos.html')
   



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




with app.app_context():
    db.create_all()
    db.session.commit()

    users = Usuarios.query.all()
    print(users)


if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = '5001')  



