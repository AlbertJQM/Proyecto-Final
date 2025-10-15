"""
Módulo de Utilidades para el Proyecto de Glaucoma.

Proporciona funciones auxiliares (helpers) para tareas comunes como la
manipulación del sistema de archivos y la gestión de archivos CSV.
Esto permite que la lógica de negocio principal (en gestor.py) sea más
limpia y legible.

Principios de Diseño Aplicados:
- **Separación de Responsabilidades (SoC)**: Abstrae las operaciones de
    entrada/salida (I/O) de la lógica de la aplicación.
- **Don't Repeat Yourself (DRY)**: Centraliza funciones que podrían ser
    necesarias en múltiples partes del código.
"""

import csv
import os
import shutil
from pathlib import Path
from typing import List, Dict
import config

def gestionar_rutas(ruta_base: Path, subcarpetas: List[Path]):
    """
    Crea un directorio base y una lista de subdirectorios si no existen.

    Args:
        ruta_base (Path): El directorio principal a crear.
        subcarpetas (List[Path]): Una lista de rutas de subdirectorios
                                  a crear dentro del directorio base.
    """
    try:
        # Crea el directorio base y todos los padres necesarios.
        # 'exist_ok=True' evita un error si el directorio ya existe.
        ruta_base.mkdir(parents=True, exist_ok=True)

        # Itera sobre la lista de subcarpetas y las crea.
        for carpeta in subcarpetas:
            print(carpeta)
            carpeta.mkdir(exist_ok=True, parents=True)
        print(f"Estructura de directorios verificada/creada en: {ruta_base}")

    except OSError as e:
        # Captura errores relacionados con el sistema de archivos.
        print(f"Error al crear la estructura de directorios: {e}")


def escribir_csv(ruta_archivo: Path, datos: List[Dict], cabeceras: List[str]):
    """
    Escribe (o sobreescribe) una lista de diccionarios en un archivo CSV.

    Utiliza DictWriter para un manejo robusto de los datos basado en las
    cabeceras.

    Args:
        ruta_archivo (Path): La ruta completa del archivo CSV a escribir.
        datos (List[Dict]): La lista de diccionarios que se escribirá.
        cabeceras (List[str]): La lista de nombres de las columnas.
    """
    try:
        with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as archivo_csv:
            writer = csv.DictWriter(archivo_csv, fieldnames=cabeceras)
            
            # Escribe la fila de cabeceras.
            writer.writeheader()
            
            # Escribe todas las filas de datos.
            writer.writerows(datos)

    except IOError as e:
        print(f"Error al escribir en el archivo CSV '{ruta_archivo}': {e}")


def leer_csv(ruta_archivo: Path) -> List[Dict]:
    """
    Lee los datos de un archivo CSV y los devuelve como una lista de diccionarios.

    Si el archivo no existe, devuelve una lista vacía sin generar un error.

    Args:
        ruta_archivo (Path): La ruta del archivo CSV a leer.

    Returns:
        List[Dict]: Una lista de diccionarios, donde cada diccionario
                    representa una fila del CSV.
    """
    if not ruta_archivo.exists():
        return []

    try:
        with open(ruta_archivo, mode='r', newline='', encoding='utf-8') as archivo_csv:
            # DictReader convierte cada fila en un diccionario.
            reader = csv.DictReader(archivo_csv)
            return list(reader)
    except IOError as e:
        print(f"Error al leer el archivo CSV '{ruta_archivo}': {e}")
        return []

def copiar_archivo(ruta_origen: Path, ruta_destino: Path):
    """
    Copia un archivo desde una ruta de origen a una de destino.

    Args:
        ruta_origen (Path): Ruta del archivo a copiar.
        ruta_destino (Path): Ruta donde se guardará la copia.
    """

    try:
        shutil.copy(ruta_origen, ruta_destino)
        print(f"Archivo copiado de '{ruta_origen}' a '{ruta_destino}'")
    except IOError as e:
        print(f"Error al copiar el archivo: {e}")