import multiprocessing
import os
import sys
import threading
import time
from datetime import datetime

import numpy as np
import pandas as pd
import pyqtgraph as pg
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QTimer

try:
	from mcculw import ul
	from mcculw.enums import TempScale, TInOptions
except Exception as e:
	print('Cannot import mcculw library')
	print(e)

# Local module and scripts
from pyccapt.control.control import share_variables, read_files
from pyccapt.control.gui import gui_pumps_vacuum
from pyccapt.control.devices import initialize_devices


class Ui_Baking(object):

	def __init__(self, variables, conf, SignalEmitter_Pumps_Vacuum, parent=None):
		"""
		Initialize the UiBaking class.

		Args:
			variables: Instance of variables class.
			conf: Configuration settings.
			parent: Parent widget (default is None).
		"""
		self.variables = variables
		self.conf = conf
		self.emitter = SignalEmitter_Pumps_Vacuum
		self.parent = parent
		self.now = datetime.now()
		self.running = True
		self.vacuum_main = 0
		self.vacuum_buffer = 0
		self.vacuum_load_lock = 0
		self.vacuum_cryo_load_lock = 0

		self.data = pd.DataFrame(
			columns=['data', 'Time', 'timestamp', 'MC_vacuum', 'BC_vacuum', 'LL_vacuum', 'CLL_vacuum', 'MC_NEG',
			         'MC_Det', 'Mc_Top', 'MC_Gate', 'BC_Top', 'BC_Pump', 'CLL_gate', 'LL_pump'])
		now_time = self.now.strftime("%d-%m-%Y_%H-%M-%S")
		folders_above = os.path.abspath(os.path.join(os.getcwd(), "../"))
		self.save_path = folders_above + '/pyccapt/files/baking_logging/%s/' % now_time
		if not os.path.isdir(self.save_path):
			os.makedirs(self.save_path, mode=0o777, exist_ok=True)
		self.file_name = self.save_path + 'baking_logging_%s.csv' % now_time
		self.file_name_backup = self.save_path + 'backup_baking_logging_%s.csv' % now_time

	def setupUi(self, Baking):
		"""
		setupUi function.
		Args:
			Baking: Parent widget.

		Returns:
			None
		"""
		Baking.setWindowIcon(QtGui.QIcon('./files/logo.png'))
		Baking.setObjectName("Baking")
		Baking.resize(820, 757)
		self.gridLayout_2 = QtWidgets.QGridLayout(Baking)
		self.gridLayout_2.setObjectName("gridLayout_2")
		self.gridLayout = QtWidgets.QGridLayout()
		self.gridLayout.setObjectName("gridLayout")
		# self.tempretures = QtWidgets.QGraphicsView(parent=Baking)
		self.tempretures = pg.PlotWidget(parent=Baking)
		self.tempretures.setMinimumSize(QtCore.QSize(800, 500))
		self.tempretures.setObjectName("tempretures")
		self.gridLayout.addWidget(self.tempretures, 0, 0, 1, 1)
		self.save_data = QtWidgets.QPushButton(parent=Baking)
		self.save_data.setMinimumSize(QtCore.QSize(0, 25))
		self.save_data.setStyleSheet("QPushButton{\n"
		                             "background: rgb(193, 193, 193)\n"
		                             "}")
		self.save_data.setObjectName("save_data")
		self.gridLayout.addWidget(self.save_data, 2, 0, 1, 1)
		# self.presures = QtWidgets.QGraphicsView(parent=Baking)
		self.presures = pg.PlotWidget(parent=Baking)
		self.presures.setMinimumSize(QtCore.QSize(800, 200))
		self.presures.setObjectName("presures")
		self.gridLayout.addWidget(self.presures, 1, 0, 1, 1)
		self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

		self.retranslateUi(Baking)
		QtCore.QMetaObject.connectSlotsByName(Baking)
		###
		read_thread = threading.Thread(target=self.read)
		read_thread.setDaemon(True)
		read_thread.start()

		self.save_data.clicked.connect(self.save_data_csv)

		# Create a QTimer to hide the warning message after 8 seconds
		self.timer = QTimer(self.parent)
		self.timer.timeout.connect(self.plot)
		self.timer.start(1000)

		self.tempretures.addLegend()
		styles = {"color": "#f00", "font-size": "12px"}
		self.tempretures.setLabel("left", "Temperature (C)", **styles)
		self.tempretures.setLabel("bottom", "Time (sec)", **styles)

		self.presures.addLegend()
		styles = {"color": "#f00", "font-size": "12px"}
		self.presures.setLabel("left", "Pressure (mBar)", **styles)
		self.presures.setLabel("bottom", "Time (sec)", **styles)

		self.emitter.vacuum_main.connect(self.update_vacuum_main)
		self.emitter.vacuum_buffer.connect(self.update_vacuum_buffer)
		self.emitter.vacuum_load_lock.connect(self.update_vacuum_load)
		self.emitter.vacuum_cryo_load_lock.connect(self.update_vacuum_cryo_load_lock)
	def retranslateUi(self, Baking):
		"""
		retranslateUi function.
		Args:
			Baking: Parent widget.

		Returns:
			None
		"""
		_translate = QtCore.QCoreApplication.translate
		###
		#  Baking.setWindowTitle(_translate("Baking", "Form"))
		Baking.setWindowTitle(_translate("Baking", "PyCCAPT Baking"))
		Baking.setWindowIcon(QtGui.QIcon('../files/logo.png'))
		###
		self.save_data.setText(_translate("Baking", "Save CSV"))

	def update_vacuum_main(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		if value == -1:
			print('Error')
		else:
			self.vacuum_main = value

	def update_vacuum_buffer(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		if value == -1:
			print('Error')
		else:
			self.vacuum_buffer = value

	def update_vacuum_load(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		if value == -1:
			print('Error')
		else:
			self.vacuum_load_lock = value

	def update_vacuum_cryo_load_lock(self, value):
		"""
		Update the vacuum value in the GUI
		Args:
			value: the temperature value

		Return:
			None
		"""
		if value == -1:
			print('Error')
		else:
			self.vacuum_cryo_load_lock = value


	def read(self):
		"""
		Read function.

		Args:
			None
		Returns:
			None
		"""
		if not self.variables.flag_pumps_vacuum_start:
			try:
				tpg = initialize_devices.TPG362(port='COM5')
			except Exception as e:
				print(f"Error connecting to TPG362:{e}")
				tpg = None
			if conf['COM_PORT_gauge_ll'] != "off":
				try:
					E_AGC_ll = initialize_devices.EdwardsAGC(variables.COM_PORT_gauge_ll, variables)
				except Exception as e:
					print(f"Error connecting to LL gauge:{e}")
					E_AGC_ll = None
			if conf['COM_PORT_gauge_cll'] != "off":
				try:
					E_AGC_cll = initialize_devices.EdwardsAGC(variables.COM_PORT_gauge_cll, variables)
				except Exception as e:
					print(f"Error connecting to CLL gauge:{e}")
					E_AGC_cll = None

		index = 0
		desired_period = 1.0
		if self.conf['baking'] == 'on':
			while self.running:
				start_time = time.perf_counter()
				# print('-----------', index, 'seconds', '--------------')
				if not self.variables.flag_pumps_vacuum_start:
					try:
						gauge_bc, _ = tpg.pressure_gauge(1)
					except Exception as e:
						print(f"Error reading BC:{e}")
						# Handle the case where response is not a valid float
						gauge_bc = -1
					try:
						gauge_mc, _ = tpg.pressure_gauge(2)
					except Exception as e:
						print(f"Error reading MC:{e}")
						# Handle the case where response is not a valid float
						gauge_mc = -1
					response = initialize_devices.command_edwards(conf, variables, 'pressure', E_AGC=E_AGC_ll,
					                                              status='load_lock')

					try:
						gauge_ll = float(response.replace(';', ' ').split()[2]) * 0.01
					except Exception as e:
						print(f"Error reading LL:{e}")
						# Handle the case where response is not a valid float
						gauge_ll = -1
					response = initialize_devices.command_edwards(conf, variables, 'pressure', E_AGC=E_AGC_cll,
					                                              status='cryo_load_lock')

					try:
						gauge_cll = float(response.replace(';', ' ').split()[2]) * 0.01
					except Exception as e:
						print(f"Error reading CLL:{e}")
						# Handle the case where response is not a valid float
						gauge_cll = -1
				else:
					gauge_bc = self.vacuum_main
					gauge_mc = self.variables.vacuum_buffer
					gauge_ll = self.vacuum_load_lock
					gauge_cll = self.vacuum_cryo_load_lock

				board_num = 0
				value_temperature = []
				for i in range(8):
					options = TInOptions.NOFILTER
					val = float(ul.t_in(board_num, i, TempScale.CELSIUS, options))
					value_temperature.append(round(val, 3))
				# print("Channel{:d} - {:s}:  {:.3f} Degrees.".format(i, channel_list[i], value_temperature[i]))
				value_temperature = np.array(value_temperature, dtype=np.dtype(float))

				new_row = [self.now.strftime("%d-%m-%Y"), datetime.now().strftime('%H:%M:%S'), index,
				           gauge_mc, gauge_bc, gauge_ll, gauge_cll,
						   value_temperature[0], value_temperature[1], value_temperature[2],
						   value_temperature[3], value_temperature[4], value_temperature[5], value_temperature[6],
						   value_temperature[7]]

				self.data.loc[len(self.data)] = new_row

				index = index + 1
				if index % 20 == 0:
					try:
						self.data.to_csv(self.file_name, sep=';', index=False)
					except Exception as e:
						self.data.to_csv(self.file_name_backup, sep=';', index=False)
						print('csv File cannot be saved')
						print('close the csv file')
						print(e)

				end_time = time.perf_counter()
				elapsed_time = end_time - start_time
				remaining_time = desired_period - elapsed_time

				if remaining_time > 0:
					time.sleep(remaining_time)

	def plot(self):
		"""
		Plot function.

		Args:
			None
		Returns:
			None
		"""
		time_range = 900  # 15 minutes
		time = self.data['timestamp'].tail(time_range).to_numpy()
		MC_NEG = self.data['MC_NEG'].tail(time_range).to_numpy()
		MC_Det = self.data['MC_Det'].tail(time_range).to_numpy()
		Mc_Top = self.data['Mc_Top'].tail(time_range).to_numpy()
		MC_Gate = self.data['MC_Gate'].tail(time_range).to_numpy()
		BC_Top = self.data['BC_Top'].tail(time_range).to_numpy()
		BC_Pump = self.data['BC_Pump'].tail(time_range).to_numpy()
		MC_vacuum = self.data['MC_vacuum'].tail(time_range).to_numpy()
		BC_vacuum = self.data['BC_vacuum'].tail(time_range).to_numpy()
		LL_vacuum = self.data['LL_vacuum'].tail(time_range).to_numpy()
		CLL_vacuum = self.data['CLL_vacuum'].tail(time_range).to_numpy()
		CLL_gate = self.data['CLL_gate'].tail(time_range).to_numpy()
		LL_pump = self.data['LL_pump'].tail(time_range).to_numpy()

		self.tempretures.clear()
		self.presures.clear()

		self.tempretures.plot(time, MC_NEG, pen='b', name='MC_NEG')
		self.tempretures.plot(time, MC_Det, pen='g', name='MC_Det')
		self.tempretures.plot(time, Mc_Top, pen='r', name='Mc_Top')
		self.tempretures.plot(time, MC_Gate, pen='c', name='MC_Gate')
		self.tempretures.plot(time, BC_Top, pen='m', name='BC_Top')
		self.tempretures.plot(time, BC_Pump, pen='y', name='BC_Pump')
		self.tempretures.plot(time, CLL_gate, pen='orange', name='CLL_gate')
		self.tempretures.plot(time, LL_pump, pen='w', name='LL_pump')


		self.presures.plot(time, MC_vacuum, pen='r', name='MC_vacuum')
		self.presures.plot(time, BC_vacuum, pen='g', name='BC_vacuum')
		self.presures.plot(time, LL_vacuum, pen='b', name='LL_vacuum')
		self.presures.plot(time, CLL_vacuum, pen='c', name='CLL_vacuum')

		self.tempretures.enableAutoRange(axis='x')
		self.presures.enableAutoRange(axis='x')

	def save_data_csv(self):
		"""
		save_data_csv function.
		Args:
			None
		Returns:
			None
		"""
		now = datetime.now()
		now_time = now.strftime("%d-%m-%Y_%H-%M-%S")
		self.data.to_csv(self.save_path + '/manual_save_%s.csv' % now_time,
		                 sep=';', index=False)

	def stop(self):
		"""
		Stop function.

		Args:
			None
		Returns:
			None
		"""
		self.running = False
		self.timer.stop()  # Stop the QTimer


class BakingWindow(QtWidgets.QWidget):
	closed = QtCore.pyqtSignal()  # Define a custom closed signal
	def __init__(self, gui_baking, *args, **kwargs):
		"""
		Initialize the BakingWindow class.

		Args:
			gui_baking: An instance of the GUI baking class.
			*args: Variable length argument list.
			**kwargs: Arbitrary keyword arguments.
		"""
		super().__init__(*args, **kwargs)
		self.gui_baking = gui_baking

	def closeEvent(self, event):
		"""
		Override the close event to stop the background thread and perform additional cleanup if needed.

		Args:
			event: The close event.
		"""
		self.gui_baking.stop()  # Call the stop method to stop the background thread
		# Additional cleanup code here if needed
		self.closed.emit()  # Emit the custom closed signal
		super().closeEvent(event)

	def setWindowStyleFusion(self):
		# Set the Fusion style
		QtWidgets.QApplication.setStyle("Fusion")


if __name__ == "__main__":
	try:
		# Load the JSON file
		configFile = 'config.json'
		p = os.path.abspath(os.path.join(__file__, "../../.."))
		os.chdir(p)
		conf = read_files.read_json_file(configFile)
	except Exception as e:
		print('Can not load the configuration file')
		print(e)
		sys.exit()

	# Initialize global experiment variables
	manager = multiprocessing.Manager()
	ns = manager.Namespace()
	variables = share_variables.Variables(conf, ns)

	app = QtWidgets.QApplication(sys.argv)
	app.setStyle('Fusion')
	Baking = QtWidgets.QWidget()
	SignalEmitter_Pumps_Vacuum = gui_pumps_vacuum.SignalEmitter()
	ui = Ui_Baking(variables, conf, SignalEmitter_Pumps_Vacuum)
	ui.setupUi(Baking)
	Baking.show()
	sys.exit(app.exec())
