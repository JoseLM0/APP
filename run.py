from flask import Flask, render_template, request, session, redirect, url_for, abort              
from forms import Cambio_contraseña, Registro, Registro_contactos, Login_form, Buscador, Ordenadoresform
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap  
import config 
from models import db, Usuarios, Contactos, Tareas, Ordenadores
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
    form = Buscador()    
    buscado = Usuarios.query 
    if form.validate_on_submit():
        busqueda = form.busqueda.data
        buscado = buscado.filter(Usuarios.Nombre.like('%' + busqueda + '%'))
        buscado = buscado.order_by(Usuarios.Nombre).all()
        return render_template('/buscarpersonal.html', form=form, busqueda = busqueda, buscado = buscado)
    return render_template("/personal.html", personal = insertObject, form = form)

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
    form = Buscador()    
    tareas = Tareas.query 
    if form.validate_on_submit():
        busqueda = form.busqueda.data
        tareas = tareas.filter(Tareas.Descripcion.like('%' + busqueda + '%'))
        tareas = tareas.order_by(Tareas.Titulo).all()
        return render_template('/buscartarea.html', form=form, busqueda = busqueda, tareas = tareas)
    return render_template('/tareas.html', tareas = insertObject, form=form)  




@app.route('/nuevatarea', methods=['POST'])
def nueva_tarea():
    titulo = request.form['Titulo']
    descripcion = request.form['Descripcion']
    estado = request.form['Estado']
    user = session['Usuario']
    puesto = session['Puesto']
    d = datetime.now()
    diaTarea = d.strftime("%Y-%m-%d %H:%M:%S")

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

@app.route('/listadecontactos', methods=['GET', 'POST'])
def contactos(): 
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM contactos")
    personal = cursor.fetchall()
    #Convertir a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in personal:
        insertObject.append(dict(zip(columnNames, record)))
        cursor.close()
    form = Buscador()    
    buscado = Contactos.query 
    if form.validate_on_submit():
        busqueda = form.busqueda.data
        buscado = buscado.filter(Contactos.Nombre.like('%' + busqueda + '%'))
        buscado = buscado.order_by(Contactos.Nombre).all()
        return render_template('/buscarcontactos.html', form=form, busqueda = busqueda, buscado = buscado)
    return render_template("/contactos.html", personal = insertObject, form = form)


@app.route('/nuevocontacto', methods=['GET', 'POST'])    
def nuevocontacto():
    form = Registro_contactos()
    d = datetime.now()
    diasubidad = d.strftime("%Y/%Y/%D $H:%M:%S")
    user = session['Usuario']
    if form.validate_on_submit():
        contacto = Contactos(Nombre = form.Nombre.data, Apellido1 = form.Apellido1.data, Apellido2 = form.Apellido2.data, Telefono1 = form.Telefono1.data, Telefono2 = form.Telefono2.data, Calle = form.Calle.data, Poblacion = form.Poblacion.data, Provincia = form.Provincia.data, Pais = form.Pais.data, Correo1 = form.Correo1.data, Correo2 = form.Correo2.data, Empresa = form.Empresa.data, fechasubida = diasubidad, usuariosubida = user)
        db.session.add(contacto)
        db.session.commit()
        print('FORM VALIDO')
        return redirect(url_for("contactos"))
    else:
        print('FORM falla')
    return render_template('/nuevocontacto.html', form=form)

@app.route('/borrarcontacto', methods=['POST'])
def borrarcontacto():
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM contactos WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('contactos'))

@app.route('/editarcontacto/<string:id>', methods = ['GET', 'POST'])
def editarcontacto(id):
    user = Contactos.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    form = Registro_contactos(request.form, obj=user) 
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("contactos"))   
    return render_template('/editarcontacto.html', form=form, perfil=True)

#EQUIPOS INFORMATICOS

@app.route('/equipos_informaticos', methods=['GET', 'POST'])
def equipos_informaticos(): 
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ordenadores")
    ordenadores = cursor.fetchall()
    #Convertir a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in ordenadores:
        insertObject.append(dict(zip(columnNames, record)))
        cursor.close()
    form = Buscador()    
    buscado = Ordenadores.query 
    if form.validate_on_submit():
        busqueda = form.busqueda.data
        buscado = buscado.filter(Ordenadores.Tipo.like('%' + busqueda + '%'))
        buscado = buscado.order_by(Ordenadores.Tipo).all()
        return render_template('/buscarequipos.html', form=form, busqueda = busqueda, buscado = buscado)
    return render_template('/e-informaticos.html', ordenadores = insertObject, form = form)


@app.route('/nuevoordenador', methods=['GET', 'POST'])    
def nuevoordenador():
    form = Ordenadoresform()
    d = datetime.now()
    diasubidad = d.strftime("%Y/%m/%d $H:%M:%S")
    user = session['Usuario']
    if form.validate_on_submit():
        contacto = Ordenadores(Codigo = form.Codigo.data, Tipo = form.Tipo.data, Estado = form.Estado.data, Activo = form.Activo.data, Fecompra = form.Fecompra.data, Proveedor = form.Proveedor.data, Factura = form.Factura.data, Marca = form.Marca.data, Modelo = form.Modelo.data, CPU = form.CPU.data, SO = form.SO.data, Lugar = form.Lugar.data, Encargado = form.Encargado.data, Observaciones = form.Observaciones.data, fsubida = diasubidad, Usubido = user)
        db.session.add(contacto)
        db.session.commit()
        print('FORM VALIDO')
        return redirect(url_for("equipos_informaticos"))
    else:
        print('FORM falla')
    return render_template('/nuevoequipo.html', form=form)

@app.route('/borrarordenador', methods=['POST'])
def borrarordenador():
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM ordenadores WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('equipos_informaticos'))

@app.route('/editarordenador/<string:id>', methods = ['GET', 'POST'])
def editarordenador(id):
    user = Ordenadores.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    form = Ordenadoresform(request.form, obj=user) 
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("equipos_informaticos"))   
    return render_template('/editarordenador.html', form=form, perfil=True)

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



