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

global_linewidth = 0.2
global_contourmpl = 1.10

class Spectrum:
    def __init__(self, filepath, color, contour_levels, linewidth=global_linewidth):
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

    # Label the axes
    #ax.set_xlabel("1H / ppm", size=20)     # Add in illustrator
    #ax.set_ylabel("15N / ppm", size=20)

    # Save the figure
    fig.savefig(outfile)
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
        Spectrum(filepath="monoUb_0eq.ft2", color='black', contour_levels=[globalScale * 8.0e5 * contour_mpl ** x for x in range(20)]),
        Spectrum(filepath="monoUb_0.25eq.ft2", color='blue', contour_levels=[globalScale * 7.5e5 * contour_mpl ** x for x in range(20)]),
        Spectrum(filepath="monoUb_0.5eq.ft2", color='green', contour_levels=[globalScale * 5.0e5 * contour_mpl ** x for x in range(20)]),
        Spectrum(filepath="monoUb_0.75eq.ft2", color='orange', contour_levels=[globalScale * 5.0e5 * contour_mpl ** x for x in range(20)]),
        Spectrum(filepath="monoUb_1eq.ft2", color='cyan', contour_levels=[globalScale * 5.0e5 * contour_mpl ** x for x in range(20)]),
        Spectrum(filepath="monoUb_2eq.ft2", color='purple', contour_levels=[globalScale * 5.0e5 * contour_mpl ** x for x in range(20)]),
        Spectrum(filepath="monoUb_4eq.ft2", color='grey', contour_levels=[globalScale * 5.0e5 * contour_mpl ** x for x in range(20)]),
        Spectrum(filepath="monoUb_8eq.ft2", color='red', contour_levels=[globalScale * 5.0e5 * contour_mpl ** x for x in range(20)]),
    ]
    return spectra

# --- Full ---
# Define the region of interest (xlim and ylim in ppm)
user_xlim = (10.2, 6.5)
user_ylim = (131.5, 101.0)
plot_multiple_spectra(loadSpectra(4.5), "full_distal.pdf", xlim=user_xlim, ylim=user_ylim)
