from flask import Flask

app = Flask(__name__)
app.config.from_object('config.Config')  # Carga config.py

from app import routes  # Importa rutas
