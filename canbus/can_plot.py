# -*- coding: utf-8 -*-
"""
canPlot is a program to visualize CAN data from a text file, which 
is produced by the program readDecodeCANFromFile.py

"""
import numpy
from matplotlib import rcParams
import matplotlib.pyplot as plt
# load data
data = numpy.loadtxt("./resources/CANData.txt",
                     usecols=(0, 2,), delimiter=",")
# odd rows represent rpm data
rpm = data[::2]
# even rows represent fuel consumption data
fuelconsumption = data[1::2]


def plot_vehicle_data(data, x_label_text, y_label_text, title, save_path):
    """ plot_vehicle_data accepts 5 parameters and plots and saves the vehicle data as a pdf file.
    data: The vehicle data.
    x_label_text: The label on the x axis.
    y_label_text: The label on the y axis.
    title: The title of the plot.
    save_path: The path on which the pdf is saved.
    """
    # setup plot and adjust configuration
    # DIN A5 size
    plt.figure(figsize=(8.27, 5.83))
    # math type font
    plt.matplotlib.rcParams["mathtext.fontset"] = "stix"
    plt.matplotlib.rcParams["font.family"] = "STIXGeneral"
    # outward-oriented axes ticks
    rcParams["xtick.direction"] = "out"
    rcParams["ytick.direction"] = "out"
    # more parameters
    params = {
        "axes.labelsize": 10,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "font.family": "Monospace",
        "text.usetex": False,
    }
    # commit parameters
    rcParams.update(params)
    # no frame
    plt.axes(frameon=0)
    # light grid
    plt.grid()
    # generate plot
    plt.plot(data[:, 0]-data[0, 0], data[:, 1],
             color="k", linewidth=1, linestyle="-")
    plt.xlabel(x_label_text)
    plt.ylabel(y_label_text)
    plt.title(title)
    plt.savefig(save_path,  # This is simple recommendation for publication plots
                dpi=1000,
                # Plot will occupy a maximum of available space
                bbox_inches="tight")


plot_vehicle_data(fuelconsumption, "Vergangene Zeit ab erster Messung [s]",
                  "Verbrauchswert [l/h]", "Kraftstoffverbrauch", "./resources/Kraftstoffverbrauch.pdf")
plot_vehicle_data(rpm, "Vergangene Zeit ab erster Messung [s]",
                  "Drehzahl pro Minute", "Motordrehzahl", "./resources/RPM.pdf")
