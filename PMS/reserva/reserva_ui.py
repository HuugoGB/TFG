import tkinter as tk
from tkinter import ttk, messagebox
from api.webservice import get, post, put, delete


class Reserva(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)

        self.endpoint = "/reservas"

        self.crear_widgets()

    # ----------------------
    # INTERFAZ
    # ----------------------

    def crear_widgets(self):

        frame_top = tk.LabelFrame(self, text="Gestión de Reservas")
        frame_top.pack(fill="x", padx=10, pady=10)

        tk.Button(frame_top, text="Crear Reserva",
                  command=self.crear_reserva).pack(side="left", padx=10)


        # frame donde se cargará todo el contenido dinámico
        self.frame_contenido = tk.Frame(self)
        self.frame_contenido.pack(fill="both", expand=True)

    # ----------------------
    # UTILIDAD
    # ----------------------

    def limpiar_contenido(self):
        for widget in self.frame_contenido.winfo_children():
            widget.destroy()

    def crear_reserva(self):
        pass
