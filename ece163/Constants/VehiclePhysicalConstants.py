"""All the vehicle constants that define the various constants that are used in the simulation and control
   model. These are physical constants, mathematical constants, and the rest."""

import math
from ece163.Utilities import MatrixMath
from ece163.Containers import States
from ece163.Containers import Inputs

LINEARMAX = 250
ROTATEMAX = 180

dT = 1/100	# Time step for simulation

# parameters for Aerosonde UAV
InitialSpeed = 25.0 # [m/s]
InitialHeight = -100.0 # [m], negative is above ground

mass = 11  # [kg]
rho = 1.2682  # [kg / m^3]
g0 = 9.81  # gravity, [m/s^2]
b = 2.8956  # wing-span [m]
c = 0.18994  # wing chord [m]
S = 0.55  # wing area [m^2]
e = 0.9  # Oswald's Efficiency Factor []

AR = b ** 2 / S

M = 50.  # barrier function coefficient for angle of attack
alpha0 = math.radians(27.)  # angle at which stall occurs [deg]

Jxx = 0.8244  # [kg m^2]
Jyy = 1.135  # [kg m^2]
Jzz = 1.759  # [kg m^2]
Jxz = 0.1204  # [kg m^2]

Jbody = [[Jxx, 0., -Jxz], [0., Jyy, 0.], [-Jxz, 0., Jzz]]
Jdet = (Jxx * Jzz - Jxz ** 2)
JinvBody = MatrixMath.matrixScalarMultiply(1. / Jdet, [[Jzz, 0., Jxz], [0., Jdet / Jyy, 0.], [Jxz, 0., Jxx]])

# Aerodynamic Partial Derivatives for Forces

# Lift
CL0 = 0.23  # zero angle of attack lift coefficient
CLalpha = math.pi * AR / (1 + math.sqrt(1 + (AR / 2.) ** 2))
CLalpha = 5.61  # given in book
CLq = 7.95  # needs to be normalized by c/2*Va
CLdeltaE = 0.13  # lift due to elevator deflection

# Drag
CDp = 0.0  # minimum drag
CDalpha = 0.03  # drag slope
CD0 = 0.043  # intercept of linarized drag slope
CDq = 0  # drag wrt pitch rate
CDdeltaE = 0.0135  # drag due to elevator deflection

# Pitching Moment
CM0 = 0.0135  # intercept of pitching moment
CMalpha = -2.74  # pitching moment slope
CMq = -38.21  # pitching moment wrt q
CMdeltaE = -0.99  # pitching moment from elevator

# Sideforce
CY0 = 0.
CYbeta = -0.98
CYp = 0.
CYr = 0.
CYdeltaA = 0.075
CYdeltaR = 0.19

# Rolling Moment
Cl0 = 0.
Clbeta = -0.13
Clp = -0.51
Clr = 0.25
CldeltaA = 0.17
CldeltaR = 0.0024

# Yawing Moment
Cn0 = 0.
Cnbeta = 0.073
Cnp = 0.069
Cnr = -0.095
CndeltaA = -0.011
CndeltaR = -0.069

# Propeller Thrust
Sprop = 0.2027 # propellor area [m^2]
kmotor = 80.  # motor constant
kTp = 0.  # motor torque constant
kOmega = 0.  # motor speed constant
Cprop = 1.0  # propeller thrust coefficient

# Alternate Propellor Model
D_prop = 20. * (0.0254)  # prop diameter in m
#
# # Motor parameters
KV = 145.  # from datasheet RPM/V
KQ = (1. / KV) * 60. / (2. * math.pi)  # KQ in N-m/A, V-s/rad
R_motor = 0.042  # ohms
i0 = 1.5  # no-load (zero-torque) current (A)

# Inputs
ncells = 12.
V_max = 3.7 * ncells  # max voltage for specified number of battery cells

# Coeffiecients from prop_data fit (from lecture slide)
C_Q2 = -0.01664
C_Q1 = 0.004970
C_Q0 = 0.005230
C_T2 = -0.1079
C_T1 = -0.06044
C_T0 = 0.09357

# Dyden Wind Gust Model Coefficients
DrydenLowAltitudeLight = Inputs.drydenParameters(200.0, 200.0, 50.0, 1.06, 1.06, 0.7)
DrydenLowAltitudeModerate = Inputs.drydenParameters(200.0, 200.0, 50.0, 2.12, 2.12, 1.4)
DrydenHighAltitudeLight = Inputs.drydenParameters(533.0, 533.0, 533.0, 1.5, 1.5, 1.5)
DrydenHighAltitudeModerate = Inputs.drydenParameters(533.0, 533.0, 533.0, 3.0, 3.0, 3.0)
DrydenNoGusts = Inputs.drydenParameters(200.0, 200.0, 50.0, 0.0, 0.0, 0.0)
DrydenNoWind = Inputs.drydenParameters(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)

SteadyWinds = [('No Wind',(0.0, 0.0, 0.0)),('Light Wind',(3.0, -5.0, 0.0)),
			   ('Moderate Wind',(-12.0, 3.5, 0.0)), ('Strong Wind',(-16.0, -16.0, 0.0))]
GustWinds = [('Light Low Altitude', DrydenLowAltitudeLight), ('Moderate Low Altitude', DrydenLowAltitudeModerate),
			 ('Light High Altitude', DrydenHighAltitudeLight), ('Moderate High Altitude', DrydenHighAltitudeModerate)]

