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
        self.temp_ax = fig.add_subplot(111)
        self.hum_ax = self.temp_ax.twinx()

        self.temp_line, = self.temp_ax.plot(*data.g_temp_dat, 'r-')
        self.hum_line, = self.hum_ax.plot(*data.g_hum_dat, 'b-')

        self.tk_obj = FigureCanvasTkAgg(fig, master=root)
        self.tk_obj.draw()

        # y limit set here to stop the graph from conforming to the data
        self.temp_ax.set_ylim([0, 40])
        self.hum_ax.set_ylim([0, 100])
        self.temp_ax.set_xlabel('time (seconds)')
        self.temp_ax.set_ylabel('temperature (deg Celsius)', color='r')
        self.hum_ax.set_ylabel('humidity (% concentration)', color='b')

    def update(self):
        self.temp_line.set_xdata(self.data.g_temp_dat[0])
        self.temp_line.set_ydata(self.data.g_temp_dat[1])

        self.hum_line.set_xdata(self.data.g_hum_dat[0])
        self.hum_line.set_ydata(self.data.g_hum_dat[1])

        self.temp_ax.set_xlim([self.data.latest_DHT - 100, self.data.latest_DHT])

        self.tk_obj.draw()
        self.tk_obj.flush_events()

