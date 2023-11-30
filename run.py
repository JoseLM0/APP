from flask import Flask       

app = Flask(__name__)    

@app.route('/', methods={'GET'})    
def holamundo():
    return 'Hola Mundocl' 

@app.route('/mis_proyectos', methods=['GET'])    
def mostrarproyectos():
    return 'Aqui se muestran los proyectos'

if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = '5001')  
     
