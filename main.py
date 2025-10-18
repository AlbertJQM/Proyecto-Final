"""
Módulo Principal de la Aplicación de Gestión de Imágenes Médicas.

Este módulo contiene la llamada a la clase `AplicacionGUI`, que construye y gestiona la
interfaz gráfica de usuario (GUI) utilizando Tkinter. Actúa como la "Vista"
en una arquitectura Modelo-Vista-Controlador (MVC), interactuando con el
"Controlador" (`GestorImagenes`) para presentar y manipular los datos.

Principios de Diseño Aplicados:
- **Interfaz de Usuario Intuitiva**: Diseñada para ser clara y fácil de usar.
- **Acoplamiento Débil**: La GUI no conoce los detalles de implementación
  del gestor; solo llama a sus métodos públicos.
"""
import tkinter as tk
from models.interfaz_grafica import AplicacionGUI

# --- Punto de Entrada de la Aplicación ---
if __name__ == "__main__":
    # Creamos la ventana principal
    ventana_principal = tk.Tk()
    
    # Creamos una instancia de nuestra clase de aplicación
    app = AplicacionGUI(ventana_principal)
    
    # Iniciamos el bucle principal de la aplicación
    ventana_principal.mainloop()