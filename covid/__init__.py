from flask import Flask 

app = Flask(__name__)

from covid import views # lo importamos después de crear la app
