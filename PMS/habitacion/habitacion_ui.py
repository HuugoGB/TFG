import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from api.webservice import get, post
from datetime import datetime, timedelta



class Habitacion(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.endpoint_hab = "/habitaciones"
        self.endpoint_tipohab = "/tipo_habitacion"

        self.crear_widgets()

    # ----------------------
    # INTERFAZ
    # ----------------------

    def crear_widgets(self):

        frame_top = tk.LabelFrame(self, text="Gestión de Habitaciones")
        frame_top.pack(fill="x", padx=10, pady=10)

        tk.Button(frame_top, text="Crear Tipo Habitacion",
                  command=self.crear_tipo_habitacion).pack(side="left", padx=10)

        tk.Button(frame_top, text="Crear Habitacion",
                  command=self.crear_habitaciones).pack(side="left", padx=10)

        tk.Button(frame_top, text="Ver Disponibilidad Tipo Habitacion",
                  command=self.disponibilidad_tipohab).pack(side="left", padx=10)

        tk.Button(frame_top, text="Ver Habitacion Reservada",
                  command=self.disponibilidad_hab).pack(side="left", padx=10)

        # frame donde se cargará todo el contenido dinámico
        self.frame_contenido = tk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True)

    # ----------------------
    # UTILIDAD
    # ----------------------

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    # ----------------------
    # CREAR TIPO HAB
    # ----------------------

    def crear_tipo_habitacion(self):

        self.limpiar_contenido()

        frame = tk.Frame(self.frame_contenido)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Codigo:").grid(row=0, column=0)
        entry_codigo = tk.Entry(frame)
        entry_codigo.grid(row=0, column=1)

        tk.Label(frame, text="Denominacion:").grid(row=1, column=0)
        entry_denominacion = tk.Entry(frame)
        entry_denominacion.grid(row=1, column=1)

        tk.Label(frame, text="Personas:").grid(row=2, column=0)
        spin_personas = tk.Spinbox(frame, from_=1, to=6, width=5)
        spin_personas.grid(row=2, column=1)

        tk.Label(frame, text="Precio:").grid(row=3, column=0)
        entry_precio = tk.Entry(frame)
        entry_precio.grid(row=3, column=1)

        def crear():

            datos = {
                "codigo": entry_codigo.get().strip(),
                "denominacion": entry_denominacion.get().strip(),
                "pax": spin_personas.get(),
                "precio": entry_precio.get().strip()
            }

            endpoint = f"{self.endpoint_tipohab}/create"
            resultado = post(endpoint, datos)

            if resultado:
                messagebox.showinfo("OK", "Tipo habitación creado")
                self.limpiar_contenido()

        tk.Button(frame, text="Crear", command=crear).grid(row=4, column=0, pady=10)

    # ----------------------
    # CREAR HABITACIONES
    # ----------------------

    def crear_habitaciones(self):

        self.limpiar_contenido()

        frame = tk.Frame(self.frame_contenido)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Tipo Hab:").grid(row=0, column=0)

        tipos_hab = get(self.endpoint_tipohab)

        self.tipohab_map = {}

        if tipos_hab:
            for t in tipos_hab["resultTipoHab"]:
                self.tipohab_map[t["denominacion"]] = t["codigo"]

        combo_tipohab = ttk.Combobox(
            frame,
            values=list(self.tipohab_map.keys()),
            state="readonly"
        )

        combo_tipohab.grid(row=0, column=1)

        if self.tipohab_map:
            combo_tipohab.current(0)

        tk.Label(frame, text="Cantidad:").grid(row=1, column=0)

        spin_cantidad = tk.Spinbox(frame, from_=1, to=20, width=5)
        spin_cantidad.grid(row=1, column=1)

        def crear():

            denominacion = combo_tipohab.get()
            codigo = self.tipohab_map[denominacion]

            datos = {"codigo": codigo}

            endpoint = f"{self.endpoint_hab}/create/{spin_cantidad.get()}"

            resultado = post(endpoint, datos)

            if resultado:
                messagebox.showinfo("OK", "Habitaciones creadas")
                self.limpiar_contenido()

        tk.Button(frame, text="Crear", command=crear).grid(row=2, column=0, pady=10)

    # ----------------------
    # DISPONIBILIDAD TIPO HAB
    # ----------------------

    def disponibilidad_tipohab(self):

        self.limpiar_contenido()

        frame = tk.Frame(self.frame_contenido)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Fecha Entrada").grid(row=0, column=0)
        entry_entrada = DateEntry(
            frame,
            date_pattern="yyyy-mm-dd",
            width=12
        )
        entry_entrada.grid(row=0, column=1)

        tk.Label(frame, text="Fecha Salida").grid(row=1, column=0)
        mañana = datetime.now() + timedelta(days=1)
        entry_salida = DateEntry(
            frame,
            date_pattern="yyyy-mm-dd",
            width=12
        )
        entry_salida.set_date(mañana)
        entry_salida.grid(row=1, column=1, padx=10, pady=5)

        tabla = ttk.Treeview(
            self.frame_contenido,
            columns=("denominacion", "total_habitaciones", "habitaciones_disponibles"),
            show="headings"
        )

        tabla.heading("denominacion", text="Tipo Habitación")
        tabla.heading("total_habitaciones", text="Habitaciones Totales")
        tabla.heading("habitaciones_disponibles", text="Habitaciones Disponibles")


        tabla.pack(fill="both", expand=True, pady=10)

        def consultar():

            endpoint = f"{self.endpoint_tipohab}/disponibilidad_todas?dia_entrada={entry_entrada.get()}&dia_salida={entry_salida.get()}"

            datos = get(endpoint)

            if not datos:
                return



            for r in datos["result"]:
                tabla.insert("", tk.END, values=(r["denominacion"], r["total_habitaciones"], r["habitaciones_disponibles"]))

        tk.Button(frame, text="Consultar", command=consultar).grid(row=2, column=0, pady=10)

    # ----------------------
    # HABITACIONES RESERVADAS
    # ----------------------

    def disponibilidad_hab(self):

        self.limpiar_contenido()

        frame = tk.Frame(self.frame_contenido)
        frame.pack(padx=10, pady=10)

        tk.Label(frame, text="Fecha Entrada").grid(row=0, column=0)

        entry_entrada = DateEntry(
            frame,
            date_pattern="yyyy-mm-dd",
            width=12
        )
        entry_entrada.grid(row=0, column=1)

        tk.Label(frame, text="Fecha Salida").grid(row=1, column=0)
        mañana = datetime.now() + timedelta(days=1)
        entry_salida = DateEntry(
            frame,
            date_pattern="yyyy-mm-dd",
            width=12
        )
        entry_salida.set_date(mañana)
        entry_salida.grid(row=1, column=1, padx=10, pady=5)

        # Tipo de habitación
        tk.Label(frame, text="Tipo Hab").grid(row=2, column=0)

        tipos_hab = get(self.endpoint_tipohab)

        self.tipohab_map = {}

        if tipos_hab:
            for t in tipos_hab["resultTipoHab"]:
                self.tipohab_map[t["denominacion"]] = t["codigo"]

        combo_tipohab = ttk.Combobox(
            frame,
            values=list(self.tipohab_map.keys()),
            state="readonly",
            width=15
        )

        combo_tipohab.grid(row=2, column=1)

        if self.tipohab_map:
            combo_tipohab.current(0)

        tabla = ttk.Treeview(
            self.frame_contenido,
            columns=("id", "numero", "camas", "codigo"),
            show="headings"
        )

        tabla.heading("id", text="ID")
        tabla.heading("numero", text="Número Hab")
        tabla.heading("camas", text="Camas")
        tabla.heading("codigo", text="Tipo")

        tabla.pack(fill="both", expand=True, pady=10)

        def consultar():

            denominacion = combo_tipohab.get()
            codigo = self.tipohab_map[denominacion]

            entrada = entry_entrada.get()
            salida = entry_salida.get()

            endpoint = f"{self.endpoint_hab}/disponibilidad?dia_entrada={entrada}&dia_salida={salida}&codigo={codigo}"

            datos = get(endpoint)

            if not datos:
                return

            for item in tabla.get_children():
                tabla.delete(item)

            for r in datos["resultDisponibilidad"]:
                tabla.insert(
                    "",
                    tk.END,
                    values=(
                        r["idHabitacion"],
                        r["numero_hab"],
                        r["camas"],
                        r["codigo"]
                    )
                )

        tk.Button(frame, text="Consultar", command=consultar).grid(row=3, column=0, pady=10)