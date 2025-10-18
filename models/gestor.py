"""
Módulo de Lógica de Negocio para el Proyecto de Glaucoma.

Define la clase `GestorImagenes`, que actúa como el "cerebro" o controlador
de la aplicación. Orquesta las interacciones entre el modelo de datos (Imagen),
las utilidades del sistema de archivos (utils) y la configuración (config).

Principios de Diseño Aplicados:
- **Fachada (Facade Pattern)**: Proporciona una interfaz simplificada a un
    subsistema complejo (manejo de archivos, CSV, etc.). La GUI solo interactuará
    con esta clase.
- **Cohesión Alta**: Todos los métodos están relacionados con la gestión de
    imágenes.
- **Bajo Acoplamiento**: Depende de abstracciones (config, utils) en lugar de
    implementaciones concretas, lo que facilita los cambios.
"""

import uuid
from datetime import date, datetime
from pathlib import Path
from typing import Dict, List, Optional

import config
import utils
from models.imagen import Imagen

class GestorImagenes:
    """
    Clase central que gestiona todas las operaciones sobre las imágenes.
    """

    def __init__(self):
        """
        Inicializa el gestor.
        
        Al crearse, automáticamente se asegura de que la estructura de carpetas
        exista y carga cualquier metadata previamente guardada del archivo CSV.
        """
        self.__lista_imagenes: List[Imagen] = []
        self.inicializar_entorno()
        self.cargar_metadata_existente()

    def inicializar_entorno(self):
        """
        Asegura que la estructura de directorios y el archivo CSV existan.
        
        Utiliza las funciones de `utils` y las constantes de `config`.
        """
        print("Inicializando entorno del proyecto...")
        
        # Preparamos la lista de subcarpetas del dataset que deben existir.
        subcarpetas_dataset = [config.RUTA_DATASET / sub for sub in config.CARPETAS_DATASET]
        
        # Delegamos la creación de carpetas a nuestra función de utilidad.
        utils.gestionar_rutas(config.RUTA_DATA, subcarpetas_dataset)

        # Si el archivo metadata.csv no existe, lo crea con las cabeceras.
        if not config.RUTA_METADATA_CSV.exists():
            print(f"Creando archivo de metadatos en: {config.RUTA_METADATA_CSV}")
            # Escribimos un archivo vacío con solo las cabeceras.
            utils.escribir_csv(config.RUTA_METADATA_CSV, [], config.CABECERAS_CSV)

    def cargar_metadata_existente(self):
        """
        Lee el archivo CSV y carga los datos en la memoria de la aplicación.
        
        Convierte cada fila del CSV en un objeto `Imagen` y lo almacena en la
        lista interna `__lista_imagenes`.
        """
        print("Cargando metadatos existentes...")
        datos_csv = utils.leer_csv(config.RUTA_METADATA_CSV)
        
        for fila in datos_csv:
            # Convertimos los datos del CSV (que son strings) a los tipos correctos.
            fecha_obj = datetime.strptime(fila["fecha_adquisicion"], "%Y-%m-%d").date()
            
            # Creamos la instancia de Imagen.
            imagen_obj = Imagen(
                id_imagen=fila["id_imagen"],
                ruta_archivo=fila["ruta_archivo"],
                id_paciente=fila["id_paciente"],
                fecha_adquisicion=fecha_obj,
                diagnostico=fila["diagnostico"],
                conjunto_datos=fila["conjunto_datos"],
                coordenadas_fovea=(float(fila["Fovea_X"]), float(fila["Fovea_Y"])) if fila["Fovea_X"] and fila["Fovea_Y"] else None,
                dimensiones=(int(fila["Size_X"]), int(fila["Size_Y"])) if fila["Size_X"] and fila["Size_Y"] else None
            )
            self.__lista_imagenes.append(imagen_obj)
        
        print(f"Se han cargado {len(self.__lista_imagenes)} registros.")

    def registrar_nueva_imagen(self, ruta_origen_str: str, metadata: Dict) -> bool:
        """
        Registra una nueva imagen en el sistema.

        Esto implica: copiar el archivo, generar un ID, crear un objeto Imagen
        y guardar la nueva metadata en el CSV.

        Args:
            ruta_origen_str (str): La ruta del archivo de imagen a registrar.
            metadata (Dict): Un diccionario con la metadata (id_paciente, etc.).

        Returns:
            bool: True si el registro fue exitoso, False en caso contrario.
        """
        ruta_origen = Path(ruta_origen_str)
        if not ruta_origen.exists():
            print(f"Error: El archivo de origen no existe: {ruta_origen}")
            return False

        # 1. Preparar datos y generar ID
        nuevo_id = self.__generar_id_unico()
        conjunto = metadata.get("conjunto_datos", "Train") # 'Train' por defecto
        
        # 2. Definir ruta de destino y copiar el archivo
        ruta_destino = config.RUTA_DATASET / conjunto / ruta_origen.name
        utils.copiar_archivo(ruta_origen, ruta_destino)
        
        # 3. Crear el objeto Imagen
        nueva_imagen = Imagen(
            id_imagen=nuevo_id,
            ruta_archivo=str(ruta_destino),
            id_paciente=metadata["id_paciente"],
            fecha_adquisicion=metadata["fecha_adquisicion"],
            diagnostico=metadata["diagnostico"],
            conjunto_datos=conjunto,
            coordenadas_fovea=metadata.get("coordenadas_fovea"), # Opcional
            dimensiones=metadata.get("dimensiones") # Opcional
        )

        # 4. Validar y guardar
        if nueva_imagen.validar_metadata():
            self.__lista_imagenes.append(nueva_imagen)
            self.__guardar_metadata_en_csv()
            print(f"Imagen '{nuevo_id}' registrada exitosamente.")
            return True
        else:
            # En un caso real, aquí se debería borrar el archivo copiado.
            print(f"No se pudo registrar la imagen '{nuevo_id}' por metadatos inválidos.")
            return False

    def modificar_metadata_imagen(self, id_imagen: str, nuevos_datos: Dict):
        """
        Modifica la metadata de una imagen existente.

        Args:
            id_imagen (str): El ID de la imagen a modificar.
            nuevos_datos (Dict): Diccionario con los campos y valores a actualizar.
        """
        ruta_origen = Path(nuevos_datos.get("ruta_archivo", ""))
        if not ruta_origen.exists():
            print(f"Error: El archivo de origen no existe: {ruta_origen}")
            return False

        ruta_destino = config.RUTA_DATASET / nuevos_datos.get("conjunto_datos", "Train") / ruta_origen.name
        if ruta_origen.resolve() != ruta_destino.resolve(): # Solo copiar si son diferentes
            utils.copiar_archivo(ruta_origen, ruta_destino)
            utils.verificar_duplicados_dataset(ruta_origen, ruta_destino)
            nuevos_datos["ruta_archivo"] = str(ruta_destino)
        
        imagen = self.__buscar_imagen_por_id(id_imagen)
        if not imagen:
            print(f"Error: No se encontró la imagen con ID '{id_imagen}'.")
            return

        if Path(imagen.ruta_archivo).exists() and Path(imagen.ruta_archivo).resolve() != ruta_destino.resolve():
            utils.verificar_duplicados_dataset(Path(imagen.ruta_archivo), ruta_destino)

        # Actualiza los atributos del objeto con los nuevos datos.
        for campo, valor in nuevos_datos.items():
            if hasattr(imagen, campo):
                setattr(imagen, campo, valor)
        
        self.__guardar_metadata_en_csv()
        print(f"Metadata de la imagen '{id_imagen}' actualizada.")
        return True

    def eliminar_imagen_por_id(self, id_imagen: str):
        """
        Elimina una imagen del sistema (archivo y registro en CSV).

        Args:
            id_imagen (str): El ID de la imagen a eliminar.
        """
        imagen = self.__buscar_imagen_por_id(id_imagen)
        if not imagen:
            print(f"Error: No se encontró la imagen con ID '{id_imagen}'.")
            return

        # 1. Eliminar el archivo físico
        try:
            Path(imagen.ruta_archivo).unlink()
        except OSError as e:
            print(f"Error al eliminar el archivo físico '{imagen.ruta_archivo}': {e}")
            # Se podría decidir si continuar o no, por ahora continuamos.

        # 2. Eliminar de la lista en memoria
        self.__lista_imagenes.remove(imagen)
        
        # 3. Reescribir el CSV sin el registro eliminado
        self.__guardar_metadata_en_csv()
        print(f"Imagen '{id_imagen}' eliminada exitosamente.")

    def obtener_imagenes_como_objetos(self) -> List[Imagen]:
        """Retorna una copia de la lista de objetos Imagen."""
        return self.__lista_imagenes.copy()

    # --- Métodos Privados (Helpers) ---

    def __guardar_metadata_en_csv(self):
        """
        Convierte la lista de objetos Imagen a una lista de diccionarios y la
        escribe en el archivo CSV, sobreescribiendo el contenido anterior.
        """
        datos_para_csv = [img.a_diccionario() for img in self.__lista_imagenes]
        utils.escribir_csv(config.RUTA_METADATA_CSV, datos_para_csv, config.CABECERAS_CSV)

    def __buscar_imagen_por_id(self, id_imagen: str) -> Optional[Imagen]:
        """Busca y retorna un objeto Imagen por su ID."""
        for imagen in self.__lista_imagenes:
            if imagen.id_imagen == id_imagen:
                return imagen
        return None

    def __generar_id_unico(self) -> str:
        """Genera un ID único y corto para una nueva imagen."""
        # uuid4() genera un ID largo y aleatorio. Tomamos solo los primeros 8 caracteres.
        return f"img_{uuid.uuid4().hex[:8]}"