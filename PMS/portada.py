import tkinter as tk

class Portada(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        titulo = tk.Label(
            self,
            text="Bienvenido al Sistema de Gestión Hotelera",
            font=("Arial", 24, "bold")
        )
        titulo.pack(pady=20)

        mensaje = tk.Label(
            self,
            text="Gestione reservas y clientes de manera eficiente",
            font=("Arial", 16)
        )
        mensaje.pack(pady=10)

        btn_inicio = tk.Button(
            self,
            text="Iniciar",
            command=lambda: controller.mostrar_panel()
        )
        btn_inicio.pack(pady=20)