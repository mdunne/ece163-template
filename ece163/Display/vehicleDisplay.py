"""
This module handles displaying the vehicle in an OpenGL window for easy visualization
"""
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import pyqtgraph.opengl
import pyqtgraph
from ..Modeling import VehicleGeometry
import numpy
from ..Containers import States

defaultZoom = 200
defaultAzimuth = 45
defaultElevation = 30
defaultZoomTick = 50

class vehicleDisplay(QWidget):
	updateVehiclePositionSignal = pyqtSignal(list)
	def __init__(self, parent=None):
		"""
		sets up the full window with the plane along with a row of camera controls
		"""
		super().__init__(parent)

		self.usedLayout = QVBoxLayout()
		self.setLayout(self.usedLayout)
		self.trackPlane = True

		self.lastPlanePos = pyqtgraph.Vector(0, 0, 0)

		# we will always have the openGLBase Widget
		self.openGLWindow = pyqtgraph.opengl.GLViewWidget()
		self.usedLayout.addWidget(self.openGLWindow)

		# a random grid, will likely be changed afterwards
		self.openGLWindow.setGeometry(0, 0, 1000, 1000)
		self.grid = pyqtgraph.opengl.GLGridItem()
		self.grid.scale(200, 200, 200)
		self.grid.setSize(2000, 2000, 2000)
		self.openGLWindow.addItem(self.grid)

		# and an arbitrary camera starting position
		self.openGLWindow.setCameraPosition(distance=defaultZoom, elevation=defaultElevation, azimuth=defaultAzimuth)

		# a copy of the vehicle, we assume we will always want a vehicle
		self.vehicleDrawInstance = VehicleGeometry.VehicleGeometry()

		# we need to grab the vertices for the vehicle each update
		newVertices = numpy.array(self.vehicleDrawInstance.getNewPoints(0, 0, 0, 0, 0, 0))

		# faces and colors only need to be done once
		newFaces = numpy.array(self.vehicleDrawInstance.faces)
		newColors = numpy.array(self.vehicleDrawInstance.colors)

		# we convert the vertices to meshdata which allows us not to have to translate points every time
		self.vehicleMeshData = pyqtgraph.opengl.MeshData(vertexes=newVertices, faces=newFaces, faceColors=newColors)

		# and we create the meshItem, we do not smooth to make the triangles be clean colors
		self.openGLVehicle = pyqtgraph.opengl.GLMeshItem(meshdata=self.vehicleMeshData, drawEdges=True, smooth=False, computeNormals=False)

		# always add the vehicle to the display
		self.openGLWindow.addItem(self.openGLVehicle)

		# and add an axis

		self.Axis = pyqtgraph.opengl.GLAxisItem(glOptions='additive')
		self.Axis.setSize(2000, 2000, 2000)
		self.openGLWindow.addItem(self.Axis)
		self.updateVehiclePositionSignal.connect(self.drawNewVehiclePosition)

		# we add another hbox for camera controls

		cameraControlBox = QHBoxLayout()
		self.usedLayout.addLayout(cameraControlBox)

		zoomInButton = QPushButton("Zoom In")
		zoomInButton.clicked.connect(self.ZoomIn)
		zoomOutButton = QPushButton("Zoom Out")
		zoomOutButton.clicked.connect(self.ZoomOut)
		cameraControlBox.addWidget(zoomInButton)
		cameraControlBox.addWidget(zoomOutButton)

		self.trackButton = QPushButton("Track")
		self.trackButton.clicked.connect(self.TrackButtonResponse)
		cameraControlBox.addWidget(self.trackButton)

		self.manualButton = QPushButton("Manual")
		self.manualButton.clicked.connect(self.ManualButtonResponse)
		cameraControlBox.addWidget(self.manualButton)

		self.resetCameraButton = QPushButton("Reset")
		self.resetCameraButton.clicked.connect(self.resetCameraView)
		cameraControlBox.addWidget(self.resetCameraButton)

		self.__setCameraModeButtons()
		return

	def sizeHint(self):
		"""
		Tells Qt preferred size for widget
		"""
		return QSize(720, 480)

	def updateVehiclePosition(self, newState):
		"""
		Updates the vehicle position

		:param newState: vehicleState instance to extract the needed parameters from
		"""
		self.updateVehiclePositionSignal.emit([newState.pn*VehicleGeometry.baseUnit, newState.pe*VehicleGeometry.baseUnit, newState.pd*VehicleGeometry.baseUnit, newState.yaw, newState.pitch, newState.roll])
		return

	def drawNewVehiclePosition(self, newPosition):
		"""
		Handles update of the plane in the window, NEVER CALLED directly.

		:param newPosition: new position as a list
		"""

		# we simply create a new set of vertices
		newVertices=numpy.array(self.vehicleDrawInstance.getNewPoints(*newPosition))
		self.vehicleMeshData.setVertexes(newVertices)  # update our mesh with them
		self.openGLVehicle.setMeshData(meshdata=self.vehicleMeshData, smooth=False, computeNormals=False)  # and setMeshData automatically invokes a redraw
		self.lastPlanePos = pyqtgraph.Vector(newPosition[1], newPosition[0], -newPosition[2])
		if self.trackPlane:
			self.openGLWindow.setCameraPosition(pos=self.lastPlanePos)
		return

	def ZoomIn(self):
		"""
		Zooms in by default tick
		"""
		self.openGLWindow.opts['distance'] -= defaultZoomTick
		self.openGLWindow.update()
		return

	def ZoomOut(self):
		"""
		Zooms out by default tick
		"""
		self.openGLWindow.opts['distance'] += defaultZoomTick
		self.openGLWindow.update()
		return

	def __setCameraModeButtons(self):
		self.trackButton.setDisabled(self.trackPlane)
		self.manualButton.setDisabled(not self.trackPlane)

	def ManualButtonResponse(self):
		"""
		Sets camera to manual mode
		"""
		self.trackPlane = False
		self.__setCameraModeButtons()
		self.openGLWindow.setCameraPosition(pos=pyqtgraph.Vector(0, 0, 0))
		return

	def TrackButtonResponse(self):
		"""
		Sets Camera to Track plane
		"""
		self.trackPlane = True
		self.__setCameraModeButtons()
		self.openGLWindow.setCameraPosition(pos=self.lastPlanePos)
		self.openGLWindow.update()
		return

	def resetCameraView(self):
		"""
		Resets the camera to the default azimuth, elevation and zoom. This does not change the tracking mode
		"""
		self.openGLWindow.setCameraPosition(distance=defaultZoom, azimuth=defaultAzimuth, elevation=defaultElevation)
