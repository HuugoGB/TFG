import tkinter as tk
from tkinter import ttk, messagebox

from api.webservice import get, post, put, delete


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

        tk.Label(frame_form, text="Tipo de régimen").grid(row=0, column=0, padx=5, pady=5)

        self.entry_regimen = tk.Entry(frame_form)
        self.entry_regimen.grid(row=0, column=1, padx=5, pady=5)

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

        columnas = ("tipoRegimen",)

        self.tabla = ttk.Treeview(self, columns=columnas, show="headings")

        self.tabla.heading("tipoRegimen", text="Tipo de Régimen")

        self.tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_regimen)

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
            self.tabla.insert("", tk.END, values=(r["tipoRegimen"], r["precio"]))

    # -----------------------------
    # CREAR
    # -----------------------------

    def crear_regimen(self):

        tipo = self.entry_regimen.get()

        if not tipo:
            messagebox.showwarning("Aviso", "Introduce un régimen")
            return

        datos = {"tipoRegimen": tipo}

        resultado = post(self.endpoint, datos)

        if resultado:
            messagebox.showinfo("OK", "Régimen creado")
            self.cargar_regimenes()
            self.entry_regimen.delete(0, tk.END)

    # -----------------------------
    # SELECCIONAR
    # -----------------------------

    def seleccionar_regimen(self, event):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        valores = self.tabla.item(seleccionado)["values"]

        self.entry_regimen.delete(0, tk.END)
        self.entry_regimen.insert(0, valores[0])

    # -----------------------------
    # ACTUALIZAR
    # -----------------------------

    def actualizar_regimen(self):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un régimen")
            return

        regimen_original = self.tabla.item(seleccionado)["values"][0]
        nuevo_regimen = self.entry_regimen.get()

        datos = {"tipoRegimen": nuevo_regimen}

        resultado = put(f"{self.endpoint}/{regimen_original}", datos)

        if resultado:
            messagebox.showinfo("OK", "Régimen actualizado")
            self.cargar_regimenes()

    # -----------------------------
    # BORRAR
    # -----------------------------

    def borrar_regimen(self):

        seleccionado = self.tabla.focus()

        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un régimen")
            return

        regimen_borrar = self.tabla.item(seleccionado)["values"][0]

        endpoint = self.endpoint+"/"+regimen_borrar

        resultado = delete(endpoint)

        if resultado:
            messagebox.showinfo("OK", "Régimen borrado")
            self.cargar_regimenes()









