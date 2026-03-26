import tkinter as tk
from tkinter import ttk, messagebox

from api.webservice import get, post, put, delete, patch


class Regimen(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.endpoint = "/regimen"

        self.crear_widgets()
        self.cargar_regimenes()

    # -----------------------------
    # INTERFAZ
    # -----------------------------

    def crear_widgets(self):

        # FRAME FORMULARIO
        frame_form = tk.LabelFrame(self, text="Gestión de Regímenes")
        frame_form.pack(fill="x", padx=10, pady=10)

        btn_crear = tk.Button(frame_form, text="Crear", command=self.crear_regimen)
        btn_crear.grid(row=0, column=2, padx=5)

        btn_actualizar = tk.Button(frame_form, text="Actualizar", command=self.actualizar_regimen)
        btn_actualizar.grid(row=0, column=3, padx=5)

        btn_borrar = tk.Button(frame_form, text="Borrar",command = self.borrar_regimen)
        btn_borrar.grid(row=0, column=4, padx=5)


        btn_refrescar = tk.Button(frame_form, text="Refrescar", command=self.cargar_regimenes)
        btn_refrescar.grid(row=0, column=5, padx=5)

        # -----------------------------
        # TABLA
        # -----------------------------

        columnas = ("tipoRegimen", "precio")

        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")

        self.tabla.heading("tipoRegimen", text="Tipo de Régimen")
        self.tabla.heading("precio", text="Precio")


        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

    # -----------------------------
    # CARGAR DATOS
    # -----------------------------

    def cargar_regimenes(self):

        datos = get(self.endpoint)

        if not datos:
            return

        # limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # recorrer lista de regimenes
        for r in datos["resultRegimen"]:
            self.tabla.insert("", tk.END, values=(r["descripcion"],r["precio"],r["tipoRegimen"]))

    # -----------------------------
    # CREAR
    # -----------------------------

    def crear_regimen(self):
        #--------------------------
        #FORMULARIO CREAR
        #--------------------------
        formulario = tk.Toplevel(self)
        formulario.title("Crear Regimen")
        formulario.geometry("300x180")
        formulario.resizable(False,False)

        #Campo tipoRegimen
        tk.Label(formulario, text="Tipo Regimen").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_tipoRegimen = tk.Entry(formulario)
        entry_tipoRegimen.grid(row=0, column=1, padx=10, pady=10)

        #Campo descripcion
        tk.Label(formulario, text="Descripcion:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_descripcion = tk.Entry(formulario)
        entry_descripcion.grid(row=1, column=1, padx=10, pady=10)

        #Campo precio
        tk.Label(formulario, text="Precio:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        entry_precio = tk.Entry(formulario)
        entry_precio.grid(row=2, column=1, padx=10, pady=10)

        def crear():
            nuevo_tipoRegimen = entry_tipoRegimen.get().strip()
            nueva_descripcion = entry_descripcion.get().strip()
            try:
                nuevo_precio = float(entry_precio.get().strip())
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número.")
                return

            datos = {
            "tipoRegimen": nuevo_tipoRegimen,
            "descripcion": nueva_descripcion,
            "precio": nuevo_precio
            }

            endpoint = f"{self.endpoint}/create/"
            resultado = post(endpoint, datos)
            if resultado:
                messagebox.showinfo("OK", "Régimen creado")
                formulario.destroy()
                self.cargar_regimenes()

        # -----------------------------
        # Botones del formulario
        # -----------------------------
        btn_guardar = tk.Button(formulario, text="Crear", command=crear)
        btn_guardar.grid(row=3, column=0, padx=10, pady=15)

        btn_cancelar = tk.Button(formulario, text="Cancelar", command=formulario.destroy)
        btn_cancelar.grid(row=3, column=1, padx=10, pady=15)

        # hacer modal
        formulario.transient(self)
        formulario.grab_set()
        formulario.focus()

    # -----------------------------
    # ACTUALIZAR
    # -----------------------------

    def actualizar_regimen(self):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un régimen")
            return

        tipoRegimen_actualizar = self.tabla.item(seleccionado)["values"][2]
        descripcion_original = self.tabla.item(seleccionado)["values"][0]
        precio_original = self.tabla.item(seleccionado)["values"][1]

        #--------------------------
        #FORMULARIO ACTUALIZAR
        #--------------------------
        formulario = tk.Toplevel(self)
        formulario.title("Actualizar Regimen")
        formulario.geometry("300x180")
        formulario.resizable(False,False)

        #Campo descripcion
        tk.Label(formulario, text="Descripcion:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        entry_descripcion = tk.Entry(formulario)
        entry_descripcion.grid(row=0, column=1, padx=10, pady=10)
        entry_descripcion.insert(0, descripcion_original)

        #Campo precio
        tk.Label(formulario, text="Precio:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        entry_precio = tk.Entry(formulario)
        entry_precio.grid(row=1, column=1, padx=10, pady=10)
        entry_precio.insert(0, str(precio_original))

        def actualizar():
            nueva_descripcion = entry_descripcion.get().strip()
            try:
                nuevo_precio = float(entry_precio.get().strip())
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número.")
                return

            datos = {
            "descripcion": nueva_descripcion,
            "precio": nuevo_precio
            }

            endpoint = f"{self.endpoint}/update/{tipoRegimen_actualizar}"
            resultado = patch(endpoint, datos)
            if resultado:
                messagebox.showinfo("OK", "Régimen actualizado")
                formulario.destroy()
                self.cargar_regimenes()

        # -----------------------------
        # Botones del formulario
        # -----------------------------
        btn_guardar = tk.Button(formulario, text="Actualizar", command=actualizar)
        btn_guardar.grid(row=3, column=0, padx=10, pady=15)

        btn_cancelar = tk.Button(formulario, text="Cancelar", command=formulario.destroy)
        btn_cancelar.grid(row=3, column=1, padx=10, pady=15)

        # hacer modal
        formulario.transient(self)
        formulario.grab_set()
        formulario.focus()

    # -----------------------------
    # BORRAR
    # -----------------------------

    def borrar_regimen(self):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un régimen")
            return

        regimen_borrar = self.tabla.item(seleccionado)["values"][2]

        endpoint = f"{self.endpoint}/delete/{regimen_borrar}"

        resultado = delete(endpoint)

        if resultado:
            messagebox.showinfo("OK", "Régimen borrado")
            self.cargar_regimenes()









