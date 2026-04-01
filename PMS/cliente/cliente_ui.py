import tkinter as tk
from tkinter import ttk, messagebox
from api.webservice import get, post, put, delete


class Clientes(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.endpoint = "/clientes"

        self.agencias_map = {}   # nombre -> cif
        self.agencias_dict = {}  # cif -> nombre

        self.crear_widgets()
        self.cargar_clientes()

    # ----------------------
    # INTERFAZ
    # ----------------------

    def crear_widgets(self):

        frame_top = tk.LabelFrame(self, text="Gestión de Clientes")
        frame_top.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_top, text="Buscar:").grid(row=0, column=0)

        # input dinámico
        self.input_busqueda = tk.Entry(frame_top)
        self.input_busqueda.grid(row=0, column=1, padx=5)

        tk.Label(frame_top, text="Buscar por:").grid(row=0, column=2, padx=5)

        self.campos_busqueda = {
            "Nombre": "nombre",
            "Apellido": "apellido",
            "DNI": "dni",
            "ID Cliente": "idCliente",
            "Email": "email",
            "Contraseña": "contrasena",
            "Agencia": "cif"
        }

        self.combo_busqueda = ttk.Combobox(
            frame_top,
            values=list(self.campos_busqueda.keys()),
            state="readonly",
            width=15
        )
        self.combo_busqueda.grid(row=0, column=3, padx=5)
        self.combo_busqueda.current(0)

        self.combo_busqueda.bind("<<ComboboxSelected>>", self.cambiar_input_busqueda)

        tk.Button(frame_top, text="Buscar", command=self.buscar_cliente).grid(row=0, column=4)

        # ------------------
        # TABLA
        # ------------------
        columnas = ("id", "nombre", "apellido", "dni", "email", "contrasena", "agencia")

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        self.tabla.bind("<Double-1>", self.ver_reservas_cliente)

        scroll.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)

        # ------------------
        # BOTONES
        # ------------------
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Crear", command=self.crear_cliente).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Editar", command=self.actualizar_cliente).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.eliminar_cliente).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Refrescar", command=self.cargar_clientes).pack(side="left", padx=5)

    # ----------------------
    # CARGAR AGENCIAS
    # ----------------------
    def cargar_agencias(self):
        agencias = get("/agencia")

        self.agencias_map = {}
        self.agencias_dict = {}

        if agencias:
            for a in agencias["result"]:
                self.agencias_map[a["nombreAgencia"]] = a["cif"]
                self.agencias_dict[a["cif"]] = a["nombreAgencia"]

    # ----------------------
    # CARGAR CLIENTES
    # ----------------------
    def cargar_clientes(self):

        datos = get(self.endpoint)
        if not datos:
            return

        self.cargar_agencias()

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for c in datos["resultClientes"]:
            nombre_agencia = self.agencias_dict.get(c["cif"], "Sin agencia")

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    c["idCliente"],
                    c["nombre"],
                    c["apellido"],
                    c["dni"],
                    c["email"],
                    c["contrasena"],
                    nombre_agencia
                )
            )

    # ----------------------
    # BUSCAR
    # ----------------------
    def buscar_cliente(self):

        campo_label = self.combo_busqueda.get()
        campo = self.campos_busqueda[campo_label]

        valor = self.input_busqueda.get().strip()

        if valor == "":
            self.cargar_clientes()
            return

        # CASO AGENCIA
        if campo_label == "Agencia":

            if valor not in self.agencias_map:
                messagebox.showwarning("Aviso", "Agencia no válida")
                return

            valor = self.agencias_map[valor]

        endpoint = f"{self.endpoint}/buscar?campo={campo}&valor={valor}"
        datos = get(endpoint)

        if not datos:
            return

        self.cargar_agencias()

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for c in datos["resultCliente"]:
            nombre_agencia = self.agencias_dict.get(c["cif"], "Sin agencia")

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    c["idCliente"],
                    c["nombre"],
                    c["apellido"],
                    c["dni"],
                    c["email"],
                    c["contrasena"],
                    nombre_agencia
                )
            )

    # ----------------------
    # CAMBIAR INPUT
    # ----------------------
    def cambiar_input_busqueda(self, event=None):

        parent = self.input_busqueda.master
        self.input_busqueda.destroy()

        campo = self.combo_busqueda.get()

        if campo == "Agencia":

            self.cargar_agencias()

            self.input_busqueda = ttk.Combobox(
                parent,
                values=list(self.agencias_map.keys()),
                state="readonly",
                width=18
            )

            self.input_busqueda.grid(row=0, column=1, padx=5)

            if self.agencias_map:
                self.input_busqueda.current(0)

        else:
            self.input_busqueda = tk.Entry(parent)
            self.input_busqueda.grid(row=0, column=1, padx=5)

    # ----------------------
    # CRUD
    # ----------------------
    def crear_cliente(self):

        formulario = tk.Toplevel(self)
        formulario.title("Crear Cliente")
        formulario.geometry("300x250")

        self.cargar_agencias()

        tk.Label(formulario, text="Nombre").grid(row=0, column=0)
        entry_nombre = tk.Entry(formulario)
        entry_nombre.grid(row=0, column=1)

        tk.Label(formulario, text="Apellido").grid(row=1, column=0)
        entry_apellido = tk.Entry(formulario)
        entry_apellido.grid(row=1, column=1)

        tk.Label(formulario, text="DNI").grid(row=2, column=0)
        entry_dni = tk.Entry(formulario)
        entry_dni.grid(row=2, column=1)

        tk.Label(formulario, text="Agencia").grid(row=3, column=0)
        combo_agencia = ttk.Combobox(formulario, values=list(self.agencias_map.keys()), state="readonly")
        combo_agencia.grid(row=3, column=1)
        combo_agencia.current(0)

        tk.Label(formulario, text="Email").grid(row=4, column=0)
        entry_email = tk.Entry(formulario)
        entry_email.grid(row=4, column=1)

        tk.Label(formulario, text="Contraseña").grid(row=5, column=0)
        entry_pass = tk.Entry(formulario)
        entry_pass.grid(row=5, column=1)

        def crear():
            cif = self.agencias_map[combo_agencia.get()]

            datos = {
                "nombre": entry_nombre.get(),
                "apellido": entry_apellido.get(),
                "dni": entry_dni.get(),
                "cif": cif,
                "email": entry_email.get(),
                "contrasena": entry_pass.get()
            }

            if post(f"{self.endpoint}/create/", datos):
                messagebox.showinfo("OK", "Cliente creado")
                formulario.destroy()
                self.cargar_clientes()

        tk.Button(formulario, text="Crear", command=crear).grid(row=6, column=0)
        tk.Button(formulario, text="Cancelar", command=formulario.destroy).grid(row=6, column=1)

    # -----------------------------
    # ACTUALIZAR CLIENTE
    # -----------------------------
    def actualizar_cliente(self):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un Cliente")
            return

        idCliente = self.tabla.item(seleccionado)["values"][0]
        nombre_original = self.tabla.item(seleccionado)["values"][1]
        apellido_original = self.tabla.item(seleccionado)["values"][2]
        dni_original = self.tabla.item(seleccionado)["values"][3]
        email_original = self.tabla.item(seleccionado)["values"][4]
        contrasena_original = self.tabla.item(seleccionado)["values"][5]


        formulario = tk.Toplevel(self)
        formulario.title("Actualizar Cliente")
        formulario.geometry("300x250")
        formulario.resizable(False, False)

        # Nombre
        tk.Label(formulario, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_nombre = tk.Entry(formulario)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)
        entry_nombre.insert(0, nombre_original)

        # Apellido
        tk.Label(formulario, text="Apellido:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_apellido = tk.Entry(formulario)
        entry_apellido.grid(row=1, column=1, padx=10, pady=5)
        entry_apellido.insert(0, apellido_original)

        # DNI
        tk.Label(formulario, text="DNI:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_dni = tk.Entry(formulario)
        entry_dni.grid(row=2, column=1, padx=10, pady=5)
        entry_dni.insert(0, dni_original)

        # CIF/Agencia
        tk.Label(formulario, text="Agencia:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        agencias = get("/agencia")
        self.agencias_map = {}
        if agencias:
            for a in agencias["result"]:
                self.agencias_map[a["nombreAgencia"]] = a["cif"]
        combo_agencia = ttk.Combobox(formulario,values=list(self.agencias_map.keys()), state="readonly", width=15)
        combo_agencia.grid(row=3, column=1, padx=10, pady=5)
        combo_agencia.current(0)

        # Email
        tk.Label(formulario, text="Email:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        entry_email = tk.Entry(formulario)
        entry_email.grid(row=4, column=1, padx=10, pady=5)
        entry_email.insert(0, email_original)

        # Contraseña
        tk.Label(formulario, text="Contraseña:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        entry_contrasena = tk.Entry(formulario)
        entry_contrasena.grid(row=5, column=1, padx=10, pady=5)
        entry_contrasena.insert(0, contrasena_original)

        def actualizar():
            nombre_agencia = combo_agencia.get()
            cif = self.agencias_map[nombre_agencia]
            datos = {
                "nombre": entry_nombre.get().strip(),
                "apellido": entry_apellido.get().strip(),
                "dni": entry_dni.get().strip(),
                "cif": cif,
                "email": entry_email.get().strip(),
                "contrasena": entry_contrasena.get().strip()
            }
            endpoint = f"{self.endpoint}/update/{idCliente}"
            resultado = put(endpoint, datos)
            if resultado:
                messagebox.showinfo("OK", "Cliente actualizado")
                formulario.destroy()
                self.cargar_clientes()

        # Botones
        tk.Button(formulario, text="Actualizar", command=actualizar).grid(row=6, column=0, padx=10, pady=15)
        tk.Button(formulario, text="Cancelar", command=formulario.destroy).grid(row=6, column=1, padx=10, pady=15)

        # Modal
        formulario.transient(self)
        formulario.grab_set()
        formulario.focus()

    def eliminar_cliente(self):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        idCliente = self.tabla.item(seleccionado)["values"][0]

        if delete(f"{self.endpoint}/delete/{idCliente}"):
            self.cargar_clientes()

    # ----------------------
    # POPUP RESERVAS
    # ----------------------
    def ver_reservas_cliente(self, event=None):

        seleccionado = self.tabla.focus()
        idCliente = self.tabla.item(seleccionado)["values"][0]

        reservas = get(f"{self.endpoint}/reservasCliente/{idCliente}")

        if not reservas:
            return

        popup = tk.Toplevel(self)
        popup.title(f"Reservas {idCliente}")

        tabla = ttk.Treeview(
            popup,
            columns=("entrada", "salida", "precio"),
            show="headings"
        )

        tabla.heading("entrada", text="Entrada")
        tabla.heading("salida", text="Salida")
        tabla.heading("precio", text="Precio")

        tabla.pack(fill="both", expand=True)

        for r in reservas["resultReservas"]:
            tabla.insert("", tk.END, values=(r["dia_entrada"], r["dia_salida"], r["precio_total"]))