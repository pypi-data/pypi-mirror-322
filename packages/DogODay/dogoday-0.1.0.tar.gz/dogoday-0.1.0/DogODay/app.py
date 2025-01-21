from PyQt6.QtWidgets import  QApplication
import requests
import os, sys

from .auth import DogAPIAuth
from .gui.controller import Modelo, Vista, Controlador

def main():
    app = QApplication(sys.argv)

    # Configurar la sesión con la que me comunicaré con la API
    autenticacion = DogAPIAuth(os.environ.get("DOGAPI_KEY"))
    sesion = requests.Session()
    sesion.auth = autenticacion

    # Declarar mis elementos de Modelo-Vista-Controlador
    vista = Vista()
    modelo = Modelo(sesion)

    controlador = Controlador(vista, modelo)

    vista.show()

    sys.exit(app.exec())