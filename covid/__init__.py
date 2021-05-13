from flask import Flask 

app = Flask(__name__)

@app.route('/') # abrimos una ruta
def index(): 
    return 'Flask está funcionando!'