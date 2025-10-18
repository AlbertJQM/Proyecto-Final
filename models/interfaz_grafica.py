import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import date
from PIL import Image, ImageTk

# Importamos el "cerebro" de nuestra aplicación.
from models.gestor import GestorImagenes

class AplicacionGUI:
    """
    Clase que encapsula toda la interfaz gráfica de la aplicación.
    """

    def __init__(self, root):
        """
        Inicializa la ventana principal y todos sus componentes (widgets).

        Args:
            root: La ventana raíz de Tkinter (tk.Tk()).
        """
        self.root = root
        self.root.title("Gestor de Imágenes Médicas - Glaucoma")
        self.root.geometry("1200x800")

        # Instanciamos el cerebro de la aplicación.
        self.gestor = GestorImagenes()

        # Variable para almacenar la ruta del archivo seleccionado
        self.ruta_archivo_seleccionado = tk.StringVar()
        
        # Variables para almacenar el ancho y alto del archivo seleccionado
        self.ancho_imagen = tk.IntVar()
        self.alto_imagen = tk.IntVar()

        # Bandera para distinguir entre agregar y editar
        self.es_editar = False
        
        # ID de la imagen que se está modificando (si aplica)
        self.id_a_modificar = None

        # --- Creación de los componentes de la GUI ---
        self._crear_widgets()
        
        # --- Carga inicial de datos ---
        self.refrescar_tabla_imagenes()

    def _crear_widgets(self):
        """Crea y organiza todos los componentes visuales de la aplicación."""

        # --- Frame Principal ---
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- Frame del Formulario (Izquierda) ---
        form_frame = ttk.LabelFrame(main_frame, text="Registro de Imagen", padding="10", width=320)
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10)
        form_frame.pack_propagate(False)

        # -- Widgets del Formulario --
        ttk.Label(form_frame, text="Archivo de Imagen:").pack(anchor="w")
        self.entry_ruta = ttk.Entry(form_frame, textvariable=self.ruta_archivo_seleccionado, state="readonly", width=40)
        self.entry_ruta.pack(fill="x")
        ttk.Button(form_frame, text="Seleccionar Archivo...", command=self._evento_seleccionar_archivo).pack(fill="x", pady=5)

        ttk.Label(form_frame, text="ID Paciente:").pack(anchor="w", pady=(10,0))
        self.entry_paciente = ttk.Entry(form_frame)
        self.entry_paciente.pack(fill="x")

        ttk.Label(form_frame, text="Diagnóstico:").pack(anchor="w", pady=(10,0))
        self.combo_diagnostico = ttk.Combobox(form_frame, values=["No tiene Glaucoma", "Tiene Glaucoma"], state="readonly")
        self.combo_diagnostico.pack(fill="x")
        self.combo_diagnostico.set("No tiene Glaucoma") # Valor por defecto

        ttk.Label(form_frame, text="Conjunto de Datos:").pack(anchor="w", pady=(10,0))
        self.combo_conjunto = ttk.Combobox(form_frame, values=["Train", "Test", "Validation"], state="readonly")
        self.combo_conjunto.pack(fill="x")
        self.combo_conjunto.set("Train") # Valor por defecto

        # Agrupamos las coordenadas en una misma fila usando un frame y grid
        coords_frame = ttk.Frame(form_frame)
        coords_frame.pack(fill="x", pady=(10,0))

        # Colocamos: Label X | Entry X | Label Y | Entry Y en la misma fila
        ttk.Label(coords_frame, text="Coordenada X Fóvea:").grid(row=0, column=0, sticky="w", pady=(10,0), padx=(0,20))
        self.entry_fovea_x = ttk.Entry(coords_frame, width=10)
        self.entry_fovea_x.grid(row=1, column=0, sticky="w")

        ttk.Label(coords_frame, text="Coordenada Y Fóvea:").grid(row=0, column=1, sticky="w", pady=(10,0))
        self.entry_fovea_y = ttk.Entry(coords_frame, width=10)
        self.entry_fovea_y.grid(row=1, column=1, sticky="w")

        ttk.Label(coords_frame, text="Ancho Imagen (px):").grid(row=2, column=0, sticky="w", pady=(10,0))
        self.entry_ancho_imagen = ttk.Entry(coords_frame, textvariable=self.ancho_imagen, state="readonly", width=10)
        self.entry_ancho_imagen.grid(row=3, column=0, sticky="w")
        
        ttk.Label(coords_frame, text="Alto Imagen (px):").grid(row=2, column=1, sticky="w", pady=(10,0))
        self.entry_alto_imagen = ttk.Entry(coords_frame, textvariable=self.alto_imagen, state="readonly", width=10)
        self.entry_alto_imagen.grid(row=3, column=1, sticky="w")

        # Botón para guardar
        ttk.Button(form_frame, text="Guardar Imagen", command=self._evento_guardar_nueva_imagen).pack(fill="x", pady=10)
        

        # -- Previsualización de la Imagen --
        self.label_preview = ttk.Label(form_frame, text="Previsualización", relief="solid", anchor="center")
        self.label_preview.pack(fill="both", expand=True, pady=10)


        # --- Frame de la Tabla (Derecha) ---
        tabla_frame = ttk.LabelFrame(main_frame, text="Imágenes Registradas", padding="10")
        tabla_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # -- Tabla (TreeView) --
        columnas = ("id_imagen", "id_paciente", "diagnostico", "fecha_adquisicion", "conjunto_datos", "coordenadas_fovea", "dimensiones", "ruta_archivo")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings")
        
        # Definir cabeceras
        self.tree.heading("id_imagen", text="ID Imagen")
        self.tree.heading("id_paciente", text="ID Paciente")
        self.tree.heading("diagnostico", text="Diagnóstico")
        self.tree.heading("fecha_adquisicion", text="Fecha")
        self.tree.heading("conjunto_datos", text="Conjunto")
        self.tree.heading("coordenadas_fovea", text="Fóvea (X,Y)")
        self.tree.heading("dimensiones", text="Dimensiones")
        self.tree.heading("ruta_archivo", text="Ruta Archivo")

        # Ajustar tamaño de columnas
        self.tree.column("id_imagen", width=80)
        self.tree.column("id_paciente", width=80)
        self.tree.column("diagnostico", width=100)
        self.tree.column("fecha_adquisicion", width=100)
        self.tree.column("conjunto_datos", width=80)
        self.tree.column("coordenadas_fovea", width=100)
        self.tree.column("dimensiones", width=100)
        self.tree.column("ruta_archivo", width=250)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Cargar datos en el formulario al hacer click (selección) en la tabla
        self.tree.bind("<<TreeviewSelect>>", self._cargar_registro_seleccionado)

        # Frame para colocar los botones en la misma fila
        botones_frame = ttk.Frame(tabla_frame)
        botones_frame.pack(fill="x", pady=5)
        center_frame = ttk.Frame(botones_frame)
        center_frame.pack(anchor="center")
        
        # Botón para modificar
        ttk.Button(center_frame, text="Modificar Selección", command=self._evento_modificar_seleccion).pack(side=tk.LEFT, padx=5)

        # Botón para eliminar
        ttk.Button(center_frame, text="Eliminar Selección", command=self._evento_eliminar_seleccion).pack(side=tk.LEFT, padx=5)

    def refrescar_tabla_imagenes(self):
        """Limpia y vuelve a cargar todos los datos en la tabla (TreeView)."""
        # Borrar todos los items existentes
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Obtener la lista actualizada de objetos Imagen
        imagenes = self.gestor.obtener_imagenes_como_objetos()
        
        # Insertar cada imagen en la tabla
        for img in imagenes:
            self.tree.insert("", tk.END, values=(
                img.id_imagen,
                str(img.id_paciente),
                img.diagnostico,
                img.fecha_adquisicion.isoformat(),
                img.conjunto_datos,
                f"({img.coordenadas_fovea[0]}, {img.coordenadas_fovea[1]})" if img.coordenadas_fovea else "N/A",
                f"({img.dimensiones[0]}x{img.dimensiones[1]})" if img.dimensiones else "N/A",
                img.ruta_archivo
            ))

    def _evento_seleccionar_archivo(self):
        """Abre un diálogo para seleccionar un archivo y muestra la previsualización."""
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Archivos de Imagen", "*.png *.jpg *.jpeg *.bmp *.gif"), ("Todos los archivos", "*.*")]
        )
        if ruta:
            self.ruta_archivo_seleccionado.set(ruta)
            self._mostrar_preview(ruta)

    def _mostrar_preview(self, ruta_imagen):
        """
        Carga y muestra una imagen en el widget de previsualización.
        
        Args:
            ruta_imagen (str): La ruta del archivo de imagen a mostrar.
        """
        try:
            img = Image.open(ruta_imagen)
            # Obtenemos y guardamos las dimensiones de la imagen original
            self.ancho_imagen.set(img.width)
            self.alto_imagen.set(img.height)
            img.thumbnail((250, 250)) # Redimensiona para que quepa en la GUI
            self.photo_preview = ImageTk.PhotoImage(img)
            self.label_preview.config(image=self.photo_preview)
        except Exception as e:
            self.label_preview.config(image=None, text=f"Error al cargar\nla imagen:\n{e}")

    def _evento_guardar_nueva_imagen(self):
        """Recoge los datos del formulario y le pide al gestor que registre la imagen."""
        # 1. Recoger datos de los campos de entrada
        ruta = self.ruta_archivo_seleccionado.get()
        paciente_id = self.entry_paciente.get()
        diagnostico = self.combo_diagnostico.get()
        conjunto = self.combo_conjunto.get()
        coordenadas_fovea = (self.entry_fovea_x.get(), self.entry_fovea_y.get())
        dimensiones = (self.ancho_imagen.get(), self.alto_imagen.get())
        
        # 2. Validar que los campos no estén vacíos
        if not all([ruta, paciente_id, diagnostico, conjunto, coordenadas_fovea[0], coordenadas_fovea[1]]):
            messagebox.showwarning("Campos Incompletos", "Por favor, complete todos los campos antes de guardar.")
            return

        # 3. Crear el diccionario de metadata
        metadata = {
            "id_paciente": paciente_id,
            "diagnostico": diagnostico,
            "conjunto_datos": conjunto,
            "fecha_adquisicion": date.today(), # Usamos la fecha actual
            "coordenadas_fovea": (float(coordenadas_fovea[0]), float(coordenadas_fovea[1])) if all(coordenadas_fovea) else None,
            "dimensiones": dimensiones
        }

        if self.es_editar:
            # Modo edición: actualizar la imagen existente
            metadata["ruta_archivo"] = ruta
            exito = self.gestor.modificar_metadata_imagen(self.id_a_modificar, metadata)
            if exito:
                messagebox.showinfo("Éxito", "La metadata de la imagen ha sido modificada correctamente.")
                self.refrescar_tabla_imagenes()
                self._limpiar_formulario()
                self.es_editar = False
                self.id_a_modificar = None
            else:
                messagebox.showerror("Error", "No se pudo modificar la metadata. Revise la consola para más detalles.")
            return

        # 4. Llamar al gestor para que haga el trabajo
        exito = self.gestor.registrar_nueva_imagen(ruta, metadata)
        
        # 5. Actualizar la GUI
        if exito:
            messagebox.showinfo("Éxito", "La imagen ha sido registrada correctamente.")
            self.refrescar_tabla_imagenes()
            self._limpiar_formulario()
        else:
            messagebox.showerror("Error", "No se pudo registrar la imagen. Revise la consola para más detalles.")

    def _evento_eliminar_seleccion(self):
        """Obtiene la selección de la tabla y le pide al gestor que la elimine."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione una imagen de la tabla para eliminar.")
            return

        # Pedimos confirmación al usuario
        confirmar = messagebox.askyesno("Confirmar Eliminación", "¿Está seguro de que desea eliminar la imagen seleccionada?")
        if not confirmar:
            return

        # Obtenemos el ID de la imagen de la fila seleccionada
        item_seleccionado = self.tree.item(seleccion[0])
        id_a_eliminar = item_seleccionado['values'][0]
        
        # Llamamos al gestor
        self.gestor.eliminar_imagen_por_id(id_a_eliminar)
        
        # Actualizamos la GUI
        messagebox.showinfo("Éxito", f"Imagen '{id_a_eliminar}' eliminada.")
        self.refrescar_tabla_imagenes()

    def _evento_modificar_seleccion(self):
        """Obtiene la selección de la tabla y le pide al gestor que modifique su metadata."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Sin Selección", "Por favor, seleccione una imagen de la tabla para modificar.")
            return

        # Obtenemos el ID de la imagen de la fila seleccionada
        item_seleccionado = self.tree.item(seleccion[0])
        self.id_a_modificar = item_seleccionado['values'][0]

        # Indicamos que estamos en modo edición
        self.es_editar = True
        self._evento_guardar_nueva_imagen()

    def _limpiar_formulario(self):
        """Limpia todos los campos de entrada del formulario."""
        self.ruta_archivo_seleccionado.set("")
        self.entry_paciente.delete(0, tk.END)
        self.combo_diagnostico.set("No tiene Glaucoma")
        self.combo_conjunto.set("Train")
        self.entry_fovea_x.delete(0, tk.END)
        self.entry_fovea_y.delete(0, tk.END)
        self.ancho_imagen.set(0)
        self.alto_imagen.set(0)
        self.label_preview.config(image=None, text="Previsualización")

    def _cargar_registro_seleccionado(self, event):
        """Carga los valores de la fila seleccionada en los campos del formulario (sin entrar en modo edición)."""
        seleccion = self.tree.selection()
        if not seleccion:
            return
        try:
            item = self.tree.item(seleccion[0])
            vals = item.get("values", [])
            if not vals:
                return

            # Rellenar campos del formulario (no activar es_editar ni id_a_modificar)
            self._limpiar_formulario()
            self.ruta_archivo_seleccionado.set(vals[7])
            self.entry_paciente.insert(0, str(vals[1]))
            self.combo_diagnostico.set(vals[2])
            self.combo_conjunto.set(vals[4])

            coordenadas_fovea = vals[5]
            if coordenadas_fovea and coordenadas_fovea != "N/A":
                coords = coordenadas_fovea.strip("()").split(",")
                # limpiar espacios
                coords = [c.strip() for c in coords]
                if len(coords) >= 2:
                    self.entry_fovea_x.insert(0, coords[0])
                    self.entry_fovea_y.insert(0, coords[1])

            dimension = vals[6]
            if dimension and dimension != "N/A":
                dims = dimension.strip("()").split("x")
                if len(dims) == 2:
                    try:
                        self.ancho_imagen.set(int(dims[0]))
                        self.alto_imagen.set(int(dims[1]))
                    except ValueError:
                        self.ancho_imagen.set(0)
                        self.alto_imagen.set(0)
            else:
                self.ancho_imagen.set(0)
                self.alto_imagen.set(0)

            # Mostrar preview si existe ruta
            ruta = self.ruta_archivo_seleccionado.get()
            if ruta:
                self._mostrar_preview(ruta)
        except Exception as e:
            print(f"Error cargando selección en formulario: {e}")