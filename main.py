import tkinter as tk

from portada import Portada
from panel_pms import PanelPMS


class App(tk.Tk):

    def __init__(self):
        super().__init__()

        self.title("PMS")
        self.geometry("1600x900")

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.mostrar_portada()

    def mostrar_portada(self):

        for widget in self.container.winfo_children():
            widget.destroy()

        portada = Portada(self.container, self)
        portada.pack(fill="both", expand=True)

    def mostrar_panel(self):

        for widget in self.container.winfo_children():
            widget.destroy()

        panel = PanelPMS(self.container, self)
        panel.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = App()
    app.mainloop()