# rutas que tengan que ver con la aplicación covid

from covid import app 

@app.route('/') # abrimos una ruta
def index(): 
    return 'Flask está funcionando desde views!'