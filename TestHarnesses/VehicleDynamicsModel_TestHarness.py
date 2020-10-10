"""
.. modle:: VehicleDynamicsModel_TestHarness.py
	:platform: MacOS, Unix, Windows,
	:synopsis: Compares output from VehicleDynamicsModelGeneration.py with 
	students'  function implementations
.. moduleauthor:: Pavlo Vlastos <pvlastos@ucsc.edu>
"""
import os
import sys
sys.path.insert(0, os.path.abspath('..'))
import math

import ece163.Utilities.MatrixMath as MatrixMath
import ece163.Utilities.Rotations as Rotations
import ece163.Modeling.VehicleDynamicsModel as VDM
import ece163.Containers.States as States
import argparse
import random
import pickle
import traceback

#  these two functions allow for more standardized output, they should be copied to each test harness and customized
def printTestBlockResult(function, testsPassed, testCount):
	if testsPassed != testCount:
		addendum = " (TESTS FAILED)"
	else:
		addendum = ""
	print("{}/{} tests passed for {}{}".format(testsPassed, testCount, function.__name__, addendum))

def printTestFailure(function, inputs, outputs, expectedoutputs):
	print("Test Failed for {}. Please find repr version of the inputs below for testing".format(function.__name__))
	print("Inputs: {}".format(repr(inputs)))
	print("Outputs: {}".format(repr(outputs)))
	print("Expected Outputs: {}".format(repr(expectedoutputs)))
###############################################################################

# Instantiate a vehicle dynamics model object
vehDyMo = VDM.VehicleDynamicsModel()

###############################################################################
parser = argparse.ArgumentParser()
parser.add_argument('-c','--continueMode', action='store_true', help='Runs all tests regardless of failures')
parser.add_argument('picklePath', nargs='?', default='VehicleDynamicsModel_TestData.pickle', help='valid path to pickle for input')
arguments = parser.parse_args()

picklePath = arguments.picklePath
inContinueMode = arguments.continueMode

print("Beginning Test Harness for Vehilce Dynamics Model using file {}".format(picklePath))
try:
	with open(picklePath, 'rb') as f:
		allTests = pickle.load(f)
except FileNotFoundError:
	print('Test file not found, exiting')
	sys.exit(-1)

testBlocksPassed = 0  # we keep track of the number of test blocks passed

testBlockIterator = iter(allTests)  # we hard code the tests as well so we need an iterator

###############################################################################
# getVehicleState()
print("Comparing outputs for {}".format(vehDyMo.getVehicleState.__name__))
curTestBlock = next(testBlockIterator)  # we now have all the tests for this block
testsPassed = 0
for state, expectedResult in curTestBlock:  # and now we can iterate through them
	try:
		vehDyMo.setVehicleState(state)
		result = vehDyMo.getVehicleState()
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.getVehicleState, state, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.getVehicleState, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# setVehicleState()
print("Comparing outputs for {}".format(vehDyMo.setVehicleState.__name__))
curTestBlock = next(testBlockIterator)  
testsPassed = 0
for state, expectedResult in curTestBlock:  
	try:
		vehDyMo.setVehicleState(state)
		result = vehDyMo.getVehicleState()
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.setVehicleState, state, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.setVehicleState, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# resetVehicleState()
print("Comparing outputs for {}".format(vehDyMo.resetVehicleState.__name__))
curTestBlock = next(testBlockIterator)  
testsPassed = 0
for previousVDM, expectedVDM in curTestBlock: 
	try:
		vehDyMo.setVehicleState(previousVDM.state)
		vehDyMo.resetVehicleState()
		resultingVDM = VDM.VehicleDynamicsModel()
		resultingVDM.setVehicleState(vehDyMo.state)
		if resultingVDM.state == expectedVDM.state:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.resetVehicleState, previousVDM.state, resultingVDM.state, expectedVDM.state)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.resetVehicleState, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# reset()
print("Comparing outputs for {}".format(vehDyMo.reset.__name__))
curTestBlock = next(testBlockIterator)  
testsPassed = 0
for previousVDM, expectedVDM in curTestBlock: 
	try:
		vehDyMo.setVehicleState(previousVDM.state)
		vehDyMo.resetVehicleState()
		resultingVDM = VDM.VehicleDynamicsModel()
		resultingVDM.setVehicleState(vehDyMo.state)
		if resultingVDM.state == expectedVDM.state:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.resetVehicleState, state, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.resetVehicleState, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# derivative()
print("Comparing outputs for {}".format(vehDyMo.derivative.__name__))
curTestBlock = next(testBlockIterator)  
testsPassed = 0
for previousVDM, fmInputs, expectedResult in curTestBlock: 
	try:
		vehDyMo.setVehicleState(previousVDM.state)
		result = vehDyMo.derivative(vehDyMo.state, fmInputs)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.derivative, vehDyMo.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.derivative, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# Rexp()
print("Comparing outputs for {}".format(vehDyMo.Rexp.__name__))
curTestBlock = next(testBlockIterator)  
testsPassed = 0
for dT, previousVDM, dot, expectedResult in curTestBlock: 
	try:
		vehDyMo.setVehicleState(previousVDM.state)
		result = vehDyMo.Rexp(dT, vehDyMo.state, dot)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.Rexp, vehDyMo.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.Rexp, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# IntegrateState()
print("Comparing outputs for {}".format(vehDyMo.IntegrateState.__name__))
curTestBlock = next(testBlockIterator)  
testsPassed = 0
for dT, previousVDM, dot, expectedResult in curTestBlock: 
	try:
		vehDyMo.setVehicleState(previousVDM.state)
		result = vehDyMo.IntegrateState(dT, vehDyMo.state, dot)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.IntegrateState, vehDyMo.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.IntegrateState, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# ForwardEuler()
print("Comparing outputs for {}".format(vehDyMo.ForwardEuler.__name__))
curTestBlock = next(testBlockIterator)  
testsPassed = 0
for previousVDM, fmInputs, expectedResult in curTestBlock: 
	try:
		vehDyMo.setVehicleState(previousVDM.state)
		result = vehDyMo.ForwardEuler(fmInputs)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.ForwardEuler, vehDyMo.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.ForwardEuler, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# Update()
print("Comparing outputs for {}".format(vehDyMo.Update.__name__))
UpdateTestBlockCount = 0

###############################################################################
# Update() Block 0
print("Update Test Block {}".format(UpdateTestBlockCount))
UpdateTestBlockCount += 1
curTestBlock = next(testBlockIterator)
testsPassed = 0
for previousVDM, fmInputs, expectedResult in curTestBlock:
	try:
		result = previousVDM.Update(fmInputs)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.Update, previousVDM.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.Update, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# Update() Block 1
print("Update Test Block {}".format(UpdateTestBlockCount))
UpdateTestBlockCount += 1
curTestBlock = next(testBlockIterator)
testsPassed = 0
for previousVDM, fmInputs, expectedResult in curTestBlock:
	try:
		result = previousVDM.Update(fmInputs)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.Update, previousVDM.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.Update, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# Update() Block 2
print("Update Test Block {}".format(UpdateTestBlockCount))
UpdateTestBlockCount += 1
curTestBlock = next(testBlockIterator)
testsPassed = 0
for previousVDM, fmInputs, expectedResult in curTestBlock:
	try:
		result = previousVDM.Update(fmInputs)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.Update, previousVDM.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.Update, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# Update() Block 3
print("Update Test Block {}".format(UpdateTestBlockCount))
UpdateTestBlockCount += 1
curTestBlock = next(testBlockIterator)
testsPassed = 0
for previousVDM, fmInputs, expectedResult in curTestBlock:
	try:
		result = previousVDM.Update(fmInputs)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.Update, previousVDM.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.Update, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# Update() Block 4
print("Update Test Block {}".format(UpdateTestBlockCount))
UpdateTestBlockCount += 1
curTestBlock = next(testBlockIterator)
testsPassed = 0
for previousVDM, fmInputs, expectedResult in curTestBlock:
	try:
		result = previousVDM.Update(fmInputs)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.Update, previousVDM.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.Update, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# Update() Block 5
print("Update Test Block {}".format(UpdateTestBlockCount))
UpdateTestBlockCount += 1
curTestBlock = next(testBlockIterator)
testsPassed = 0
for previousVDM, fmInputs, expectedResult in curTestBlock:
	try:
		result = previousVDM.Update(fmInputs)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.Update, previousVDM.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.Update, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
# Update() Block 6
print("Update Test Block {}".format(UpdateTestBlockCount))
UpdateTestBlockCount += 1
curTestBlock = next(testBlockIterator)
testsPassed = 0
for previousVDM, fmInputs, expectedResult in curTestBlock:
	try:
		result = previousVDM.Update(fmInputs)
		if result == expectedResult:
			testsPassed += 1
		else:
			if not inContinueMode:
				printTestFailure(vehDyMo.Update, previousVDM.state, fmInputs, result, expectedResult)
				sys.exit(-1)
	except Exception as e:  # overly broad exception clause but we want it to catch everything
		print('Test harness failed with the exception below. It will not continue')
		print(traceback.format_exc())
		sys.exit(-1)

printTestBlockResult(vehDyMo.Update, testsPassed, len(curTestBlock))
if testsPassed == len(curTestBlock):
	testBlocksPassed += 1

###############################################################################
if testBlocksPassed == len(allTests):
	print("All tests Passed for Vehicle Dynamics Model")
else:
	print("{}/{} tests blocks passed for Vehicle Dynamics Model".format(testBlocksPassed, len(allTests)))

