from flask import Flask, render_template, request              

app = Flask(__name__)    
#INICIO
<<<<<<< HEAD
@app.route('/', methods={'GET', 'POST'})    
def index():
    if request.method == 'POST':
        nombre = request.form['Nombre'] 
        return render_template('/index.html', nombre = nombre)  
    else:  
        return render_template('/index.html') 

<<<<<<< HEAD
#AGENDA
@app.route('/agenda', methods=['GET'])    
def agenda():
    return render_template('/agenda.html')

#Contato
@app.route('/Contacto')
def contacto():
    return render_template('/contacto.html')    
=======
=======
>>>>>>> Vistas
@app.route('/', methods={'GET', 'POST'})    
def index():
    if request.method == 'POST':
        nombre = request.form['Nombre'] 
        return render_template('/index.html', nombre = nombre)  
    else:  
        return render_template('/index.html') 

#Agenda
@app.route('/agenda', methods=['GET'])    
def agenda():
    return render_template('/agenda.html')
#Contacto
@app.route('/contacto', methods=['GET'])    
def contacto():
<<<<<<< HEAD
    return render_template('contacto.html')
>>>>>>> Vistas
=======
    return render_template('/contacto.html')

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
>>>>>>> Vistas

if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = '5001')  

     
