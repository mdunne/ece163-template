"""
widget which handles the creation of linear models and determining the gains
"""

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from ..Controls import VehiclePerturbationModels
from ..Containers import Controls
from ..Controls import VehicleControlGains
import sys
import os
import datetime

import math
import threading
import pickle

lateralNames = ['Wn_roll', 'Zeta_roll', 'Wn_course', 'Zeta_course', 'Wn_sideslip', 'Zeta_sideslip']
longitudinalNames = ['Wn_pitch', 'Zeta_pitch', 'Wn_altitude','Zeta_altitude', 'Wn_SpeedfromThrottle',
                        'Zeta_SpeedfromThrottle', 'Wn_SpeedfromElevator', 'Zeta_SpeedfromElevator']

gainNames = ['kp_roll', 'kd_roll', 'ki_roll', 'kp_sideslip', 'ki_sideslip', 'kp_course', 'ki_course',
				'kp_pitch', 'kd_pitch', 'kp_altitude', 'ki_altitude', 'kp_SpeedfromThrottle', 'ki_SpeedfromThrottle',
                'kp_SpeedfromElevator', 'ki_SpeedfromElevator']
longitudinalGainNames = []

defaultTuningParameterFileName = "VehicleTuningParameters_Data.pickle"
defaultGainsFileName = "VehicleGains_Data.pickle"

class controlGainsWidget(QWidget):
	def __init__(self, guiControls, callBackOnSuccesfulGains=None, parent=None):
		super().__init__(parent)

		self.perturbationInstance = VehiclePerturbationModels.VehiclePerturbation()
		self.gainsInstance = VehicleControlGains.VehicleControlGains()
		self.curGains = Controls.controlGains()
		self.callBackOnSuccesfulGains = callBackOnSuccesfulGains
		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)

		topBoxEnclosure = QHBoxLayout()
		self.usedLayout.addLayout(topBoxEnclosure)

		inputBox = QVBoxLayout()
		inputBox.addWidget(QLabel("Tuning Parameters"))
		outputBox = QVBoxLayout()
		outputBox.addWidget(QLabel("Calculated Gains"))
		topBoxEnclosure.addLayout(inputBox)
		topBoxEnclosure.addLayout(outputBox)
		topBoxEnclosure.addStretch()

		# self.ParameterTabs = QTabWidget()
		# self.usedLayout.addWidget(self.ParameterTabs)

		# self.lateralGainsWidget = QWidget()
		# self.ParameterTabs.addTab(self.lateralGainsWidget, "Lateral Gains")

		# lateralGainsLayout = QGridLayout()
		# self.lateralGainsWidget.setLayout(lateralGainsLayout)
		self.parameterGainValues = dict()

		formLayout = QFormLayout()
		inputBox.addLayout(formLayout)
		inputBox.addStretch()
		try:
			with open(os.path.join(sys.path[0], defaultTuningParameterFileName), 'rb') as f:
				savedParameters = pickle.load(f)
		except FileNotFoundError:
			savedParameters = Controls.controlTuning()
			for pName in lateralNames+longitudinalNames:
				setattr(savedParameters, pName, 1)

		for boxName, parNames in zip(['Lateral Autopilot', 'Longitudinal Autopilot'], [lateralNames, longitudinalNames]):
			sectionName = QLabel(boxName)
			sectionName.setAlignment(Qt.AlignLeft)
			formLayout.addRow(sectionName)
			for parameterName in parNames:
				# newInput = doubleInputWithLabel.doubleInputWithLabel(parameterName)
				newInput = QLineEdit()
				newValidator = QDoubleValidator()
				newInput.setValidator(newValidator)
				newInput.setText("{}".format(getattr(savedParameters, parameterName)))
				formLayout.addRow(parameterName, newInput)
				# inputBox.addWidget(newInput)
				self.parameterGainValues[parameterName] = newInput

		compression = QHBoxLayout()
		self.usedLayout.addLayout(compression)

		self.calcGainsButton = QPushButton("Calculate Gains")
		self.calcGainsButton.clicked.connect(self.calculateGainsResponse)
		compression.addWidget(self.calcGainsButton)
		self.saveGainsButton = QPushButton("Save Gains")
		self.saveGainsButton.clicked.connect(self.saveGainsResponse)
		compression.addWidget(self.saveGainsButton)

		self.statusText = QLabel("No Info")
		compression.addWidget(self.statusText)
		compression.addStretch()


		self.gainsTextBox = QPlainTextEdit()
		self.gainsTextBox.setReadOnly(True)
		outputBox.addWidget(self.gainsTextBox)
		outputBox.addStretch()

		try:
			with open(os.path.join(sys.path[0], defaultGainsFileName), 'rb') as f:
				self.curGains = pickle.load(f)
			self.updateGainsDisplay(self.curGains)
		except FileNotFoundError:
			pass
		self.usedLayout.addStretch()

	def createLinearizedModels(self, trimState=None, trimInput=None):
		if trimState is None:
			trimState = self.perturbationInstance.trimState
		if trimInput is None:
			trimInput = self.perturbationInstance.trimInputs

		self.perturbationInstance.setTrimStateandInputs(trimState, trimInput)
		# self.perturbationInstance.CreateStateSpace()
		self.perturbationInstance.CreateTransferFunction()
		# self.perturbationInstance.exportPertubationModels(os.path.join(sys.path[0], VehiclePerturbationModels.defaultPerturbationFilename))
		self.statusText.setText("Linearized Models Made at {}".format(datetime.datetime.now()))
		return

	def calculateGainsResponse(self):
		"""
		calculate the gains given the linear model here

		:return:
		"""
		newParameters = Controls.controlTuning()
		for parameter in lateralNames+longitudinalNames:
			if hasattr(newParameters, parameter):
				setattr(newParameters, parameter, float(self.parameterGainValues[parameter].text()))
			else:
				print(parameter)
		with open(os.path.join(sys.path[0], defaultTuningParameterFileName), 'wb') as f:
			pickle.dump(newParameters, f)
		self.gainsInstance.setLinearizedModel(self.perturbationInstance.transferFunction)
		self.gainsInstance.computeGains(newParameters)
		self.curGains = self.gainsInstance.getControlGains()
		self.updateGainsDisplay(self.gainsInstance.controlGains)
		self.statusText.setText(("Gains Calculated"))
		if self.callBackOnSuccesfulGains is not None:
			self.callBackOnSuccesfulGains()
		return

	def updateGainsDisplay(self, newGains):
		self.gainsTextBox.clear()
		for name in gainNames:
			self.gainsTextBox.appendPlainText("{}: {}".format(name, getattr(newGains, name)))

	def saveGainsResponse(self):
		"""
		we save the gains here
		"""
		with open(os.path.join(sys.path[0], defaultGainsFileName), 'wb') as f:
			pickle.dump(self.curGains, f)

		return
