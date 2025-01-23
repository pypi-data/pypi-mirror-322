import ipywidgets as widgets
import matplotlib.colors as mcolors
import pandas as pd
from IPython.display import display, clear_output
from ipywidgets import Output

from pyccapt.calibration.calibration import ion_selection, mc_plot


def call_ion_selection(variables, colab=False):
	out = Output()
	output2 = Output()
	output3 = Output()

	bin_size = widgets.FloatText(value=0.1, description='bin size:')
	prominence = widgets.IntText(value=50, description='peak prominence:')
	distance = widgets.IntText(value=1, description='peak distance:')
	lim_tof = widgets.IntText(value=400, description='lim tof/mc:')
	percent = widgets.IntText(value=50, description='percent MRP:')
	index_fig = widgets.IntText(value=1, description='fig index:')
	plot_peak = widgets.Dropdown(
		options=[('True', True), ('False', False)],
		description='plot peak:'
	)
	save_fig = widgets.Dropdown(
		options=[('False', False), ('True', True)],
		description='save fig:'
	)

	def hist_plot_p(variables, out):

		with out:
			clear_output(True)
			# clear the peak_idx
			variables.peaks_idx = []
			mc_plot.hist_plot(variables, bin_size.value, log=True, target='mc', normalize=False,
			                  prominence=prominence.value, distance=distance.value, percent=percent.value,
			                  selector='peak', figname=index_fig.value, lim=lim_tof.value,
			                  peaks_find_plot=plot_peak.value, print_info=False, save_fig=save_fig.value)

	def hist_plot_r(variables, out):
		with out:
			clear_output(True)
			print('=============================')
			print('Press left click to draw a line')
			print('Press right click to remove a line')
			print('Press r to remove all the line')
			print('Hold shift and use mouse scroll for zooming on x axis')
			print('Hold ctrl and left mouse bottom to move a line')
			print('=============================')
			mc_plot.hist_plot(variables, bin_size.value, log=True, target='mc', normalize=False,
			                  prominence=prominence.value, distance=distance.value, percent=percent.value,
			                  selector='range', figname=index_fig.value, lim=lim_tof.value, peaks_find_plot=True,
			                  ranging_mode=True, save_fig=False, print_info=False)

	##############################################
	# element calculate
	peak_val = widgets.FloatText(value=1.1, description='peak value:')

	mass_difference = widgets.FloatText(value=2, description='mass range:')
	charge = widgets.Dropdown(
		options=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6)],
		value=3,
		description='charge:'
	)
	aboundance_threshold = widgets.FloatText(value=0.0, description='threshold aboundance:', min=0, max=1, step=0.1)
	num_element = widgets.IntText(value=5, description='num element:')
	# formula calculate
	formula_m = widgets.Text(
		value='{12}C1{16}O2',
		placeholder='Type a formula  {12}C1{16}O2',
		description='Isotope formula:',
		disabled=False
	)

	molecule_charge = widgets.Dropdown(
		options=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6)],
		value=3,
		description='charge:'
	)

	# molecule create
	formula_com = widgets.Text(
		value='',
		placeholder="H, O",
		description='Elements:',
		disabled=False
	)
	complexity = widgets.Dropdown(
		options=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6)],
		value=3,
		description='complexity:'
	)

	charge_com = widgets.Dropdown(
		options=[('1', 1), ('2', 2), ('3', 3), ('4', 4), ('5', 5), ('6', 6)],
		value=3,
		description='charge:'
	)

	##############################################
	plot_button_p = widgets.Button(
		description='plot hist',
	)

	plot_button_r = widgets.Button(
		description='plot hist',
	)

	plot_button = widgets.Button(
		description='plot hist',
	)

	find_elem_button = widgets.Button(
		description='find element',
	)

	plot_element = widgets.Button(
		description='plot element',
	)

	formula_button = widgets.Button(
		description='manual formula',
	)

	add_ion_button = widgets.Button(
		description='add ion',
	)
	romove_ion_button = widgets.Button(
		description='remove ion',
	)
	show_color = widgets.Button(
		description='show color',
	)
	change_color = widgets.Button(
		description='change color',
	)

	change_row = widgets.Button(
		description='change row',
	)

	color_picker = widgets.ColorPicker(description='Select a color:')
	row_index = widgets.IntText(value=0, description='index row:')

	plot_button_p.on_click(lambda b: plot_on_click_p(b, variables, out))

	def plot_on_click_p(b, variables, out):
		plot_button_p.disabled = True
		hist_plot_p(variables, out)
		plot_button_p.disabled = False

	plot_button_r.on_click(lambda b: plot_on_click_r(b, variables, out))

	def plot_on_click_r(b, variables, out):
		plot_button_r.disabled = True
		hist_plot_r(variables, out)
		plot_button_r.disabled = False

	def plot_found_element(b, variables):
		variables.AptHistPlotter.plot_founded_range_loc(variables.ions_list_data, remove_lines=False)

	plot_element.on_click(lambda b: plot_found_element(b, variables))


	def vol_on_click(b, variables, output2):
		with output2:
			clear_output(True)
			df1 = ion_selection.load_elements(formula_com.value, aboundance_threshold.value, charge.value,
			                                  variables=variables)
			df2 = ion_selection.molecule_create(formula_com.value, complexity.value, charge.value,
			                                    aboundance_threshold.value, variables)
			df3 = ion_selection.find_closest_elements(peak_val.value, num_element.value, aboundance_threshold.value,
			                                          charge.value, variables=variables)
			df = pd.concat([df1, df2, df3], axis=0)
			df = df[(df['abundance'] >= aboundance_threshold.value)]
			df = df[abs(df['mass'] - peak_val.value) <= mass_difference.value]
			df = df.iloc[(df['mass'] - peak_val.value).abs().argsort()]
			# Reset the index to maintain a clean index order
			df.reset_index(drop=True, inplace=True)
			df = df[:num_element.value]
			variables.range_data_backup = df.copy()
			variables.ions_list_data = df.copy()
			display(df)

	find_elem_button.on_click(lambda b: vol_on_click(b, variables, output2))

	formula_button.on_click(lambda b: manual_formula(b, variables, output2))

	def manual_formula(b, variables, output2):
		with output2:
			if formula_m.value == '':
				print("Input is empty. Type the formula.")
			else:
				df = ion_selection.molecule_manual(formula_m.value, molecule_charge.value, latex=True,
				                                   variables=variables)
				clear_output(True)
				display(df)

	add_ion_button.on_click(lambda b: add_ion_to_range_dataset(b, variables, output3))

	def add_ion_to_range_dataset(b, variables, output3):
		ion_selection.ranging_dataset_create(variables, row_index.value, peak_val.value)
		with output3:
			clear_output(True)
			display(variables.range_data)

	romove_ion_button.on_click(lambda b: remove_ion_to_range_dataset(b, variables, output3))

	def remove_ion_to_range_dataset(b, variables, output3):
		if len(variables.range_data) >= 1:
			variables.range_data = variables.range_data.drop(len(variables.range_data) - 1)
			with output3:
				clear_output(True)
				display(variables.range_data)

	show_color.on_click(lambda b: show_color_ions(b, variables, output3))

	def show_color_ions(b, variables, output3):
		with output3:
			clear_output(True)
			display(variables.range_data.style.applymap(ion_selection.display_color, subset=['color']))

	change_color.on_click(lambda b: change_color_m(b, variables, output3))

	def change_color_m(b, variables, output3):
		with output3:
			selected_color = mcolors.to_hex(color_picker.value)
			variables.range_data.at[row_index.value, 'color'] = selected_color
			clear_output(True)
			display(variables.range_data.style.applymap(ion_selection.display_color, subset=['color']))

	# Create "Next" and "Previous" buttons

	start_button = widgets.Button(description="start")
	next_button = widgets.Button(description="next")
	prev_button = widgets.Button(description="previous")
	reset_zoom_button = widgets.Button(description="reset zoom")
	all_peaks_button = widgets.Button(description="add all peaks")

	# Define button click events
	start_button.on_click(lambda b: start_peak(b, variables))

	change_row.on_click(lambda b: move_and_sort_dataframe(b, variables, row_index_source.value, row_index_dest.value,
	                                                      output3))

	row_index_source = widgets.IntText(value=0, description='Target index:')
	row_index_dest = widgets.IntText(value=0, description='destination index:')

	def move_and_sort_dataframe(b, variables, row_index, destination_index, output3):
		# Check if the indices are valid
		with output3:
			if (row_index not in variables.range_data.index or destination_index < 0 or
					destination_index >= len(variables.range_data.index)):
				print("Invalid indices provided.")
				return variables.range_data

			# Move the row to the destination index
			row_to_move = variables.range_data.loc[row_index]
			variables.range_data = variables.range_data.drop(row_index)
			variables.range_data = pd.concat([variables.range_data.iloc[:destination_index],
			                                  pd.DataFrame([row_to_move]),
			                                  variables.range_data.iloc[destination_index:]])

			# Sort the DataFrame based on index
			variables.range_data.reset_index(drop=True, inplace=True)
			clear_output(True)
			display(variables.range_data)


	def start_peak(b, variables):
		variables.h_line_pos = []
		print('=============================')
		print('Press left click to draw a line')
		print('Press right click to remove a line')
		print('Press r to remove all the line')
		print('Press a to automatically draw lines')
		print('Hold shift and use mouse scroll for zooming on x axis')
		print('Hold ctrl and left mouse bottom to move a line')
		print('=============================')
		variables.peaks_index = 0
		peak_val.value = variables.peaks_x_selected[variables.peaks_index]
		print('peak idc:', variables.peaks_index, 'Peak location:', peak_val.value)
		variables.AptHistPlotter.zoom_to_x_range(x_min=peak_val.value - 5, x_max=peak_val.value + 5, reset=False)
		variables.AptHistPlotter.change_peak_color(peak_val.value, dx=0.2)
		# reset the range data backup
		variables.range_data_backup = pd.DataFrame()

	next_button.on_click(lambda b: next_peak(b, variables))

	def next_peak(b, variables):
		variables.peaks_index += 1
		if variables.peaks_index >= len(variables.peaks_x_selected):
			variables.peaks_index = 0
		peak_val.value = variables.peaks_x_selected[variables.peaks_index]
		print('peak idc:', variables.peaks_index, 'Peak location:', peak_val.value)
		variables.AptHistPlotter.zoom_to_x_range(x_min=peak_val.value - 5, x_max=peak_val.value + 5, reset=False)
		variables.AptHistPlotter.change_peak_color(peak_val.value, dx=0.2)
		variables.AptHistPlotter.line_manager.remove_all_lines()
		# reset the range data backup
		variables.range_data_backup = pd.DataFrame()

	prev_button.on_click(lambda b: prev_peak(b, variables))

	def prev_peak(b, variables):
		variables.peaks_index -= 1
		peak_val.value = variables.peaks_x_selected[variables.peaks_index]
		print('peak idc:', variables.peaks_index, 'Peak location:', peak_val.value)
		variables.AptHistPlotter.zoom_to_x_range(x_min=peak_val.value - 5, x_max=peak_val.value + 5, reset=False)
		variables.AptHistPlotter.change_peak_color(peak_val.value, dx=0.2)
		variables.AptHistPlotter.line_manager.remove_all_lines()

	reset_zoom_button.on_click(lambda b: rest_h_line(b, variables))

	def rest_h_line(b, variables):
		variables.AptHistPlotter.zoom_to_x_range(x_min=0, x_max=0, reset=True)

	all_peaks_button.on_click(lambda b: select_all_peaks(b, variables))

	def select_all_peaks(b, variables):
		variables.peaks_x_selected = variables.peak_x
		variables.peaks_index_list = [i for i in range(len(variables.peak_x))]

	tab1 = widgets.VBox([bin_size, index_fig, prominence, distance, lim_tof, percent, plot_peak, save_fig,
	                              widgets.HBox([plot_button_p, all_peaks_button])])
	tab2 = widgets.VBox([bin_size, index_fig, prominence, distance, lim_tof, percent, widgets.HBox(
		[widgets.VBox([plot_button_r, start_button, next_button, prev_button, reset_zoom_button])])])
	tab4 = widgets.VBox([widgets.HBox([widgets.VBox(
		[peak_val, charge, aboundance_threshold, mass_difference, num_element, formula_com, complexity,
		          find_elem_button, plot_element]),
		widgets.VBox([formula_m, molecule_charge, formula_button]),
		widgets.VBox([row_index, color_picker, add_ion_button, romove_ion_button,
		                       show_color, change_color]),
		widgets.VBox([row_index_source, row_index_dest, change_row])
	])])

	if not colab:
		tabs1 = widgets.Tab([tab1, tab2])
		tabs2 = widgets.Tab([tab4])
		tabs1.set_title(0, 'peak finder')
		tabs1.set_title(1, 'rangging')
		tabs2.set_title(0, 'element finder')
		# Create two Output widgets to capture the output of each plot
		out = Output()
		output2 = Output()
		output3 = Output()

		# Create an HBox to display the buttons side by side
		buttons_layout = widgets.HBox([tabs1, tabs2])

		# Create a VBox to display the output widgets below the buttons
		output_layout = widgets.HBox([out, widgets.VBox([output3, output2])])

		# Display the buttons and the output widgets
		display(buttons_layout, output_layout)

		with output3:
			display(variables.range_data)
	else:
		# Define the content for each tab
		tab_contents = {
			"Peak Finder": tab1,
			"Rangging": tab2,
			"Element Finder": tab4
		}

		# Create buttons for each "tab"
		buttons = [widgets.Button(description=title) for title in tab_contents.keys()]

		# Output widgets to display the corresponding content
		out = widgets.Output()
		out_tab = widgets.Output()
		output2 = widgets.Output()
		output3 = widgets.Output()

		# Function to handle button clicks
		def on_button_click(title):
			def handler(change):
				with out:
					clear_output(wait=True)
				with out_tab:
					clear_output(wait=True)
					display(tab_contents[title])

			return handler

		# Attach handlers to buttons
		for button in buttons:
			button.on_click(on_button_click(button.description))

		# Layout for buttons and outputs
		buttons_layout = widgets.HBox(buttons)
		output_layout = widgets.HBox([widgets.VBox([out_tab, out]), widgets.VBox([output3, output2])])

		# Display the buttons and output areas
		display(buttons_layout, output_layout)

		# Initial display
		with out_tab:
			display(tab_contents["Peak Finder"])  # Default to the first "tab" content
		with output3:
			display(variables.range_data)
