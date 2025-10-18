# Proyecto Final - Gestión de Imágenes Médicas para Detección de Glaucoma
### Módulo 1 - Fundamentos de la Ingeniería del Software para Científicos de Datos

Integrantes:
1. Luis Fernando Fernandez Quispe
2. Jhonn Hinojosa
3. Albert Jhonatan Quisbert Mújica
4. Franco Villalta

Este proyecto es una aplicación de escritorio desarrollada en Python que permite la gestión, visualización y análisis de imágenes médicas orientadas a la detección de glaucoma. Utiliza una arquitectura Modelo-Vista-Controlador (MVC) y una interfaz gráfica intuitiva basada en Tkinter.

## Estructura del Proyecto

- **main.py**: Punto de entrada de la aplicación. Inicializa la interfaz gráfica.
- **models/**: Contiene los módulos relacionados con la lógica de negocio y la gestión de imágenes (ver Diagrama de Clases).
- **utils.py**: Funciones auxiliares para el procesamiento y manejo de datos.
- **config.py**: Configuración global del proyecto.
- **images/**: Carpeta con el dataset de imágenes médicas, organizado en subcarpetas para entrenamiento, validación y prueba.
- **metadata/**: Incluye el archivo `metadata.csv` con información adicional sobre las imágenes.
- **env/**: Entorno virtual de Python con las dependencias necesarias (por ejemplo, Pillow para manejo de imágenes).

## Diagrama de Clases del Proyecto

Enlace del diagrama: https://i.ibb.co/pvRw6JdV/Diagrama-de-clases.png
<center>
<img src='https://i.ibb.co/pvRw6JdV/Diagrama-de-clases.png' width='50%'>
</center>

## Instalación

1. Clona el repositorio y accede a la carpeta del proyecto.
2. Crea y activa un entorno virtual:
   ```sh
   python -m venv env
   source env/Scripts/activate  # En Windows
   ```
3. Instala las dependencias:
   ```sh
   pip install -r requirements.txt
   ```
   *(Asegúrate de que el archivo `requirements.txt` incluya Pillow y cualquier otra dependencia necesaria.)*

## Uso

Ejecuta la aplicación desde la terminal:
```sh
python main.py
```
La interfaz gráfica te permitirá cargar imágenes, visualizar resultados y gestionar el dataset.

## Licencia

Este proyecto se distribuye bajo la licencia MIT.