import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from api.webservice import get, post, put, delete


class Reserva(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.endpoint = "/reservas"

        self.crear_widgets()
        self.cargar_reservas()

    # ----------------------
    # INTERFAZ
    # ----------------------

    def crear_widgets(self):

        frame_top = tk.LabelFrame(self, text="Gestión de Reservas")
        frame_top.pack(fill="x", padx=10, pady=10)

        # Buscador
        tk.Label(frame_top, text="Buscar:").grid(row=0, column=0)

        # input dinámico
        self.input_busqueda = tk.Entry(frame_top)
        self.input_busqueda.grid(row=0, column=1, padx=5)


        tk.Label(frame_top, text="Buscar por:").grid(row=0, column=2, padx=5)
        # Diccionario de mapeo

        self.campos_busqueda = {
            "ID Reserva": "idReserva",
            "Cliente": "idCliente",
            "Habitación": "idHabitacion",
            "Código": "codigo",
            "Régimen": "tipoRegimen",
            "Pagado": "pagado",
            "Agencia": "cif",
            "Fecha Entrada": "dia_entrada",
            "Fecha Salida": "dia_salida"
        }
        self.combo_busqueda = ttk.Combobox(
            frame_top,
            values = list(self.campos_busqueda.keys()),
            state="readonly",
            width=12
        )

        self.combo_busqueda.grid(row=0, column=3, padx=5)
        self.combo_busqueda.current(0)  # valor por defecto


        self.combo_busqueda.bind("<<ComboboxSelected>>", self.cambiar_input_busqueda)

        btn_buscar = tk.Button(frame_top, text="Buscar", command=self.buscar_reservas)
        btn_buscar.grid(row=0, column=4)


        # Tabla (Treeview)
        # ------------------
        # TABLA RESERVAS
        # ------------------
        columnas = (
            "idReserva",
            "entrada",
            "salida",
            "pagado",
            "precio",
            "personas",
            "codigo",
            "regimen",
            "cif",
            "cliente",
            "habitacion"
        )

        frame_tabla = tk.Frame(self)
        frame_tabla.pack(fill="both", expand=True, padx=10, pady=10)

        self.tabla = ttk.Treeview(frame_tabla, columns=columnas, show="headings")

        self.tabla.heading("idReserva", text="ID")
        self.tabla.heading("entrada", text="Entrada")
        self.tabla.heading("salida", text="Salida")
        self.tabla.heading("pagado", text="Pagado")
        self.tabla.heading("precio", text="Precio")
        self.tabla.heading("personas", text="Personas")
        self.tabla.heading("codigo", text="Código")
        self.tabla.heading("regimen", text="Régimen")
        self.tabla.heading("cif", text="Agencia")
        self.tabla.heading("cliente", text="Cliente")
        self.tabla.heading("habitacion", text="Habitación")

        # Ajuste de columnas (MUY recomendable)
        for col in columnas:
            self.tabla.column(col, anchor="center", width=100)

        scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll.set)

        scroll.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)


        # ------------------
        # BOTONES
        # ------------------
        frame_botones = tk.Frame(self)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Crear", command=self.crear_reserva).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Editar", command=self.editar_reserva).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Eliminar", command=self.cancelar_reserva).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Refrescar", command=self.cargar_reservas).pack(side="left", padx=5)

    # ----------------------
    # UTILIDAD
    # ----------------------

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()
    # ----------------------
    # CAMBIAR INPUT
    # ----------------------
    def cambiar_input_busqueda(self, event=None):

        parent = self.input_busqueda.master
        self.input_busqueda.destroy()

        campo = self.combo_busqueda.get()

        #AGENCIA
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

        # FECHA (NUEVO)
        elif campo == "Fecha Entrada":

            self.input_busqueda = DateEntry(
                parent,
                width=18,
                date_pattern='yyyy-mm-dd'
            )
            self.input_busqueda.grid(row=0, column=1, padx=5)

        # FECHA (NUEVO)
        elif campo == "Fecha Salida":

            self.input_busqueda = DateEntry(
                parent,
                width=18,
                date_pattern='yyyy-mm-dd'
            )
            self.input_busqueda.grid(row=0, column=1, padx=5)

        # ⚪ RESTO
        else:
            self.input_busqueda = tk.Entry(parent)
            self.input_busqueda.grid(row=0, column=1, padx=5)

    def buscar_reservas(self):
        campo_label = self.combo_busqueda.get()
        campo = self.campos_busqueda[campo_label]

        valor = self.input_busqueda.get().strip()

        if valor == "":
            self.cargar_reservas()
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

        for r in datos["resultReservas"]:
            nombre_agencia = self.agencias_map.get(r["cif"], "Sin agencia")

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    r["idReserva"],
                    r["dia_entrada"],
                    r["dia_salida"],
                    r["pagado"],
                    r["precio_total"],
                    r["totalPersonas"],
                    r["codigo"],
                    r["tipoRegimen"],
                    nombre_agencia,
                    r["idCliente"],
                    r["idHabitacion"]
                )
            )



    # ----------------------
    # CRUD
    # ----------------------


    def cargar_reservas(self):

        reservas = get(self.endpoint)

        if not reservas:
            return

        for item in self.tabla.get_children():
            self.tabla.delete(item)

        self.cargar_agencias()

        for r in reservas["resultReservas"]:
            nombre_agencia = self.agencias_map.get(r["cif"], "Sin agencia")
            self.tabla.insert(
                "",
                tk.END,
                values=(
                    r["idReserva"],
                    r["dia_entrada"],
                    r["dia_salida"],
                    "Sí" if r["pagado"] else "No",
                    r["precio_total"],
                    r["totalPersonas"],
                    r["codigo"],
                    r["tipoRegimen"],
                    r["cif"],
                    r["idCliente"],
                    r["idHabitacion"]
                )
            )

    def crear_reserva(self):
        formulario = tk.Toplevel(self)
        formulario.title("Crear Reserva")
        formulario.geometry("400x450")
        formulario.resizable(False, False)

        # ---------------- FECHAS ----------------
        tk.Label(formulario, text="Día Entrada:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_entrada = DateEntry(
            formulario,
            date_pattern="yyyy-mm-dd",
            width=16
        )
        entry_entrada.grid(row=0, column=1, padx=10, pady=5)


        tk.Label(formulario, text="Día Salida:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_salida = DateEntry(
            formulario,
            date_pattern="yyyy-mm-dd",
            width=16
        )
        entry_salida.grid(row=1, column=1, padx=10, pady=5)

        # ---------------- PAGADO ----------------
        tk.Label(formulario, text="Pagado:").grid(row=2, column=0, padx=10, pady=5, sticky="e")

        combo_pagado = ttk.Combobox(
            formulario,
            values=["0 - No", "1 - Sí"],
            state="readonly",
            width=18
        )
        combo_pagado.grid(row=2, column=1, padx=10, pady=5)
        combo_pagado.current(0)

        # ---------------- PERSONAS ----------------
        tk.Label(formulario, text="Total Personas:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        spin_personas = tk.Spinbox(formulario, from_=1, to=5, width=5)
        spin_personas.grid(row=3, column=1, padx=10, pady=5)

        # ---------------- CÓDIGO ----------------

        tk.Label(formulario, text="Código:").grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.tipoHabs_map = {}
        combo_codigo = ttk.Combobox(formulario, state="readonly", width=18)
        combo_codigo.grid(row=4, column=1, padx=10, pady=5)

        def cargar_tipos():
            pax = spin_personas.get().strip()

            if not pax:
                return

            endpoint = f"/tipo_habitacion/disponibilidad?pax={pax}&dia_entrada={entry_entrada.get()}&dia_salida={entry_salida.get()}"

            tipoHabs = get(endpoint)

            self.tipoHabs_map = {}
            opciones = []

            if tipoHabs and "resultTipoHab" in tipoHabs:
                for a in tipoHabs["resultTipoHab"]:
                    self.tipoHabs_map[a["denominacion"]] = a["codigo"]
                    opciones.append(a["denominacion"])

            combo_codigo["values"] = opciones

            if opciones:
                combo_codigo.set(opciones[0])

        spin_personas.bind("<KeyRelease>", lambda e: cargar_tipos())
        entry_entrada.bind("<<DateEntrySelected>>", lambda e: cargar_tipos())
        entry_salida.bind("<<DateEntrySelected>>", lambda e: cargar_tipos())

        # ---------------- REGIMEN ----------------
        tk.Label(formulario, text="Régimen:").grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.regimenes_map = {}
        regimenes = get("/regimen")

        if regimenes:
            for a in regimenes["resultRegimen"]:
                self.regimenes_map[a["descripcion"]] = a["tipoRegimen"]

        combo_regimen = ttk.Combobox(
            formulario,
            values=list(self.regimenes_map.keys()),
            state="readonly",
            width=18
        )
        combo_regimen.grid(row=5, column=1, padx=10, pady=5)

        if combo_regimen["values"]:
            combo_regimen.current(0)

        # ---------------- AGENCIA ----------------
        tk.Label(formulario, text="Agencia:").grid(row=6, column=0, padx=10, pady=5, sticky="e")

        self.agencias_map = {}
        agencias = get("/agencia")

        if agencias:
            for a in agencias["result"]:
                self.agencias_map[a["nombreAgencia"]] = a["cif"]

        combo_agencia = ttk.Combobox(
            formulario,
            values=list(self.agencias_map.keys()),
            state="readonly",
            width=18
        )
        combo_agencia.grid(row=6, column=1, padx=10, pady=5)

        if combo_agencia["values"]:
            combo_agencia.current(0)

        # ---------------- CLIENTE ----------------
        tk.Label(formulario, text="Cliente:").grid(row=7, column=0, padx=10, pady=5, sticky="e")

        self.clientes_map = {}
        clientes = get("/clientes")

        if clientes:
            for a in clientes["resultClientes"]:
                self.clientes_map[a["nombre"]] = a["idCliente"]

        combo_cliente = ttk.Combobox(
            formulario,
            values=list(self.clientes_map.keys()),
            state="readonly",
            width=18
        )
        combo_cliente.grid(row=7, column=1, padx=10, pady=5)

        if combo_cliente["values"]:
            combo_cliente.current(0)

        # ---------------- CREAR ----------------
        def crear():
            if entry_entrada.get() >= entry_salida.get():
                messagebox.showerror("Error", "La fecha de salida debe ser mayor que la de entrada")
                return
            id_hab = self.habitaciones_map.get(combo_habs.get())

            if not id_hab:
                messagebox.showerror("Error", "Selecciona una habitación válida")
                return

            datos = {
                "diaEntrada": entry_entrada.get().strip(),
                "diaSalida": entry_salida.get().strip(),
                "pagado": combo_pagado.get().split(" - ")[0],
                "totalPersonas": spin_personas.get().strip(),
                "codigo": self.tipoHabs_map.get(combo_codigo.get()),
                "tipoRegimen": self.regimenes_map.get(combo_regimen.get()),
                "cif": self.agencias_map.get(combo_agencia.get()),
                "idCliente": self.clientes_map.get(combo_cliente.get()),
                "idHabitacion": id_hab
            }

            endpoint = f"{self.endpoint}/create"
            resultado = post(endpoint, datos)

            if resultado:
                messagebox.showinfo("OK", "Reserva creada correctamente")
                formulario.destroy()
                self.cargar_reservas()

        # ---------------- BOTONES ----------------
        tk.Button(formulario, text="Crear", command=crear).grid(row=9, column=0, padx=10, pady=15)
        tk.Button(formulario, text="Cancelar", command=formulario.destroy).grid(row=9, column=1, padx=10, pady=15)

        formulario.transient(self)
        formulario.grab_set()
        formulario.focus()

    def editar_reserva(self):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona una Reserva")
            return

        valores = self.tabla.item(seleccionado)["values"]

        idReserva_original = valores[0]
        diaEntrada_original = valores[1]
        diaSalida_original = valores[2]
        pagado_original = valores[3]
        precioTotal_original = valores[4]
        totalPersonas_original = valores[5]
        codigo_original = valores[6]
        tipoRegimen_original = valores[7]
        cif_original = valores[8]
        idCliente_original = valores[9]
        idHabitacion_original = valores[10]

        formulario = tk.Toplevel(self)
        formulario.title("Actualizar Reserva")
        formulario.geometry("400x450")
        formulario.resizable(False, False)

        # ---------------- FECHAS ----------------
        tk.Label(formulario, text="Día Entrada:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        entry_entrada = tk.Entry(formulario)
        entry_entrada.grid(row=0, column=1, padx=10, pady=5)
        entry_entrada.insert(0, diaEntrada_original)

        tk.Label(formulario, text="Día Salida:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        entry_salida = tk.Entry(formulario)
        entry_salida.grid(row=1, column=1, padx=10, pady=5)
        entry_salida.insert(0, diaSalida_original)

        # ---------------- PAGADO ----------------
        tk.Label(formulario, text="Pagado:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        entry_pagado = tk.Entry(formulario)
        entry_pagado.grid(row=2, column=1, padx=10, pady=5)
        entry_pagado.insert(0, pagado_original)

        # ---------------- PERSONAS ----------------
        tk.Label(formulario, text="Total Personas:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        entry_personas = tk.Entry(formulario)
        entry_personas.grid(row=3, column=1, padx=10, pady=5)
        entry_personas.insert(0, totalPersonas_original)

        # ---------------- CÓDIGO ----------------
        tk.Label(formulario, text="Código:").grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.tipoHabs_map = {}
        tipoHabs = get(f"/tipo_habitacion/porPax/{totalPersonas_original}")

        if tipoHabs:
            for a in tipoHabs["resultTipoHab"]:
                self.tipoHabs_map[a["denominacion"]] = a["codigo"]

        combo_codigo = ttk.Combobox(
            formulario,
            values=list(self.tipoHabs_map.keys()),
            state="readonly",
            width=18
        )
        combo_codigo.grid(row=4, column=1, padx=10, pady=5)

        # Seleccionar original
        for k, v in self.tipoHabs_map.items():
            if v == codigo_original:
                combo_codigo.set(k)
                break

        # ---------------- REGIMEN ----------------
        tk.Label(formulario, text="Régimen:").grid(row=5, column=0, padx=10, pady=5, sticky="e")

        self.regimenes_map = {}
        regimenes = get("/regimen")

        if regimenes:
            for a in regimenes["resultRegimen"]:
                self.regimenes_map[a["descripcion"]] = a["tipoRegimen"]

        combo_regimen = ttk.Combobox(
            formulario,
            values=list(self.regimenes_map.keys()),
            state="readonly",
            width=18
        )
        combo_regimen.grid(row=5, column=1, padx=10, pady=5)

        for k, v in self.regimenes_map.items():
            if v == tipoRegimen_original:
                combo_regimen.set(k)
                break

        # ---------------- AGENCIA ----------------
        tk.Label(formulario, text="Agencia:").grid(row=6, column=0, padx=10, pady=5, sticky="e")

        self.agencias_map = {}
        agencias = get("/agencia")

        if agencias:
            for a in agencias["result"]:
                self.agencias_map[a["nombreAgencia"]] = a["cif"]

        combo_agencia = ttk.Combobox(
            formulario,
            values=list(self.agencias_map.keys()),
            state="readonly",
            width=18
        )
        combo_agencia.grid(row=6, column=1, padx=10, pady=5)

        for k, v in self.agencias_map.items():
            if str(v) == str(cif_original):
                combo_agencia.set(k)
                break

        # ---------------- CLIENTE ----------------
        tk.Label(formulario, text="Cliente:").grid(row=7, column=0, padx=10, pady=5, sticky="e")

        self.clientes_map = {}
        clientes = get("/clientes")

        if clientes:
            for a in clientes["resultClientes"]:
                self.clientes_map[a["nombre"]] = a["idCliente"]

        combo_cliente = ttk.Combobox(
            formulario,
            values=list(self.clientes_map.keys()),
            state="readonly",
            width=18
        )
        combo_cliente.grid(row=7, column=1, padx=10, pady=5)

        for k, v in self.clientes_map.items():
            if v == idCliente_original:
                combo_cliente.set(k)
                break

        # ---------------- HABITACIONES ----------------
        tk.Label(formulario, text="Habitación:").grid(row=8, column=0, padx=10, pady=5, sticky="e")

        self.habitaciones_map = {}

        combo_habs = ttk.Combobox(
            formulario,
            state="readonly",
            width=18
        )
        combo_habs.grid(row=8, column=1, padx=10, pady=5)

        def cargar_habitaciones(seleccionar_original=False):
            codigo = combo_codigo.get()
            if not codigo:
                return

            codigo_real = self.tipoHabs_map.get(codigo)

            endpoint = f"/habitaciones/disponibilidad?dia_entrada={entry_entrada.get()}&dia_salida={entry_salida.get()}&codigo={codigo_real}"

            habitaciones = get(endpoint)

            self.habitaciones_map = {}
            opciones = []

            if habitaciones:
                for a in habitaciones["resultDisponibilidad"]:
                    num = str(a["numero_hab"])
                    self.habitaciones_map[num] = a["idHabitacion"]
                    opciones.append(num)

                combo_habs["values"] = opciones

                if not opciones:
                    return

            # ✅ SI ES LA PRIMERA CARGA → seleccionar la original
            if seleccionar_original:
                for num, idHab in self.habitaciones_map.items():
                    if str(idHab) == str(idHabitacion_original):
                        combo_habs.set(num)
                        return

            # fallback
            combo_habs.set(opciones[0])

        # eventos para recargar
        entry_entrada.bind("<FocusOut>", lambda e: cargar_habitaciones())
        entry_salida.bind("<FocusOut>", lambda e: cargar_habitaciones())
        combo_codigo.bind("<<ComboboxSelected>>", lambda e: cargar_habitaciones())

        # cargar inicial
        cargar_habitaciones(seleccionar_original=True)
        # ---------------- EDITAR ----------------
        def editar():
            id_habitacion = self.habitaciones_map.get(combo_habs.get())

            if not id_habitacion:
                messagebox.showerror("Error", "Selecciona una habitación válida")
                return
            datos = {
                "diaEntrada": entry_entrada.get().strip(),
                "diaSalida": entry_salida.get().strip(),
                "pagado": entry_pagado.get().strip(),
                "totalPersonas": entry_personas.get().strip(),
                "codigo": self.tipoHabs_map.get(combo_codigo.get()),
                "tipoRegimen": self.regimenes_map.get(combo_regimen.get()),
                "cif": self.agencias_map.get(combo_agencia.get()),
                "idCliente": self.clientes_map.get(combo_cliente.get()),
                "idHabitacion": id_habitacion
            }

            endpoint = f"{self.endpoint}/update/{idReserva_original}"
            resultado = put(endpoint, datos)

            if resultado:
                messagebox.showinfo("OK", "Reserva actualizada")
                formulario.destroy()
                self.cargar_reservas()

        # ---------------- BOTONES ----------------
        tk.Button(formulario, text="Actualizar", command=editar).grid(row=9, column=0, padx=10, pady=15)
        tk.Button(formulario, text="Cancelar", command=formulario.destroy).grid(row=9, column=1, padx=10, pady=15)

        formulario.transient(self)
        formulario.grab_set()
        formulario.focus()

    def cancelar_reserva(self):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            return

        idReserva = self.tabla.item(seleccionado)["values"][0]

        if delete(f"{self.endpoint}/delete/{idReserva}"):
            self.cargar_reservas()


    def cargar_agencias(self):
        agencias = get("/agencia")
        self.agencias_map = {}

        if agencias:
            for a in agencias["result"]:
                self.agencias_map[a["nombreAgencia"]] = a["cif"]