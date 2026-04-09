import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from api.webservice import get, post, put, delete, patch
from datetime import datetime, timedelta




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
            "habitacion",
            "estado"
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
        self.tabla.heading("estado", text="Estado")

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
        frame_botones = tk.LabelFrame(self, text="Funciones")
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Check In", command=self.check_in).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Check Out", command=self.check_out).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Crear", command=self.crear_reserva).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Editar", command=self.editar_reserva).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Cancelar", command=self.cancelar_reserva).pack(side="left", padx=5)
        tk.Button(frame_botones, text="Borrar", command=self.borrar_reserva).pack(side="left", padx=5)
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
                    r["idHabitacion"],
                    r["estado"]
                )
            )



    # ----------------------
    # CRUD
    # ----------------------

    def check_in(self):
        popup = tk.Toplevel(self)
        popup.title("Check-in de Reservas")
        popup.geometry("600x400")
        popup.resizable(False, False)

        # ---------------- FECHA ----------------
        tk.Label(popup, text="Fecha de Entrada:").pack(pady=5)

        entry_fecha = DateEntry(
            popup,
            date_pattern="yyyy-mm-dd",
            width=12
        )
        entry_fecha.pack(pady=5)

        # ---------------- TABLA ----------------
        columnas = ("idReserva", "cliente", "habitacion", "entrada", "estado")

        tabla = ttk.Treeview(popup, columns=columnas, show="headings")

        for col in columnas:
            tabla.heading(col, text=col)
            tabla.column(col, anchor="center", width=100)

        tabla.pack(fill="both", expand=True, padx=10, pady=10)

        # ---------------- CARGAR RESERVAS ----------------
        def cargar_reservas_fecha(event=None):
            fecha = entry_fecha.get()

            endpoint = f"/reservas/buscar?campo=dia_entrada&valor={fecha}"
            datos = get(endpoint)

            # limpiar tabla
            for item in tabla.get_children():
                tabla.delete(item)

            if not datos:
                return

            for r in datos["resultReservas"]:
                # solo mostrar las que NO estén ya en check-out o posteriores
                if r["estado"] not in ("Check-out", "Cancelada"):
                    tabla.insert(
                        "",
                        tk.END,
                        values=(
                            r["idReserva"],
                            r["idCliente"],
                            r["idHabitacion"],
                            r["dia_entrada"],
                            r["estado"]
                        )
                    )

        entry_fecha.bind("<<DateEntrySelected>>", cargar_reservas_fecha)

        # ---------------- HACER CHECK-IN ----------------
        def hacer_check_in():
            seleccionados = tabla.selection()

            if not seleccionados:
                messagebox.showwarning("Aviso", "Selecciona al menos una reserva")
                return

            for item in seleccionados:
                valores = tabla.item(item)["values"]
                idReserva = valores[0]

                patch(f"{self.endpoint}/estado/{idReserva}", {
                    "estado": "Check-in"
                })

            messagebox.showinfo("OK", "Check-in realizado correctamente")
            popup.destroy()
            self.cargar_reservas()

        # ---------------- BOTONES ----------------
        tk.Button(popup, text="Check-in", command=hacer_check_in).pack(padx=10)
        tk.Button(popup, text="Cerrar", command=popup.destroy).pack(padx=10)

        popup.transient(self)
        popup.grab_set()
        popup.focus()

    def check_out(self):
        popup = tk.Toplevel(self)
        popup.title("Check-out de Reservas")
        popup.geometry("700x400")
        popup.resizable(False, False)

        # ---------------- FECHA ----------------
        tk.Label(popup, text="Fecha de salida:").pack(pady=5)

        entry_fecha = DateEntry(
            popup,
            date_pattern="yyyy-mm-dd",
            width=16
        )
        entry_fecha.pack(pady=5)

        # ---------------- TABLA ----------------
        columnas = ("id", "cliente", "habitacion", "entrada", "salida", "estado")

        tabla = ttk.Treeview(popup, columns=columnas, show="headings", height=10)

        for col in columnas:
            tabla.heading(col, text=col.capitalize())
            tabla.column(col, anchor="center", width=100)

        tabla.pack(pady=10, fill="x", padx=10)

        # ---------------- CARGAR RESERVAS ----------------
        def cargar_reservas_fecha(event=None):
            fecha = entry_fecha.get()

            endpoint = f"/reservas/buscar?campo=dia_salida&valor={fecha}"
            datos = get(endpoint)

            # limpiar tabla
            for item in tabla.get_children():
                tabla.delete(item)

            if not datos:
                return

            for r in datos["resultReservas"]:
                tabla.insert(
                    "",
                    tk.END,
                    values=(
                        r["idReserva"],
                        r["idCliente"],
                        r["idHabitacion"],
                        r["dia_entrada"],
                        r["dia_salida"],
                        r["estado"]
                    )
                )

        # evento al cambiar fecha
        entry_fecha.bind("<<DateEntrySelected>>", cargar_reservas_fecha)

        # ---------------- CHECK OUT ----------------
        def hacer_checkout():
            seleccionados = tabla.selection()

            if not seleccionados:
                messagebox.showwarning("Aviso", "Selecciona al menos una reserva")
                return

            for item in seleccionados:
                valores = tabla.item(item)["values"]
                idReserva = valores[0]

                patch(f"{self.endpoint}/estado/{idReserva}", {
                    "estado": "Check-out"
                })

            messagebox.showinfo("OK", "Check-in realizado correctamente")
            popup.destroy()
            self.cargar_reservas()

        # ---------------- BOTONES ----------------
        frame_botones = tk.Frame(popup)
        frame_botones.pack(pady=10)

        tk.Button(frame_botones, text="Check-out", command=hacer_checkout).pack(side="left", padx=10)
        tk.Button(frame_botones, text="Cerrar", command=popup.destroy).pack(side="left", padx=10)

        popup.transient(self)
        popup.grab_set()
        popup.focus()



    def cargar_reservas(self):

        reservas = get(self.endpoint)

        if not reservas:
            return

        # 🔥 cargar todos los mapas
        self.cargar_agencias()
        self.cargar_clientes()
        self.cargar_habitaciones_map()
        self.cargar_regimenes()
        self.cargar_tipos_hab()

        # limpiar tabla
        for item in self.tabla.get_children():
            self.tabla.delete(item)

        for r in reservas["resultReservas"]:

            # ---------------- CONVERSIONES ----------------
            nombre_agencia = self.agencias_map.get(r["cif"], "Sin agencia")
            nombre_cliente = self.clientes_map.get(r["idCliente"], "Desconocido")
            numero_hab = self.habitaciones_map.get(r["idHabitacion"], "Sin asignar")
            regimen_desc = self.regimenes_map_inv.get(r["tipoRegimen"], r["tipoRegimen"])
            tipo_desc = self.tipoHab_map_inv.get(r["codigo"], r["codigo"])

            # ---------------- FORMATO FECHAS ----------------
            entrada = ""
            salida = ""

            if r["dia_entrada"]:
                try:
                    entrada = datetime.strptime(r["dia_entrada"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                except:
                    entrada = r["dia_entrada"][:10]

            if r["dia_salida"]:
                try:
                    salida = datetime.strptime(r["dia_salida"], "%Y-%m-%dT%H:%M:%S.%fZ").strftime("%Y-%m-%d")
                except:
                    salida = r["dia_salida"][:10]

            self.tabla.insert(
                "",
                tk.END,
                values=(
                    r["idReserva"],
                    entrada,
                    salida,
                    "Sí" if r["pagado"] else "No",
                    r["precio_total"],
                    r["totalPersonas"],
                    tipo_desc,
                    regimen_desc,
                    nombre_agencia,
                    nombre_cliente,
                    numero_hab,
                    r["estado"]
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
        mañana = datetime.now() + timedelta(days=1)
        entry_salida = DateEntry(
            formulario,
            date_pattern="yyyy-mm-dd",
            width=16
        )
        entry_salida.set_date(mañana)
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

        # ---------------- DISPONIBILIDAD TIPO HABS----------------
        def cargar_tipos():
            pax = spin_personas.get().strip()
            if not pax:
                return

            endpoint = f"/tipo_habitacion/disponibilidad?pax={pax}&dia_entrada={entry_entrada.get()}&dia_salida={entry_salida.get()}"

            tipoHabs = get(endpoint)

            self.tipoHabs_map = {}
            opciones = []

            for a in tipoHabs["result"]:
                self.tipoHabs_map[a["denominacion"]] = a["codigo"]
                opciones.append(a["denominacion"])

            combo_codigo["values"] = opciones

            if opciones:
                combo_codigo.set(opciones[0])
            else:
                combo_codigo.set("")

        # 🔥 EVENTOS CORRECTOS
        entry_entrada.bind("<<DateEntrySelected>>", lambda e: cargar_tipos())
        entry_salida.bind("<<DateEntrySelected>>", lambda e: cargar_tipos())

        # 🔥 CARGA INICIAL (CLAVE)
        formulario.after(100, cargar_tipos)

        # ---------------- PERSONAS ----------------
        tk.Label(formulario, text="Total Personas:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        spin_personas = tk.Spinbox(formulario, from_=1, to=5, width=5,command=cargar_tipos)
        spin_personas.grid(row=3, column=1, padx=10, pady=5)


        # ---------------- CÓDIGO ----------------
        tk.Label(formulario, text="Código:").grid(row=4, column=0, padx=10, pady=5, sticky="e")

        self.tipoHabs_map = {}
        combo_codigo = ttk.Combobox(formulario, state="readonly", width=18)
        combo_codigo.grid(row=4, column=1, padx=10, pady=5)

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
            formato = "%Y-%m-%d"  # ajusta según tu formato

            entrada = datetime.strptime(entry_entrada.get(), formato)
            salida = datetime.strptime(entry_salida.get(), formato)

            if entrada >= salida:
                messagebox.showerror("Error", "La fecha de salida debe ser mayor que la de entrada")
                return
            datos = {
                "dia_entrada": entry_entrada.get().strip(),
                "dia_salida": entry_salida.get().strip(),
                "pagado": int(combo_pagado.get().split(" - ")[0]),
                "totalPersonas": int(spin_personas.get().strip()),
                "codigo": self.tipoHabs_map.get(combo_codigo.get()),
                "tipoRegimen": self.regimenes_map.get(combo_regimen.get()),
                "cif": self.agencias_map.get(combo_agencia.get()),
                "idCliente": self.clientes_map.get(combo_cliente.get())
            }

            print(datos)

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
        entry_entrada = DateEntry(
            formulario,
            date_pattern="yyyy-mm-dd",
            width=16
        )
        entry_entrada.grid(row=0, column=1, padx=10, pady=5)


        tk.Label(formulario, text="Día Salida:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        mañana = datetime.now() + timedelta(days=1)
        entry_salida = DateEntry(
            formulario,
            date_pattern="yyyy-mm-dd",
            width=16
        )
        entry_salida.set_date(mañana)
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

        # ---------------- ESTADO ----------------
        tk.Label(formulario, text="Estado:").grid(row=9, column=0, padx=10, pady=5, sticky="e")

        combo_estado = ttk.Combobox(
            formulario,
            values=("Pendiente", "Confirmada", "Check-in", "Check-out", "Cancelada"),
            state="readonly",
            width=18
        )
        combo_estado.grid(row=9, column=1, padx=10, pady=5)

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
                "pagado": combo_pagado.get().strip(),
                "totalPersonas": entry_personas.get().strip(),
                "codigo": self.tipoHabs_map.get(combo_codigo.get()),
                "tipoRegimen": self.regimenes_map.get(combo_regimen.get()),
                "cif": self.agencias_map.get(combo_agencia.get()),
                "idCliente": self.clientes_map.get(combo_cliente.get()),
                "idHabitacion": id_habitacion,
                "estado": combo_estado.get()
            }

            endpoint = f"{self.endpoint}/update/{idReserva_original}"
            resultado = put(endpoint, datos)

            if resultado:
                messagebox.showinfo("OK", "Reserva actualizada")
                formulario.destroy()
                self.cargar_reservas()

        # ---------------- BOTONES ----------------
        tk.Button(formulario, text="Actualizar", command=editar).grid(row=10, column=0, padx=10, pady=15)
        tk.Button(formulario, text="Cancelar", command=formulario.destroy).grid(row=10, column=1, padx=10, pady=15)

        formulario.transient(self)
        formulario.grab_set()
        formulario.focus()

    def cancelar_reserva(self):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona una Reserva")
            return

        idReserva = self.tabla.item(seleccionado)["values"][0]
        patch(f"{self.endpoint}/estado/{idReserva}", {
            "estado": "Cancelada"
        })

    def borrar_reserva(self):
        seleccionado = self.tabla.focus()

        if not seleccionado:
            messagebox.showwarning("Aviso", "Selecciona una Reserva")
            return

        idReserva = self.tabla.item(seleccionado)["values"][0]
        delete(f"{self.endpoint}/delete/{idReserva}")


    def cargar_agencias(self):
        agencias = get("/agencia")
        self.agencias_map = {}

        if agencias:
            for a in agencias["result"]:
                self.agencias_map[a["nombreAgencia"]] = a["cif"]

    def cargar_clientes(self):
        clientes = get("/clientes")
        self.clientes_map = {}

        if clientes:
            for c in clientes["resultClientes"]:
                self.clientes_map[c["idCliente"]] = c["nombre"]


    def cargar_habitaciones_map(self):
        habitaciones = get("/habitaciones")
        self.habitaciones_map = {}

        if habitaciones:
            for h in habitaciones["result"]:
                self.habitaciones_map[h["idHabitacion"]] = h["numero_hab"]


    def cargar_regimenes(self):
        regimenes = get("/regimen")
        self.regimenes_map_inv = {}

        if regimenes:
            for r in regimenes["resultRegimen"]:
                self.regimenes_map_inv[r["tipoRegimen"]] = r["descripcion"]


    def cargar_tipos_hab(self):
        tipos = get("/tipo_habitacion")
        self.tipoHab_map_inv = {}

        if tipos:
            for t in tipos["resultTipoHab"]:
                self.tipoHab_map_inv[t["codigo"]] = t["denominacion"]