from .view import Vista
from .model import Modelo

class Controlador():
    def __init__(self, vista: Vista, modelo: Modelo):
        self._vista = vista
        self._modelo = modelo
        self._cargar_razas()
        self._vista.escribir_status("Listo para comenzar a buscar")

        self._conectar_signals_slots()

    # Indica al modelo que debe buscar las razas con la API y luego indica rellenar las opciones del dropdown en la vista
    def _cargar_razas(self):
        razas = self._modelo.buscar_razas()
        self._vista.actualizar_razas(razas)

    # Conecta las tres señales con dos slots
    def _conectar_signals_slots(self):
        # Señal 1: Se ha seleccionado un nuevo elemento en el dropdown
        # Conectar a slot 1
        self._vista.dropdown.currentIndexChanged.connect(self._buscar_nueva_imagen)

        # Señal 2: Se ha hecho click en el botón de buscar otra imagen
        # Conectar a slot 1
        self._vista.boton_otra.clicked.connect(self._buscar_nueva_imagen)

        # Señal 3: Se ha hecho click en el otón de votar por una imagen
        # Conectar a slot 2
        self._vista.boton_votar.clicked.connect(self._votar_imagen)
    
    # Slot 1: Buscar una nueva imagen
    def _buscar_nueva_imagen(self):
        self._vista.escribir_status("Buscando...")
        id_raza = self._vista.dropdown.currentData()
        raza = self._vista.dropdown.currentText()
        data_imagen = self._modelo.buscar_imagen_raza(id_raza)
        if data_imagen:
            # Si la búsqueda fue exitosa actualizar imagen y descripción en la vista
            self._vista.mostrar_imagen(data_imagen)
            descripcion = self._modelo.buscar_descripcion(id_raza)
            self._vista.escribir_descripcion(descripcion)
            self._vista.escribir_status("Se ha encontrado una imagen aleatoria para la raza {}".format(raza))
            self._vista.habilitar_botones()
        else:
            # Si hubo un error, mostrar placeholder, indicar error en arra de estado
            self._vista.mostrar_imagen()
            self._vista.escribir_descripcion(" ... ")
            self._vista.escribir_status("Error buscando imagenn para la raza {}".format(raza))
            self._vista.habilitar_botones(False)
    
    # Slot 2: Votar por una imagen
    def _votar_imagen(self):
        if self._modelo.votar_imagen():
            self._vista.escribir_status("El voto por la imagen mostrada ha sido exitoso")
        else:
            self._vista.escribir_status("ALERTA: Ha ocurrido un error. Voto no registrado")

