import tkinter as tk
from tkinter import ttk, messagebox
from api.webservice import get, post, put, delete


class Clientes(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.endpoint = "/clientes"

        self.crear_widgets()
        self.cargar_clientes()

    # ----------------------
    # INTERFAZ
    # ----------------------

    def crear_widgets(self):

        frame_top = tk.LabelFrame(self, text="Gestión de Clientes")
        frame_top.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_top, text="Buscar:").grid(row=0, column=0)

        self.entry_buscar = tk.Entry(frame_top)
        self.entry_buscar.grid(row=0, column=1, padx=5)

        tk.Label(frame_top, text="Buscar por:").grid(row=0, column=2, padx=5)
        # Diccionario de mapeo
        self.campos_busqueda = {
            "Nombre": "nombre",
            "Apellido": "apellido",
            "DNI": "dni",
            "ID Cliente": "idCliente"
        }
        self.combo_busqueda = ttk.Combobox(
            frame_top,
            values = list(self.campos_busqueda.keys()),
            state="readonly",
            width=12
        )

        self.combo_busqueda.grid(row=0, column=3, padx=5)
        self.combo_busqueda.current(0)  # valor por defecto

        btn_buscar = tk.Button(frame_top, text="Buscar", command=self.buscar_cliente)
        btn_buscar.grid(row=0, column=4)


        # ------------------
        # TABLA
        # ------------------
        columnas = ("id", "nombre", "apellido", "dni")

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")
        self.tabla.heading("id", text = "ID")
        self.tabla.heading("nombre", text = "Nombre")
        self.tabla.heading("apellido", text = "Apellido")
        self.tabla.heading("dni", text = "DNI")


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
    # CARGAR CLIENTES
    # ----------------------

    def cargar_clientes(self):

        datos = get(self.endpoint)

        if not datos:
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for c in datos["resultClientes"]:
            self.tabla.insert("",tk.END,values=(c["idCliente"], c["nombre"], c["apellido"], c["dni"]))

    # ----------------------
    # BUSCAR
    # ----------------------

    def buscar_cliente(self):

        campo = self.campos_busqueda[self.combo_busqueda.get()]
        valor = self.entry_buscar.get()

        if valor == "":
            self.cargar_clientes()
            return

        endpoint = f"{self.endpoint}/buscar?campo={campo}&valor={valor}"

        datos = get(endpoint)

        if not datos:
            return

        # limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        # rellenar tabla
        for c in datos["resultCliente"]:
            self.tabla.insert(
                "",
                tk.END,
                values=(c["idCliente"], c["nombre"], c["apellido"], c["dni"])
            )

    # -----------------------------
    # CREAR CLIENTE
    # -----------------------------
    def crear_cliente(self):
        formulario = tk.Toplevel(self)
        formulario.title("Crear Cliente")
        formulario.geometry("300x220")
        formulario.resizable(False, False)

        # Nombre
        tk.Label(formulario, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_nombre = tk.Entry(formulario)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5)

        # Apellido
        tk.Label(formulario, text="Apellido:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_apellido = tk.Entry(formulario)
        entry_apellido.grid(row=1, column=1, padx=10, pady=5)

        # DNI
        tk.Label(formulario, text="DNI:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_dni = tk.Entry(formulario)
        entry_dni.grid(row=2, column=1, padx=10, pady=5)

        # CIF/Agencia (Combo)
        tk.Label(formulario, text="Agencia:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        agencias = get("/agencia")
        self.agencias_map = {}
        if agencias:
            for a in agencias["result"]:
                self.agencias_map[a["nombreAgencia"]] = a["cif"]
        combo_agencia = ttk.Combobox(formulario,values=list(self.agencias_map.keys()), state="readonly", width=15)
        combo_agencia.grid(row=3, column=1, padx=10, pady=5)
        combo_agencia.current(0)

        def crear():
            nombre_agencia = combo_agencia.get()
            cif = self.agencias_map[nombre_agencia]
            datos = {
                "nombre": entry_nombre.get().strip(),
                "apellido": entry_apellido.get().strip(),
                "dni": entry_dni.get().strip(),
                "cif": cif
            }
            endpoint = f"{self.endpoint}/create/"
            resultado = post(endpoint, datos)
            if resultado:
                messagebox.showinfo("OK", "Cliente creado")
                formulario.destroy()
                self.cargar_clientes()

        # Botones
        tk.Button(formulario, text="Crear", command=crear).grid(row=4, column=0, padx=10, pady=15)
        tk.Button(formulario, text="Cancelar", command=formulario.destroy).grid(row=4, column=1, padx=10, pady=15)

        # Modal
        formulario.transient(self)
        formulario.grab_set()
        formulario.focus()


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

        formulario = tk.Toplevel(self)
        formulario.title("Actualizar Cliente")
        formulario.geometry("300x220")
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

        def actualizar():
            nombre_agencia = combo_agencia.get()
            cif = self.agencias_map[nombre_agencia]
            datos = {
                "nombre": entry_nombre.get().strip(),
                "apellido": entry_apellido.get().strip(),
                "dni": entry_dni.get().strip(),
                "cif": cif
            }
            endpoint = f"{self.endpoint}/update/{idCliente}"
            resultado = put(endpoint, datos)
            if resultado:
                messagebox.showinfo("OK", "Cliente actualizado")
                formulario.destroy()
                self.cargar_clientes()

        # Botones
        tk.Button(formulario, text="Actualizar", command=actualizar).grid(row=4, column=0, padx=10, pady=15)
        tk.Button(formulario, text="Cancelar", command=formulario.destroy).grid(row=4, column=1, padx=10, pady=15)

        # Modal
        formulario.transient(self)
        formulario.grab_set()
        formulario.focus()

    def eliminar_cliente(self):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona un régimen")
            return

        cliente_borrar = self.tabla.item(seleccionado)["values"][0]

        endpoint = f"{self.endpoint}/delete/{cliente_borrar}"

        resultado = delete(endpoint)

        if resultado:
            messagebox.showinfo("OK", "Cliente borrado")
            self.cargar_clientes()

    def ver_reservas_cliente(self, event=None):

        cliente_seleccionado = self.tabla.focus()

        idCliente = self.tabla.item(cliente_seleccionado)["values"][0]

        endpoint = f"{self.endpoint}/reservasCliente/{idCliente}"

        reservas_cliente = get(endpoint)

        if not reservas_cliente:
            return
        # ----------------------
        # POPUP
        # ----------------------
        popup = tk.Toplevel(self)
        popup.title(f"Reservas del cliente {idCliente}")
        popup.geometry("800x400")

        columnas = (
            "entrada", "salida", "pagado", "precio", "personas", "hab", "regimen"
        )

        tabla_reservas = ttk.Treeview(popup, columns=columnas, show="headings")

        tabla_reservas.heading("entrada", text="Entrada")
        tabla_reservas.heading("salida", text="Salida")
        tabla_reservas.heading("pagado", text="Pagado")
        tabla_reservas.heading("precio", text="Precio Total")
        tabla_reservas.heading("personas", text="Total Personas")
        tabla_reservas.heading("hab", text="Habitación")
        tabla_reservas.heading("regimen", text="Régimen")

        for col in columnas:
            tabla_reservas.column(col, width=100, anchor="center", stretch=True)

        # Cargar reservas
        for r in reservas_cliente["resultReservas"]:
            tabla_reservas.insert(
                "",
                tk.END,
                values=(
                    r["dia_entrada"],
                    r["dia_salida"],
                    "Sí" if r["pagado"] else "No",
                    r["precio_total"],
                    r["totalPersonas"],
                    r["codigo"],
                    r["tipoRegimen"]
                )
            )
        tabla_reservas.pack(fill="both", expand=True, padx=10, pady=10)







