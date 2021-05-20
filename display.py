from datastore import Data
import tkinter
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Display:

    def __init__(self, data, root):

        if not isinstance(data, Data):
            raise ValueError('Did not input a data class for arg "data"')
        if not isinstance(root, tkinter.Tk):
            raise ValueError('did not input tk root window for arg "root"')

        self.data = data

        fig = Figure(figsize=(10, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        self.temperature_line, = self.ax.plot(*data.g_temperature_dat)
        self.humidity_line, = self.ax.plot(*data.g_temperature_dat)

        self.tk_obj = FigureCanvasTkAgg(fig, master=root)
        self.tk_obj.draw()

    def update(self):
        self.temperature_line.set_xdata(self.data.g_temperature_dat[0])
        self.temperature_line.set_ydata(self.data.g_temperature_dat[1])

        self.humidity_line.set_xdata(self.data.g_humidity_dat[0])
        self.humidity_line.set_ydata(self.data.g_humidity_dat[1])

        self.ax.set_ylim([0, 100])
        # self.ax.set_xlim([self.data.latest_DHT - 20, self.data.latest_DHT])
        self.ax.set_xlim([0, 20])

        self.tk_obj.draw()
        self.tk_obj.flush_events()
