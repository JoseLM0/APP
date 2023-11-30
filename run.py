from flask import Flask, render_template, request              

app = Flask(__name__)    

@app.route('/', methods={'GET', 'POST'})    
def index():
    if request.method == 'POST':
        nombre = request.form['Nombre'] 
        return render_template('/index.html', nombre = nombre)
    else: 
        return render_template('/index.html') 

@app.route('/agenda', methods=['GET'])    
def agenda():
    return render_template('agenda.html')

@app.route('/contacto', methods=['GET'])    
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = '5001')  
     
