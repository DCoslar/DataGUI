import matplotlib
import tkinter as tk
from datetime import datetime

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

px = 1/plt.rcParams['figure.dpi']
matplotlib.use('TkAgg')


class GraphPage(tk.Frame):
    __slots__ = "mpl_canvas"

    def __init__(self, parent, fig=None):
        tk.Frame.__init__(self, parent)
        self.grid(row=0, column=0, sticky="NWES")
        self.figure = fig
        self.last_time = datetime.now()

    @property
    def canvas(self):
        return self.mpl_canvas

    @canvas.setter
    def canvas(self, fig):
        try:
            self.mpl_canvas.get_tk_widget().pack_forget()
        except AttributeError:
            pass
        self.update()
        self.figure = fig
        self.mpl_canvas = FigureCanvasTkAgg(fig, self)
        self.mpl_canvas.draw()
        self.mpl_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def redraw(self, event=None):
        new_size = self.master.winfo_width(), self.master.winfo_height()
        print(f"{new_size=}")
        new_plt = self.figure.set_size_inches(w=new_size[0]*px, h=new_size[1]*px)
        self.canvas = self.figure


class MPLGraph(Figure):
    def __init__(self, size=(0, 0)):
        Figure.__init__(self, figsize=(size[0]*px, size[1]*px), dpi=100)
        self.plot = self.add_subplot(111)
        self.plot.plot([1, 2, 3, 4, 5, 6, 7], [4, 3, 5, 0, 2, 0, 6])


if __name__ == "__main__":
    fig = MPLGraph()

    root = tk.Tk()
    graph_page = GraphPage(root)
    graph_page.figure = fig

    root.mainloop()