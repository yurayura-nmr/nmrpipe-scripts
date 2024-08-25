# 1D visualization by projection
# 20240229 Erik Walinda, Kyoto University, Graduate School of Medicine


import nmrglue as ng
import matplotlib.pyplot as plt

# Update the default font family
plt.rcParams['font.family'] = 'Arial'

# Peak of interest
roi_1H = 8.39
roi_15N = 108.64
slice_15N = "108.64ppm"
secondSlice_15N = "107.4ppm"

titration_point = "1_1-0Ca"
scaling_factor_1D = 5e6 # still needs ns adjustment

# read in data
dic, data = ng.pipe.read(titration_point + ".ft2")

# find PPM limits along each axis
uc_15n = ng.pipe.make_uc(dic, data, 0)
uc_13c = ng.pipe.make_uc(dic, data, 1)
x0, x1 = uc_13c.ppm_limits()
y0, y1 = uc_15n.ppm_limits()

# plot the spectrum
fig = plt.figure(figsize=(10.5, 10.5))
fig = plt.figure()
ax = fig.add_subplot(111)
cl = [8.5e5 * 1.30 ** x for x in range(20)]
ax.contour(data, cl, colors='blue', extent=(x0, x1, y0, y1), linewidths=0.5)

# add 1D slices
x = uc_13c.ppm_scale()
s1 = data[uc_15n(slice_15N), :]
s2 = data[uc_15n(secondSlice_15N), :]

ax.plot(x, -s1 / scaling_factor_1D + roi_15N, 'k-')
ax.plot(x, -s2 / scaling_factor_1D + roi_15N, 'k-')

# label the axis and save
#ax.set_xlabel("1H ppm", size=20)
# Set the axis label with superscript
ax.set_xlabel(r'$^1$H chemical shift (ppm)', size=20, labelpad=0)  # Use LaTeX formatting for superscript

ax.set_xlim(roi_1H + 0.25, roi_1H - 0.25)
ax.set_ylabel(r'$^1$$^5$N chemical shift (ppm)', size=20, labelpad=0)
ax.set_ylim(roi_15N + 0.75, roi_15N - 1.75)
fig.savefig(titration_point + "_spectrum_2d.pdf")
