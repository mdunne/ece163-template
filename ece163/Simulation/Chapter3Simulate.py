from . import Simulate
from ..Modeling import VehicleDynamicsModel

class Chapter3Simulate(Simulate.Simulate):
	def __init__(self):
		super().__init__()
		self.inputNames.extend(['Fx', 'Fy', 'Fz', 'Mx', 'My', 'Mz'])
		self.underlyingModel = VehicleDynamicsModel.VehicleDynamicsModel()
		self.variableList.append((self.underlyingModel.getVehicleState, 'state',
									['pn', 'pe', 'pd', 'yaw', 'pitch', 'roll', 'u', 'v', 'w', 'p', 'q', 'r']))
		# self.dT = 1/50


	def getVehicleState(self):
		return self.underlyingModel.getVehicleState()

	def takeStep(self, Forces):
		self.time += self.underlyingModel.dT
		self.underlyingModel.Update(Forces)
		self.recordData([Forces.Fx, Forces.Fy, Forces.Fz, Forces.Mx, Forces.My, Forces.Mz])
		return

	def reset(self):
		self.underlyingModel.reset()
		self.takenData.clear()