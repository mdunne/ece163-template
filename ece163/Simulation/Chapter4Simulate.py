from . import Simulate
from ..Modeling import VehicleAerodynamicsModel

class Chapter4Simulate(Simulate.Simulate):
	def __init__(self):
		super().__init__()
		self.inputNames.extend(['Throttle', 'Aileron', 'Elevator', 'Rudder'])
		self.underlyingModel = VehicleAerodynamicsModel.VehicleAerodynamicsModel()

		self.variableList.append((self.underlyingModel.getForcesMoments, 'ForceMoments',
									['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz']))

		self.variableList.append((self.underlyingModel.getVehicleState, 'state',
									['pn', 'pe', 'pd', 'yaw', 'pitch', 'roll', 'u', 'v', 'w', 'p', 'q', 'r', 'Va', 'alpha', 'beta']))
		# self.dT = 1/50


	def getVehicleState(self):
		return self.underlyingModel.getVehicleState()

	def takeStep(self, controlInput):
		self.time += self.underlyingModel.vehicleDynamics.dT
		self.underlyingModel.Update(controlInput)
		self.recordData([controlInput.Throttle, controlInput.Aileron, controlInput.Elevator, controlInput.Rudder])
		return

	def reset(self):
		self.underlyingModel.reset()
		self.takenData.clear()