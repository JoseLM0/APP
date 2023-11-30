from flask import Flask, render_template           

app = Flask(__name__)    

@app.route('/', methods={'GET'})    
def index():
    return render_template('/index.html') 

@app.route('/agenda', methods=['GET'])    
def agenda():
    return render_template('agenda.html')

@app.route('/contacto', methods=['GET'])    
def contacto():
    return render_template('contacto.html')

if __name__ == '__main__':
    app.run(debug=True, host = '127.0.0.1', port = '5001')  
     
