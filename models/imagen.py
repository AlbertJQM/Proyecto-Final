"""
Módulo de Modelo de Datos para el Proyecto de Glaucoma.

Este módulo define la clase `Imagen`, que representa una única imagen médica
y su metadata asociada. La clase es el pilar fundamental del modelo de datos
de la aplicación.

Principios de Diseño Aplicados:
- **Clean Code**: La clase tiene una única responsabilidad (representar una imagen)
  y sus métodos son cohesivos.
- **PEP 8**: El código sigue las convenciones de estilo de Python.
- **Type Hinting**: Se utilizan anotaciones de tipo para mejorar la claridad y
  permitir la verificación estática de tipos.
"""

# Importamos las librerías necesarias para el manejo de fechas y tipos.
# 'datetime' para trabajar con fechas de adquisición.
# 'Optional' y 'Tuple' para anotaciones de tipo más precisas.
from datetime import date
from typing import Optional, Tuple

class Imagen:
    """
    Representa una imagen médica y su metadata asociada.

    Esta clase actúa como un contenedor de datos estructurado (similar a un 'struct'
    en otros lenguajes) con validación incorporada para asegurar la integridad
    de la información.

    Atributos:
        id_imagen (str): Identificador único para la imagen (ej: 'img_0001').
        ruta_archivo (str): Ruta completa donde la imagen está almacenada.
        id_paciente (str): Identificador del paciente asociado a la imagen.
        fecha_adquisicion (date): Fecha en que la imagen fue tomada.
        diagnostico (str): Diagnóstico médico preliminar.
        conjunto_datos (str): El conjunto al que pertenece ('Train', 'Test', 'Validation').
        coordenadas_fovea (Optional[Tuple[int, int]]): Tupla con las oordenadas (x, y)
                                                       de la fóvea.
        dimensiones (Optional[Tuple[int, int]]): Tupla con (ancho, alto) de la imagen.
                                                 Es opcional en caso de que la imagen
                                                 no se pueda leer.
    """

    def __init__(self,
                 id_imagen: str,
                 ruta_archivo: str,
                 id_paciente: str,
                 fecha_adquisicion: date,
                 diagnostico: str,
                 conjunto_datos: str,
                 coordenadas_fovea: Optional[Tuple[float, float]] = None,
                 dimensiones: Optional[Tuple[int, int]] = None):
        """
        Inicializa una nueva instancia de la clase Imagen.
        """
        # Asignación directa de atributos.
        self.id_imagen = id_imagen
        self.ruta_archivo = ruta_archivo
        self.id_paciente = id_paciente
        self.fecha_adquisicion = fecha_adquisicion
        self.diagnostico = diagnostico
        self.conjunto_datos = conjunto_datos
        self.coordenadas_fovea = coordenadas_fovea
        self.dimensiones = dimensiones

    def validar_metadata(self) -> bool:
        """
        Verifica la consistencia y corrección de la metadata de la instancia.

        Esta es una validación simple. En un proyecto real, podría ser mucho
        más compleja, comprobando formatos de ID, rangos de fechas, etc.

        Returns:
            bool: True si toda la metadata es válida, False en caso contrario.
        """
        # Verificamos que los campos de texto no estén vacíos.
        if not all([self.id_imagen, self.ruta_archivo, self.id_paciente, self.diagnostico]):
            print(f"Error de validación: El ID '{self.id_imagen}' tiene campos de texto vacíos.")
            return False

        # Verificamos que la fecha de adquisición sea un objeto 'date'.
        if not isinstance(self.fecha_adquisicion, date):
            print(f"Error de validación: La fecha para '{self.id_imagen}' no es válida.")
            return False

        # Verificamos que el conjunto de datos sea uno de los valores permitidos.
        conjuntos_validos = ["Train", "Test", "Validation"]
        if self.conjunto_datos not in conjuntos_validos:
            print(f"Error de validación: El conjunto '{self.conjunto_datos}' no es válido.")
            return False

        # Si todas las validaciones pasan, retornamos True.
        return True

    def a_diccionario(self) -> dict:
        """
        Convierte la instancia de la clase en un diccionario.

        Útil para procesos de serialización, como guardar los datos en un CSV
        o un JSON. Convierte la fecha a formato ISO (YYYY-MM-DD) para una
        correcta serialización.
        
        Returns:
            dict: Un diccionario representando los datos de la imagen.
        """
        return {
            "id_imagen": self.id_imagen,
            "ruta_archivo": self.ruta_archivo,
            "id_paciente": self.id_paciente,
            "fecha_adquisicion": self.fecha_adquisicion.isoformat(),
            "diagnostico": self.diagnostico,
            "conjunto_datos": self.conjunto_datos,
            # Convertimos las dimensiones a un string para guardarlo fácil en CSV.
            "Fovea_X": str(self.coordenadas_fovea[0]) if self.coordenadas_fovea else "",
            "Fovea_Y": str(self.coordenadas_fovea[1]) if self.coordenadas_fovea else "",
            "Size_X": str(self.dimensiones[0]) if self.dimensiones else "",
            "Size_Y": str(self.dimensiones[1]) if self.dimensiones else ""
        }


    def __repr__(self) -> str:
        """
        Representación oficial del objeto como string.

        Permite que al hacer `print()` de un objeto Imagen, se muestre
        información útil para depuración.
        """
        return (f"Imagen(id='{self.id_imagen}', paciente='{self.id_paciente}', "
                f"fecha='{self.fecha_adquisicion.isoformat()}')")