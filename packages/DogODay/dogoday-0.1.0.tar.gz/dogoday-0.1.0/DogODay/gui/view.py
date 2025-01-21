from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import ( 
    QApplication,
    QMainWindow, 
    QWidget,
    QLabel,
    QTextEdit,
    QComboBox,
    QPushButton,
    QStatusBar,
    QVBoxLayout,
    QHBoxLayout
    )

from io import BytesIO
from importlib.resources import files
import os, sys

class Vista(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle('DogODay')
        self.setFixedSize(410, 600)

        # Arreglar widgets en la ventana principal
        self._central_widget = QWidget(self)
        self.setCentralWidget(self._central_widget)
        self._general_layout = QVBoxLayout()
        self._central_widget.setLayout(self._general_layout)
        self._agregar_vista_imagen()
        self._agregar_descripcion()
        self._agregar_dropdown()
        self._agregar_botones()

        # Crear una barra  de estabo
        self._barra_status = QStatusBar()
        self.setStatusBar(self._barra_status)
    
    # La imagen es de una medida fija. Para iniciar, se busca un placeholder.
    def _agregar_vista_imagen(self):
        try:
            # Esto encontrará la imagen "placeholder" utilizando importlib
            self._placeholder_path = str(files("DogODay.data").joinpath("placeholder.png"))
        except:
            # Esto encontrará la imagen cuando se está en desarrollo
            current_path = os.path.dirname(os.path.abspath(__file__))
            self._placeholder_path = os.path.join(current_path,'..','res','placeholder.png')
        self._imagen = QLabel()
        self._imagen.setFixedSize(400, 400)
        self._imagen.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.mostrar_imagen()
        self._general_layout.addWidget(self._imagen)
    
    # La descripción de la raza se coloca en un QTextEdit que está protegido contra escritura
    def _agregar_descripcion(self):
        self._display = QTextEdit()
        self._display.setFixedHeight(100)
        self._display.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self._display.setReadOnly(True)
        self._display.setPlaceholderText("... Descripción de la raza ...")
        self._general_layout.addWidget(self._display)

    # El dropdown tendrá en la posición 0 un texto que hace de placeholder
    def _agregar_dropdown(self):
        self.dropdown = QComboBox()
        self.dropdown.addItem("--- Seleccione una raza ---")
        self._general_layout.addWidget(self.dropdown)

    # Botones en un arreglo horizontal interno
    def _agregar_botones(self):
        layout_botones  = QHBoxLayout()
        self.boton_otra = QPushButton("Otra imagen")
        self.boton_votar = QPushButton("Votar imagen")
        layout_botones.addWidget(self.boton_otra)
        layout_botones.addWidget(self.boton_votar)
        self.habilitar_botones(False)
        self._general_layout.addLayout(layout_botones)

    # Método para rellenar el dropdown con el nombre de las razas. El texto será el atributo "name" mientras que la data serán los "id".
    def actualizar_razas(self, razas):
        for raza in razas:
            self.dropdown.addItem(raza["name"], userData=raza["id"])

    # Imprime la imagen que se descarga de la API, o en su defecto, la imagen placeholder.
    def mostrar_imagen(self, content=None):
        if content:
            imagen_data = BytesIO(content)
            imagen = QPixmap()
            imagen.loadFromData(imagen_data.read())
        else:
            imagen = QPixmap(self._placeholder_path)
        imagen = imagen.scaled(300, 300, Qt.AspectRatioMode.KeepAspectRatio)
        self._imagen.setPixmap(imagen)

    # Habilita o deshabilita los botones
    def habilitar_botones(self, enabled=True):
        self.boton_otra.setEnabled(enabled)
        self.boton_votar.setEnabled(enabled)
    
    # Escribe un texto en la descripción
    def escribir_descripcion(self, texto):
        self._display.setText(texto)
    
    # Escribe la información en la barra de estado
    def escribir_status(self, status):
        self._barra_status.showMessage(status)


# Este código sólo está aquí para pruebas en desarrollo
if __name__ == '__main__':
    app = QApplication(sys.argv)
    view = Vista()
    view.show()
    sys.exit(app.exec())