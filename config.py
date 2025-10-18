"""
Módulo de Configuración para el Proyecto de Glaucoma.

Centraliza todas las constantes, rutas y parámetros del proyecto para facilitar
el mantenimiento y la configuración. Modificar una ruta o un nombre de archivo
solo requiere un cambio en este lugar.

Principios de Diseño Aplicados:
- **Clean Code**: Evita "valores mágicos" (magic values) hardcodeados en la
  lógica de la aplicación.
- **Mantenibilidad**: Facilita la adaptación del proyecto a diferentes entornos
  o la modificación de su estructura.
"""

# Importamos 'pathlib' para un manejo de rutas moderno y compatible
# entre sistemas operativos (Windows, macOS, Linux).
from pathlib import Path

# --- Rutas Principales del Proyecto ---

# Path.cwd() obtiene el directorio de trabajo actual donde se ejecuta el script.
# Esto hace que el proyecto sea portable.
RUTA_BASE_PROYECTO = Path.cwd()

# Definimos las subcarpetas principales usando el operador '/', que pathlib
# sobrecarga para unir rutas de forma segura.
RUTA_DATA = RUTA_BASE_PROYECTO / "metadata"
RUTA_DATASET = RUTA_BASE_PROYECTO / "images" / "dataset"

# --- Configuración del Dataset ---

# Lista de las carpetas que deben existir dentro del directorio 'dataset'.
# Esto nos permitirá crear la estructura de forma programática.
CARPETAS_DATASET = ["Train", "Test", "Validation"]

# --- Configuración de Metadatos ---

# Nombre del archivo que almacenará la metadata.
NOMBRE_METADATA_CSV = "metadata.csv"

# Ruta completa y nombre del archivo CSV.
RUTA_METADATA_CSV = RUTA_DATA / NOMBRE_METADATA_CSV

# Cabeceras que tendrá nuestro archivo CSV. Es crucial definirlas aquí
# para asegurar consistencia al leer y escribir el archivo.
CABECERAS_CSV = [
    "id_imagen",
    "ruta_archivo",
    "id_paciente",
    "fecha_adquisicion",
    "diagnostico",
    "conjunto_datos",
    "Fovea_X",
    "Fovea_Y",
    "Size_X",
    "Size_Y"
]