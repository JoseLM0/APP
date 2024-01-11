from flask import Flask, render_template, request, session, redirect, url_for, abort              
from forms import Cambio_contraseña, Registro, Registro_contactos, Login_form, Buscador, Ordenadoresform, MaquinariaForm, VehiculosForm, FiltroTareasForm
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap  
import config 
from models import db, Usuarios, Contactos, Tareas, Ordenadores, Maquinaria, Vehiculos, Puesto
from sqlalchemy import or_ 
from flask_login import LoginManager,login_user,logout_user,login_required,current_user
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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

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
    if current_user.is_authenticated:
        return redirect(url_for("inicio"))
    form = Login_form()
    if form.validate_on_submit():
        user = Usuarios.query.filter_by(Usuario = form.Usuario.data).first()
        if user is not None and user.verify_password(form.Password.data):
            login_user(user)      
            print(user)
            return redirect('inicio')
        form.Usuario.errors.append("Usuario o contraseña incorrecta")
    return render_template('login.html', form=form ) 
    

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


#Pestaña de Usuarios
@app.route('/registro', methods = ['GET', 'POST'])
@login_required
def registro():
    form = Registro()
    del  form.Puesto
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
@login_required
def perfil(Usuario):
    user = Usuarios.query.filter_by(Usuario=Usuario).first()
    form = Registro(request.form, obj=user) 
    del form.Usuario, form.Password, form.Puesto
    if not Usuario == current_user.Usuario:
        abort(404)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))   
    return render_template('/registro.html', form=form, perfil=True)

@app.route('/cambiarcontraseña/<Usuario>', methods =['GET', 'POST'])
@login_required
def cambiarcontraseña(Usuario):
    user = Usuarios.query.filter_by(Usuario=Usuario).first()
    if user is None:
        abort(404)
    form = Cambio_contraseña()
    if not Usuario == current_user.Usuario:
        abort(404)
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("inicio"))
    return render_template("/cambiarcontraseña.html", form = form)

#ADMINISTRAR de personal


@app.route('/listadepersonal', methods=['GET', 'POST'])
@login_required
def personal(): 
    #SEGURIDAD 
    admin = current_user.Puesto <= 4
    if admin is False:
        abort(404)
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
        return render_template('/buscarpersonal.html', form=form, busqueda = busqueda, buscado = buscado )
    return render_template("/personal.html", personal = insertObject, form = form)

@app.route('/borrarpersonal', methods=['POST'])
@login_required
def borrarpersonal():
    #SEGURIDAD 
    admin = current_user.Puesto <= 2
    if admin is False:
        abort(404)
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM usuarios WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('listadepersonal'))

@app.route('/editarpersonal/<string:id>', methods = ['GET', 'POST'])
@login_required
def editarpersonal(id):
    #SEGURIDAD 
    admin = current_user.Puesto <= 2
    if admin is False:
        abort(404)
    user = Usuarios.query.filter_by(id=id).first()
    form = Registro(request.form, obj=user) 
    del form.Password
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("personal"))   
    return render_template('/editarpersonal.html', form=form, perfil=True)

@app.route('/editarcontraseña/<string:id>', methods =['GET', 'POST'])
@login_required
def editarcontraseña(id):
    #SEGURIDAD 
    admin = current_user.Puesto <= 2
    if admin is False:
        abort(404)
    user = Usuarios.query.filter_by(id=id).first()
    form = Cambio_contraseña()
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("personal"))
    return render_template("/editarcontraseña.html", form = form, perfil=True)


   
#Tareas
@app.route('/tareas', methods=['GET', 'POST'])
@login_required
def tareas():
    permiso = current_user.Puesto <= 4
    if permiso is False:
        abort(404)  
    puesto = current_user.Puesto
    forma = FiltroTareasForm()
    form = Buscador()    
    cur = mysql.connection.cursor()
    if forma.validate_on_submit():
        esta = forma.Esta.data
        if esta == "5":
            return redirect(url_for("tareas"))
        cur.execute("SElECT * FROM tareas WHERE id_puesto >= %s AND estado = %s", [puesto, esta])
        tareas = cur.fetchall()
        insertObject = []
        columnNames = [column[0] for column in cur.description]
        for record in tareas:
            insertObject.append(dict(zip(columnNames, record)))
        cur.close()
        return render_template('/tareas.html', tareas = insertObject, form=form, forma = forma, esta = esta) 
    else:
        cur.execute("SElECT * FROM tareas WHERE id_puesto >= %s", [puesto])
        tareas = cur.fetchall()
        insertObject = []
        columnNames = [column[0] for column in cur.description]
        for record in tareas:
            insertObject.append(dict(zip(columnNames, record)))
        cur.close()
    tareas = Tareas.query 
    if form.validate_on_submit():
        busqueda = form.busqueda.data
        if busqueda is not True:
            tareas = tareas.filter(or_(Tareas.Titulo.like('%' + busqueda + '%'),Tareas.Descripcion.like('%' + busqueda + '%')))
            tareas = tareas.order_by(Tareas.Titulo).all()
            return render_template('/buscartarea.html', form=form, busqueda = busqueda, tareas = tareas)
        
    return render_template('/tareas.html', tareas = insertObject, form=form, forma = forma)  



@app.route('/nuevatarea', methods=['POST'])
@login_required
def nueva_tarea():
    permiso = current_user.Puesto <= 4
    if permiso is False:
        abort(404)  
    titulo = request.form['Titulo']
    descripcion = request.form['Descripcion']
    estado = request.form['Estado']
    user = current_user.Usuario
    puesto = current_user.Puesto
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
@login_required
def borrartarea():
    permiso = current_user.Puesto <= 4
    if permiso is False:
        abort(404)  
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM tareas WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('tareas'))

@app.route('/editartareas/<string:id>', methods=['POST'])
@login_required
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


@app.route('/prueba', methods=['GET'])
@login_required
def prueba():
    return render_template('/prueba.html')
   



#Contacto

@app.route('/listadecontactos', methods=['GET', 'POST'])
def contactos():
    from login import estalogueado
    if not estalogueado:
        abort(404) 
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
        buscado = buscado.filter(or_(Contactos.Nombre.like('%' + busqueda + '%'),
                                       Contactos.Apellido1.like('%' + busqueda + '%'),
                                       Contactos.Apellido2.like('%' + busqueda + '%'),
                                       Contactos.Telefono1.like('%' + busqueda + '%'),
                                       Contactos.Telefono2.like('%' + busqueda + '%'),
                                       Contactos.Correo1.like('%' + busqueda + '%'),
                                       Contactos.Correo2.like('%' + busqueda + '%'),
                                       Contactos.Calle.like('%' + busqueda + '%'),
                                       Contactos.Poblacion.like('%' + busqueda + '%'),
                                       Contactos.Provincia.like('%' + busqueda + '%'),
                                       Contactos.Pais.like('%' + busqueda + '%'),
                                       Contactos.Empresa.like('%' + busqueda + '%'),
                                       Contactos.fechasubida.like('%' + busqueda + '%'),
                                       Contactos.usuariosubida.like('%' + busqueda + '%'),                                      
                                       
                                       ))
        buscado = buscado.order_by(Contactos.Nombre).all()
        return render_template('/buscarcontactos.html', form=form, busqueda = busqueda, buscado = buscado)
    return render_template("/contactos.html", personal = insertObject, form = form)


@app.route('/nuevocontacto', methods=['GET', 'POST'])    
@login_required
def nuevocontacto():
    form = Registro_contactos()
    d = datetime.now()
    diasubidad = d.strftime("%Y-%m-%d $H:%M:%S")
    user = current_user.Usuario
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
@login_required
def borrarcontacto():
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM contactos WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('contactos'))

@app.route('/editarcontacto/<string:id>', methods = ['GET', 'POST'])
@login_required
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
        buscado = buscado.filter(or_(Ordenadores.Codigo.like('%' + busqueda + '%'),
                                       Ordenadores.Tipo.like('%' + busqueda + '%'),
                                       Ordenadores.Estado.like('%' + busqueda + '%'),
                                       Ordenadores.Activo.like('%' + busqueda + '%'),
                                       Ordenadores.Fecompra.like('%' + busqueda + '%'),
                                       Ordenadores.Activo.like('%' + busqueda + '%'),
                                       Ordenadores.Proveedor.like('%' + busqueda + '%'),
                                       Ordenadores.Factura.like('%' + busqueda + '%'),
                                       Ordenadores.Marca.like('%' + busqueda + '%'),
                                       Ordenadores.Modelo.like('%' + busqueda + '%'),
                                       Ordenadores.CPU.like('%' + busqueda + '%'),
                                       Ordenadores.MemoriaRam.like('%' + busqueda + '%'),
                                       Ordenadores.SO.like('%' + busqueda + '%'),
                                       Ordenadores.Encargado.like('%' + busqueda + '%'),
                                       Ordenadores.Observaciones.like('%' + busqueda + '%'),
                                           ))
        buscado = buscado.order_by(Ordenadores.Tipo).all()
        return render_template('/buscarequipos.html', form=form, busqueda = busqueda, buscado = buscado)
    return render_template('/e-informaticos.html', ordenadores = insertObject, form = form)


@app.route('/nuevoordenador', methods=['GET', 'POST'])    
@login_required
def nuevoordenador():
    form = Ordenadoresform()
    d = datetime.now()
    diasubidad = d.strftime("%Y-%m-%d $H:%M:%S")
    user = current_user.Usuario
    if form.validate_on_submit():
        contacto = Ordenadores(Codigo = form.Codigo.data, Tipo = form.Tipo.data, Estado = form.Estado.data, Activo = form.Activo.data, Fecompra = form.Fecompra.data, Proveedor = form.Proveedor.data, Factura = form.Factura.data, Marca = form.Marca.data, Modelo = form.Modelo.data, CPU = form.CPU.data, SO = form.SO.data, MemoriaRam = form.MemoriaRam.data, Lugar = form.Lugar.data, Encargado = form.Encargado.data, Observaciones = form.Observaciones.data, fsubida = diasubidad, Usubido = user)
        db.session.add(contacto)
        db.session.commit()
        print('FORM VALIDO')
        return redirect(url_for("equipos_informaticos"))
    else:
        print('FORM falla')
    return render_template('/nuevoequipo.html', form=form)

@app.route('/borrarordenador', methods=['POST'])
@login_required
def borrarordenador():
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM ordenadores WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('equipos_informaticos'))

@app.route('/editarordenador/<string:id>', methods = ['GET', 'POST'])
@login_required
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


@app.route('/maquinaria', methods=['GET', 'POST'])
def maquinaria(): 
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM maquinaria")
    maquinaria = cursor.fetchall()
    #Convertir a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in maquinaria:
        insertObject.append(dict(zip(columnNames, record)))
        cursor.close()
    form = Buscador()    
    buscado = Maquinaria.query 
    if form.validate_on_submit():
        busqueda = form.busqueda.data
        buscado = buscado.filter((or_(Maquinaria.Codigo.like('%' + busqueda + '%'),
                                       Maquinaria.Tipo.like('%' + busqueda + '%'),
                                       Maquinaria.Estado.like('%' + busqueda + '%'),
                                       Maquinaria.Activo.like('%' + busqueda + '%'),
                                       Maquinaria.Fecompra.like('%' + busqueda + '%'),
                                       Maquinaria.Proveedor.like('%' + busqueda + '%'),
                                       Maquinaria.Factura.like('%' + busqueda + '%'),
                                       Maquinaria.Marca.like('%' + busqueda + '%'),
                                       Maquinaria.Modelo.like('%' + busqueda + '%'),
                                       Maquinaria.NSerie.like('%' + busqueda + '%'),
                                       Maquinaria.Lugar.like('%' + busqueda + '%'),
                                       Maquinaria.Usubido.like('%' + busqueda + '%'),
                                       Maquinaria.Encargado.like('%' + busqueda + '%'),
                                       Maquinaria.Observaciones.like('%' + busqueda + '%'),                                                                            
                                       )))
        buscado = buscado.order_by(Maquinaria.Tipo).all()
        return render_template('/buscarmaquinaria.html', form=form, busqueda = busqueda, buscado = buscado)
    return render_template('/maquinaria.html', maquinaria = insertObject, form = form)


@app.route('/nuevamaquinaria', methods=['GET', 'POST']) 
@login_required   
def nuevamaquinaria():
    form = MaquinariaForm()
    d = datetime.now()
    diasubidad = d.strftime("%Y-%m-%d $H:%M:%S")
    user = current_user.Usuario
    if form.validate_on_submit():
        nuevo = Maquinaria(Codigo = form.Codigo.data, Tipo = form.Tipo.data, Estado = form.Estado.data, Activo = form.Activo.data, Fecompra = form.Fecompra.data, Proveedor = form.Proveedor.data, Factura = form.Factura.data, Marca = form.Marca.data, Modelo = form.Modelo.data, NSerie = form.NSerie.data, Lugar = form.Lugar.data, Encargado = form.Encargado.data, Observaciones = form.Observaciones.data, fsubida = diasubidad, Usubido = user)
        db.session.add(nuevo)
        db.session.commit()
        print('FORM VALIDO')
        return redirect(url_for("maquinaria"))
    else:
        print('FORM falla')
    return render_template('/nuevamaquina.html', form=form)

@app.route('/borrarmaquina', methods=['POST'])
@login_required
def borrarmaquina():
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM maquinaria WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('maquinaria'))

@app.route('/editarmaquinaria/<string:id>', methods = ['GET', 'POST'])
@login_required
def editarmaquinaria(id):
    user = Maquinaria.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    form = MaquinariaForm(request.form, obj=user) 
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("maquinaria"))   
    return render_template('/editarmaquinaria.html', form=form, perfil=True)    

#Vehiculos


@app.route('/vehiculos', methods=['GET', 'POST'])
def vehiculos(): 
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM vehiculos")
    vehiculos = cursor.fetchall()
    #Convertir a diccionario
    insertObject = []
    columnNames = [column[0] for column in cursor.description]
    for record in vehiculos:
        insertObject.append(dict(zip(columnNames, record)))
        cursor.close()
    form = Buscador()    
    buscado = Vehiculos.query 
    if form.validate_on_submit():
        busqueda = form.busqueda.data
        buscado = buscado.filter((or_(Vehiculos.Codigo.like('%' + busqueda + '%'),
                                       Vehiculos.Tipo.like('%' + busqueda + '%'),
                                       Vehiculos.Estado.like('%' + busqueda + '%'),
                                       Vehiculos.Activo.like('%' + busqueda + '%'),
                                       Vehiculos.Fecompra.like('%' + busqueda + '%'),
                                       Vehiculos.Fematri.like('%' + busqueda + '%'),
                                       Vehiculos.Proveedor.like('%' + busqueda + '%'),
                                       Vehiculos.Factura.like('%' + busqueda + '%'),
                                       Vehiculos.Marca.like('%' + busqueda + '%'),
                                       Vehiculos.Modelo.like('%' + busqueda + '%'),
                                       Vehiculos.Matricula.like('%' + busqueda + '%'),
                                       Vehiculos.NSerie.like('%' + busqueda + '%'),
                                       Vehiculos.ITV.like('%' + busqueda + '%'),
                                       Vehiculos.Lugar.like('%' + busqueda + '%'),
                                       Vehiculos.Encargado.like('%' + busqueda + '%'),
                                       Vehiculos.Observaciones.like('%' + busqueda + '%'),                                                                              
                                       )))
        buscado = buscado.order_by(Vehiculos.Tipo).all()
        return render_template('/buscarvehiculos.html', form=form, busqueda = busqueda, buscado = buscado)
    return render_template('/vehiculos.html', vehiculos = insertObject, form = form)


@app.route('/nuevovehiculos', methods=['GET', 'POST'])   
@login_required 
def nuevovehiculos():
    form = VehiculosForm()
    d = datetime.now()
    diasubidad = d.strftime("%Y-%m-%d $H:%M:%S")
    user = current_user.Usuario
    if form.validate_on_submit():
        contacto = Vehiculos(Codigo = form.Codigo.data, Tipo = form.Tipo.data, Estado = form.Estado.data, Activo = form.Activo.data, Fecompra = form.Fecompra.data, Fematri = form.Fematri.data, Proveedor = form.Proveedor.data, Factura = form.Factura.data, Marca = form.Marca.data, Modelo = form.Modelo.data, Matricula = form.Matricula.data, ITV = form.ITV.data, NSerie = form.NSerie.data, Lugar = form.Lugar.data, Encargado = form.Encargado.data, Observaciones = form.Observaciones.data, fsubida = diasubidad, Usubido = user)
        db.session.add(contacto)
        db.session.commit()
        print('FORM VALIDO')
        return redirect(url_for("vehiculos"))
    else:
        print('FORM falla')
    return render_template('/nuevovehiculos.html', form=form)

@app.route('/borrarvehiculos', methods=['POST'])
@login_required
def borrarvehiculos():
    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM vehiculos WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('vehiculos'))

@app.route('/editarvehiculos/<string:id>', methods = ['GET', 'POST'])
@login_required
def editarvehiculos(id):
    user = Vehiculos.query.filter_by(id=id).first()
    if user is None:
        abort(404)
    form = VehiculosForm(request.form, obj=user) 
    if form.validate_on_submit():
        form.populate_obj(user)
        db.session.commit()
        return redirect(url_for("vehiculos"))   
    return render_template('/editarvehiculos.html', form=form, perfil=True)


@login_manager.user_loader
def load_user(id):
	return Usuarios.query.get(int(id))





print(load_user)
#with app.app_context():
    #db.create_all()
    #db.session.commit()

    #users = Usuarios.query.all()
    #print(users)



if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = '5001')  



