import tkinter as tk
from regimen.regimen_ui import Regimen
from cliente.cliente_ui import Clientes
from habitacion.habitacion_ui import Habitacion
from reserva.reserva_ui import Reserva

class PanelPMS(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)

        # menú lateral
        frame_menu = tk.Frame(self, width=200, bg="#2c3e50")
        frame_menu.pack(side="left", fill="y")

        # contenido
        self.frame_contenido = tk.Frame(self, bg="white")
        self.frame_contenido.pack(side="right", fill="both", expand=True)

        estilo_btn = {
            "width": 15,
            "height": 6,
            "bd": 5,
            "relief": "raised",
            "font": ("Arial", 12, "bold")
        }

        btn_clientes = tk.Button(
            frame_menu,
            text="Clientes",
            command=self.mostrar_clientes,
            **estilo_btn
        )
        btn_clientes.pack(fill="x")

        btn_reservas = tk.Button(
            frame_menu,
            text="Reservas",
            command=self.mostrar_reservas,
            **estilo_btn
        )

        btn_reservas.pack(fill="x")

        btn_regimenes = tk.Button(
            frame_menu,
            text="Regimenes",
            command=self.mostrar_regimenes,
            **estilo_btn
        )
        btn_regimenes.pack(fill="x")

        btn_habs = tk.Button(
            frame_menu,
            text="Habitaciones",
            command=self.mostrar_habitaciones,
            **estilo_btn
        )
        btn_habs.pack(fill="x")

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def mostrar_clientes(self):
        self.limpiar_contenido()
        frame = Clientes(self.frame_contenido)
        frame.pack(fill="both", expand=True)

    def mostrar_reservas(self):
        self.limpiar_contenido()
        frame = Reserva(self.frame_contenido)
        frame.pack(fill="both", expand=True)

    def mostrar_regimenes(self):
        self.limpiar_contenido()
        frame = Regimen(self.frame_contenido)
        frame.pack(fill="both", expand=True)

    def mostrar_habitaciones(self):
        self.limpiar_contenido()
        frame = Habitacion(self.frame_contenido)
        frame.pack(fill="both",expand=True)
