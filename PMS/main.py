import tkinter as tk

from portada import Portada
from panel_pms import PanelPMS


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("PMS")
        self.state("zoomed")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.mostrar_portada()

    def mostrar_portada(self):

        self.limpiar_contenido()


        portada = Portada(self.container, self)
        portada.pack(fill="both", expand=True)

    def mostrar_panel(self):

        self.limpiar_contenido()

        panel = PanelPMS(self.container, self)
        panel.pack(fill="both", expand=True)

    def limpiar_contenido(self):
        for widget in self.container.winfo_children():
                    widget.destroy()

if __name__ == "__main__":
    app = App()
    app.mainloop()