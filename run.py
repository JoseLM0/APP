from flask import Flask, render_template, request, session, redirect, url_for, abort              
from forms import Cambio_contraseña, Registro, Registro_contactos, Login_form, Buscador
from flask_bootstrap import Bootstrap  
import config 
from models import db, Usuarios, Contactos
from sqlalchemy.orm import sessionmaker
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.utils import secure_filename




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

@app.route('/login', methods=['GET','POST'])
def login():
    from login import abrir_sesion, estalogueado
    if estalogueado():
        return render_template('inicio')
    form = Login_form()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(Usuario = form.Usuario.data).first()
        if user is not None and user.verify_password(form.Password.data):
            abrir_sesion(user)      
            return redirect('inicio')
        form.Usuario.errors.append("Usuario o contraseña incorrecta")
    return render_template('login.html', form=form ) 
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


#Pestaña de Usuarios
@app.route('/registro', methods = ['GET', 'POST'])
def registro():
    #from login import es_admin
    #control permiso
    #if not es_admin():
        #abort(404)
    form = Registro()
    if form.validate_on_submit():
        existe_usuario = Usuarios.query.filter_by(Usuario=form.Usuario.data).first()
        if existe_usuario is None:
            user = Usuarios()
            form.populate_obj(user)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("inicio"))
        form.username.errors.append("Nombre de usuario ya existente")
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

#ADMINISTRAR de personal


@app.route('/listadepersonal', methods=['GET', 'POST'])
def personal():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM usuarios")
    personal = cursor.fetchall()
    #Convertir a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in personal:
        insertObject.append(dict(zip(columnNames, record)))
        cursor.close()

    return render_template("/personal.html", personal = insertObject)

@app.route('/borrarpersonal', methods=['POST'])
def borrarpersonal():
    from login import es_admin
    #control permiso
    if not es_admin():
        abort(404)
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM usuarios WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('listadepersonal'))

@app.route('/editarpersonal/<string:id>', methods = ['GET', 'POST'])
def editarpersonal(id):
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    form = Registro(request.form, obj=user) 
    del form.Password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("personal"))   
    return render_template('/editarpersonal.html', form=form, perfil=True)

@app.route('/editarcontraseña/<string:id>', methods =['GET', 'POST'])
def editarcontraseña(id):
    user = Usuarios.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    form = Cambio_contraseña()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("personal"))
    return render_template("/editarcontraseña.html", form = form, perfil=True)


   
#Tareas
@app.route('/tareas', methods=['GET', 'POST'])
def tareas():
    puesto = session['Puesto']
    cur = mysql.connection.cursor()
    cur.execute("SElECT * FROM tareas WHERE id_puesto >= %s", [puesto])
    tareas = cur.fetchall()

    insertObject = []
    columnNames = [column[0] for column in cur.description]
    for record in tareas:
        insertObject.append(dict(zip(columnNames, record)))
    cur.close()
    if request.method == "POST":
        search   = request.form["buscar"]
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tareas WHERE Descripcion LIKE %s ORDER BY id  DESC", [search])
        tareas = cur.fetchall()
        insertObject = []
        columnNames = [column[0] for column in cur.description]
        for record in tareas:
            insertObject.append(dict(zip(columnNames, record)))
        cur.close()    
        return render_template('/buscartarea.html', tareas = insertObject, busqueda = search )   
    return render_template('/tareas.html', tareas = insertObject)  

 

@app.route('/nuevatarea', methods=['POST'])
def nueva_tarea():
    titulo = request.form['Titulo']
    descripcion = request.form['Descripcion']
    estado = request.form['Estado']
    user = session['Usuario']
    puesto = session['Puesto']
    d = datetime.now()
    diaTarea = d.strftime("%Y-%m-%d $H:%M:%S")

    if titulo and descripcion and user and estado: 
        cur = mysql.connection.cursor()
        sql = "INSERT INTO  tareas (Usuario, id_puesto, Titulo, Descripcion, FECHA, Estado) VALUES (%s, %s, %s, %s, %s, %s)"
        data = (user, puesto, titulo, descripcion, diaTarea, estado)
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
    d = datetime.now()
    diaTarea = d.strftime("%Y-%m-%d $H:%M:%S")

    if titulo and descripcion and estado: 
        cursor = mysql.connection.cursor()
        sql = "UPDATE tareas SET Titulo = %s, Descripcion = %s, FECHA = %s, Estado = %s WHERE id = %s"
        data = (titulo, descripcion, diaTarea, estado, id)
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



