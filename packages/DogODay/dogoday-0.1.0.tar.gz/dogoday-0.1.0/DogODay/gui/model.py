import requests, json, importlib.resources, os

# Función para cargar el fichero de configurarión donde se encuentra la url base de la API
def load_config():
    try:
        config_path = importlib.resources.files("DogODay.res").joinpath("config.json")
    except:
        current_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(current_path,'..','res','config.json')

    with open(config_path, "r") as config_file:
        config = json.load(config_file)

    return config

class Modelo():
    def __init__(self, sesion: requests.Session):
        self._sesion = sesion
        config = load_config()
        self._base_url = config["base_url"]
        self._id_imagen_actual = None
    
    # A través de la ruta /breeds podemos acceder a una lista de objetos.
    # Cada objjeto en esta lista contiene información de cada raza.
    def buscar_razas(self):
        ruta_razas = '/breeds'
        response = self._sesion.get(self._base_url + ruta_razas)
        razas = response.json()
        return razas
    
    # Buscamos una imagen aleatoria utilizando una ruta que contiene un query '?'.
    # La API ofrece varios formatos, por lo que debemos restringir a .png y .jpeg
    def buscar_imagen_raza(self, id_raza):
        # Parte 1: Buscar una imagen aleatoria para la raza
        ruta_buscar = '/images/search?breed_id={}&mime_types=jpg,png'.format(id_raza)
        response = self._sesion.get(self._base_url + ruta_buscar)

        # Parte 2: Ir a la url donde se encuentra la imagen
        imagen_url = response.json()[0]["url"]
        self._id_imagen_actual = response.json()[0]["id"]
        response_imagen = self._sesion.get(imagen_url)
        imagen_data = response_imagen.content
        if response_imagen.status_code == 200:
            return imagen_data
        else:
            return None
    
    # Utilizar la ruta /breeds/:breed_id para obtener información básica de la raza
    def buscar_descripcion(self, id_raza):
        ruta_dato = '/breeds/{}'.format(id_raza)
        response = self._sesion.get(self._base_url + ruta_dato)
        datos = response.json()
        return json.dumps(datos, indent=4, ensure_ascii=False)
    
    # Utilizar la ruta /votes para postear un voto positivo
    def votar_imagen(self):
        ruta_votar = '/votes'
        payload = {"image_id": self._id_imagen_actual, "value": 1}
        response = self._sesion.post(self._base_url + ruta_votar, json=payload)
        if response.status_code == 201:
            return True
        else:
            return False