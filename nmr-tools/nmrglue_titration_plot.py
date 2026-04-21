"""
Erik Walinda
Kyoto University
Graduate School of Medicine

Titration Zoom Ups for publication.
Full spectrum + individual ROIs
2024/09/15 

Requires:
* nmrglue (conda install)
* matplotlib

Zoom-up linewidth: 1.0
Full spectrum needs thinner linewidth
"""

import matplotlib as mpl

# Set Times New Roman as the global font
mpl.rcParams['font.family'] = 'Times New Roman'

import nmrglue as ng
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

#global_linewidth = 1.0
#global_linewidth = 0.2
global_linewidth = 0.2
#global_contourmpl = 1.10  # Most peaks
global_contourmpl = 1.15   # For some peaks required

class Spectrum:
    def __init__(self, filepath, color, contour_levels, linewidth=global_linewidth, shift_1h=0.0, shift_15n=0.0):
        # Read the spectrum data
        self.dic, self.data = ng.pipe.read(filepath)
        self.color = color
        self.contour_levels = contour_levels
        self.linewidth = linewidth
        
        # Get PPM limits along each axis
        self.uc_15n = ng.pipe.make_uc(self.dic, self.data, 0)
        self.uc_1h = ng.pipe.make_uc(self.dic, self.data, 1)
        self.x0, self.x1 = self.uc_1h.ppm_limits()
        self.y0, self.y1 = self.uc_15n.ppm_limits()

        # (Optional) Apply shifts (like CCPN referencing)
        self.x0 = self.x0 + shift_1h
        self.x1 = self.x1 + shift_1h
        self.y0 = self.y0 + shift_15n
        self.y1 = self.y1 + shift_15n

    def plot_spectrum(self, ax, xlim, ylim):
        # Plot the spectrum on the provided axis with user-defined xlim and ylim
        ax.contour(self.data, self.contour_levels, colors=self.color,
                   extent=(self.x0, self.x1, self.y0, self.y1),
                   linewidths=self.linewidth)

# Function to plot spectra with a user-defined region of interest (ROI)
def plot_multiple_spectra(spectrum_files, outfile, xlim, ylim):
    fig = plt.figure(figsize=(5, 4))
    ax = fig.add_subplot(111)

    # Plot each spectrum
    for spectrum in spectrum_files:
        spectrum.plot_spectrum(ax, xlim, ylim)

    # Set the user-defined axis limits
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)

    x = range(0, 100)
    y = [i**0.5 for i in x]
    # Reduce number of ticks
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=3))  # at most n x-ticks
    ax.yaxis.set_major_locator(ticker.MaxNLocator(nbins=2))  # at most n y-ticks

    # Label the axes
    #ax.set_xlabel("1H / ppm", size=20)     # Add in illustrator
    #ax.set_ylabel("15N / ppm", size=20)

    # Save the figure
    fig.savefig(outfile, transparent=True)
    plt.close()


def calculate_aspect_ratio(user_x_lim, user_ylim):
    # Calculate the width and height of the region
    width = abs(user_xlim[1] - user_xlim[0])
    height = abs(user_ylim[1] - user_ylim[0])

    # Calculate the aspect ratio
    aspect_ratio = width / height

    # Print the aspect ratio
    print(f"Aspect Ratio: {aspect_ratio}")

def loadSpectra(globalScale):
    contour_mpl = global_contourmpl
    spectra = [
        Spectrum(filepath="1.ft2", color='black', contour_levels=[globalScale * 4.0e5 * contour_mpl ** x for x in range(30)],
                shift_1h=0.0,       # Optional: ppm shift in 1H
                shift_15n=-0.0),    # ppm shift in 15N

        Spectrum(filepath="2eq.ft2", color='red', contour_levels=[globalScale * 1.5e5 * contour_mpl ** x for x in range(30)],
                shift_1h=0.0,       # ppm shift in 1H
                shift_15n=-0.0),    # ppm shift in 15N
    ]
    return spectra

# --- Full ---
# Define the region of interest (xlim and ylim in ppm)
user_xlim = (10.2, 6.0)
user_ylim = (135, 101.0)
plot_multiple_spectra(loadSpectra(4.5), "full.pdf", xlim=user_xlim, ylim=user_ylim)


mpl.rcParams['font.size'] = 16            # default font size
mpl.rcParams['axes.titlesize'] = 18       # title
mpl.rcParams['axes.labelsize'] = 16       # x/y labels
mpl.rcParams['xtick.labelsize'] = 14      # x tick labels
mpl.rcParams['ytick.labelsize'] = 14      # y tick labels

# --- Residue Zoom-up ---
#user_xlim = (10.25, 9.85)
#user_ylim = (124.0, 121.0)
#plot_multiple_spectra(loadSpectra(1.8), "C779.pdf", xlim=user_xlim, ylim=user_ylim)
