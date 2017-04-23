import numpy as np
import matplotlib.pyplot as plt
import sys
import re
from kafe import *
from kafe.function_library import *

# HELP
if sys.argv[1] == "help":
	print( "help function for fitting data")
	print( "\tARGUMENTS:\n")
	print( "\t mandatory: Filename of Data")
	print( "\t optional: 'xname=' and 'yname=' for x- and y-axis label")
	print( "\t optional: 'xerr' and 'yerr' to plot x- and y-errors")
	print( "\t optional: 'save' to save the file as pdf in 'pdf=' file")
	print( "\t optional: 'title=' to change name of dataset")
	print( "\t optional: 'fittype=' to change from a linear fit model to another. In the code a custom fit model can be specified and used with 'filetype=custom'")
	sys.exit()
#

# options
bool_options = {"xerr": False, "yerr": False, "save": False}
name_options = {"fittype": linear_2par, "xname": "x-axis", "yname": "y-axis", "title": "data","pdf": "plot.pdf"}
for arg in sys.argv:
	if "fittype=" in arg:
		name_options["fittype"] = arg[8:]
	elif "xname=" in arg:
		name_options["xname"] = arg[6:]
	elif "yname=" in arg:
		name_options["yname"] = arg[6:]
	elif "title=" in arg:
		name_options["title"] = arg[6:]

	bool_options[arg] = True

# Load data from file
name_options["file"] = sys.argv[1]

# structure should be x,y,(xerr),(yerr)
x_data = []
y_data = []
xerr_data = []
yerr_data = []
with open(name_options["file"]) as f:
	lines = f.readlines()
	for line in lines:
		coord = line.replace("\n","").split("\t")
		x_data += [float(coord[0])]
		y_data += [float(coord[1])]
		if bool_options["xerr"]:
			xerr_data += [float(coord[2])]
			if bool_options["yerr"]:
				yerr_data += [float(coord[3])]
		elif bool_options["yerr"]:
			yerr_data += [float(coord[2])]

# dataset
data = Dataset(data=[x_data,y_data], axis_labels=[name_options["xname"],name_options["yname"]], title = name_options["title"])

# errors
if bool_options["xerr"]:
	data.add_error_source("x", "simple", xerr_data)
if bool_options["yerr"]:
	data.add_error_source("y", "simple", yerr_data)

# custom fit function
@LaTeX(name="f", x_name="x",parameter_names=("a","b","c"),
	expression="a\\exp(x\\,b)+c")
@FitFunction
def fit_func(x, a = 1, b = 1, c = 0):
	return a*np.exp(x*b) + c

# fit
if name_options["fittype"] == "custom":
	fit = Fit(data, fit_func)
else:
	fit = Fit(data, name_options["fittype"])
fit.do_fit()

# plot
plot = Plot(fit)
plot.plot_all()
plot.show()

# save
if bool_options["save"]:
	plot.save(name_options["pdf"])
