from flask import Flask, render_template, request              
import requests, json   
from forms import miformulario
from flask_bootstrap import Bootstrap
from flask_recaptcha import ReCaptcha   
from markupsafe import Markup

app = Flask(__name__)   

app.secret_key = "MxR[18]" 
Bootstrap(app)  
app.config['RECAPTCHA_SITE_KEY'] = '6LcvWiUpAAAAAC6XcX0GSeBHDVEAt67QjvggbkHF'
app.config['RECAPTCHA_SECRET_KEY'] = '6LcvWiUpAAAAADbcpn0LoZTARnPCHFHLSsC98yU1'
recaptcha = ReCaptcha(app)  
#INICIO

@app.route('/', methods=['GET'])    
def index():
    return render_template('/index.html') 

#Agenda
@app.route('/agenda', methods=['GET', 'POST'])    
def agenda():
    sitekey = "6LcvWiUpAAAAAC6XcX0GSeBHDVEAt67QjvggbkHF"
    if request.method == "POST":
        name = request.form['Nombre']
        correo = request.form['Correo']
        mensaje = request.form['Mensaje']
        respuesta_del_captcha = request.form['g-recaptcha-response']
        if comprobar_humano(respuesta_del_captcha):
            #SI
            status = "Exito."
            print (status)
        else:    
            #No 
            status = "Error, pruebe de nuevo."
            print(status)

    return render_template('/agenda.html', sitekey=sitekey)

#Agenda2
@app.route('/agenda2', methods=['GET', 'POST'])    
def agenda2():
    miform = miformulario()
    if miform.validate_on_submit() and recaptcha.verify():
        print(f"Nombre:{miform.nombre.data},Correo:{miform.correo.data},mensaje:{miform.mensaje.data}")
    else: 
        print("Algun dato es invalido")
    
    return render_template("agenda2.html", form=miform)


#Contacto
@app.route('/contacto', methods=['GET'])    
def contacto():

    return render_template('contacto.html')

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

#funcion Recaptcha
def comprobar_humano (respuesta_del_captcha):
    secret = "6LcvWiUpAAAAADbcpn0LoZTARnPCHFHLSsC98yU1"
    payload = {'response': respuesta_del_captcha, 'secret':secret}
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
    response_text = json.loads(response.text)
    return response_text['success'] 


if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = '5001')  



